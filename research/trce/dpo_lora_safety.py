"""
DPO + LoRA Safety Fine-tuning for HunyuanImage 3.0
===================================================
适配方案：针对自回归MoE架构的安全对齐训练

架构确认：HunyuanImage 3.0 使用「统一自回归 + 扩散推理」混合范式：
- 基础架构：自回归Transformer Decoder + MoE
- 推理方式：自回归生成 + 扩散采样步骤
- wte.weight: (133120, 4096) — vocab × hidden_dim
- 64个MoE experts，激活参数130亿

核心策略：
1. LoRA：高效微调MoE层的attention投影
2. DPO：对比安全/风险样本的偏好对齐
3. MoE Expert Intervention：对专家激活模式进行干预

Author: WorkBuddy
Date: 2026-04-02
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np


# =============================================================================
# 数据结构定义
# =============================================================================

@dataclass
class SafetyDataSample:
    """安全微调数据样本"""
    prompt: str                          # 输入提示词
    is_safe: bool                        # 是否安全
    chosen_response: Optional[str] = None   # DPO偏好响应（安全）
    rejected_response: Optional[str] = None  # DPO拒绝响应（风险）
    risk_level: float = 0.0             # 风险等级 0-1

    def __post_init__(self):
        if self.is_safe:
            assert self.chosen_response is not None, "Safe samples need chosen_response"
        else:
            assert self.rejected_response is not None, "Unsafe samples need rejected_response"


@dataclass
class DPOConfig:
    """DPO训练配置"""
    # 基础参数
    learning_rate: float = 1e-4
    beta: float = 0.1                   # KL散度系数
    margin: float = 0.01                # 安全/风险间距
    gradient_accumulation_steps: int = 4

    # LoRA配置
    lora_rank: int = 16
    lora_alpha: float = 32
    lora_dropout: float = 0.05
    target_modules: List[str] = None    # 目标模块列表

    # 训练策略
    max_seq_length: int = 2048
    warmup_steps: int = 100
    num_epochs: int = 3
    batch_size: int = 2

    # 安全相关
    risk_threshold: float = 0.5         # 判定为风险的阈值
    enable_moe_intervention: bool = True
    moe_intervention_strength: float = 0.3

    # 设备
    device: str = "cuda"


# =============================================================================
# LoRA 实现
# =============================================================================

class LoRALinear(nn.Module):
    """
    LoRA 层：低秩适配矩阵

    原理：
    W_new = W_original + alpha/rank * A * B
    其中 A ∈ R^{rank×in_features}, B ∈ R^{out_features×rank}

    仅训练 A 和 B，原始权重冻结
    """

    def __init__(
        self,
        original_layer: nn.Linear,
        rank: int = 16,
        alpha: float = 32,
        dropout: float = 0.05
    ):
        super().__init__()
        self.original_layer = original_layer
        self.rank = rank
        self.alpha = alpha
        self.scale = alpha / rank

        # 冻结原始权重
        for param in self.original_layer.parameters():
            param.requires_grad = False

        # LoRA 适配矩阵
        in_features = original_layer.in_features
        out_features = original_layer.out_features

        self.lora_A = nn.Parameter(torch.zeros(rank, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        self.lora_dropout = nn.Dropout(p=dropout)

        # Xavier 初始化
        nn.init.normal_(self.lora_A, std=1.0 / np.sqrt(rank))
        nn.init.zeros_(self.lora_B)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """前向传播"""
        # 原始输出
        original_output = self.original_layer(x)

        # LoRA 调整
        # x @ A^T @ B^T = (x @ A^T) @ B^T
        lora_output = x @ self.lora_A.T @ self.lora_B.T

        return original_output + self.scale * self.lora_output

    def merge_weights(self):
        """合并LoRA权重到原始层（推理时使用）"""
        with torch.no_grad():
            delta_W = self.alpha / self.rank * (self.lora_B @ self.lora_A)
            self.original_layer.weight.data += delta_W
            # 清空LoRA参数
            self.lora_A.data.zero_()
            self.lora_B.data.zero_()


class HunyuanImage3LoRA:
    """
    HunyuanImage 3.0 的 LoRA 适配器

    目标模块：
    - q_proj, k_proj, v_proj (Self-Attention)
    - gate_proj, up_proj, down_proj (MoE FFN)
    """

    def __init__(
        self,
        model: nn.Module,
        config: DPOConfig
    ):
        self.model = model
        self.config = config
        self.lora_layers: Dict[str, LoRALinear] = {}
        self.original_weights_backup = {}

        # 默认目标模块
        if config.target_modules is None:
            config.target_modules = [
                "q_proj", "k_proj", "v_proj",          # Attention
                "gate_proj", "up_proj", "down_proj"    # MoE FFN
            ]

    def apply_lora(self):
        """在目标模块上应用LoRA"""
        print("[LoRA] Applying LoRA to HunyuanImage 3.0...")

        for name, module in self.model.named_modules():
            # 检查是否是Linear层且在目标模块列表中
            if isinstance(module, nn.Linear):
                module_name = name.split(".")[-1]  # 获取最后一级名称

                if module_name in self.config.target_modules:
                    # 检查是否已经应用过LoRA
                    if name not in self.lora_layers:
                        # 替换为LoRA层
                        lora_layer = LoRALinear(
                            original_layer=module,
                            rank=self.config.lora_rank,
                            alpha=self.config.lora_alpha,
                            dropout=self.config.lora_dropout
                        )

                        # 设置模块
                        self._set_module_by_name(self.model, name, lora_layer)
                        self.lora_layers[name] = lora_layer

        print(f"[LoRA] Applied to {len(self.lora_layers)} layers")

    def _set_module_by_name(self, model: nn.Module, name: str, module: nn.Module):
        """通过点分隔的名称设置模块"""
        parts = name.split(".")
        parent = model
        for part in parts[:-1]:
            parent = getattr(parent, part)
        setattr(parent, parts[-1], module)

    def _get_module_by_name(self, model: nn.Module, name: str) -> nn.Module:
        """通过点分隔的名称获取模块"""
        parts = name.split(".")
        module = model
        for part in parts:
            module = getattr(module, part)
        return module

    def get_trainable_parameters(self) -> List[nn.Parameter]:
        """获取所有可训练参数"""
        params = []
        for lora_layer in self.lora_layers.values():
            params.append(lora_layer.lora_A)
            params.append(lora_layer.lora_B)
        return params

    def save_lora_weights(self, path: str):
        """保存LoRA权重"""
        state_dict = {
            name: {
                "lora_A": layer.lora_A.data.clone(),
                "lora_B": layer.lora_B.data.clone()
            }
            for name, layer in self.lora_layers.items()
        }
        torch.save(state_dict, path)
        print(f"[LoRA] Saved to {path}")

    def load_lora_weights(self, path: str):
        """加载LoRA权重"""
        state_dict = torch.load(path, map_location="cpu")
        for name, weights in state_dict.items():
            if name in self.lora_layers:
                self.lora_layers[name].lora_A.data = weights["lora_A"].clone()
                self.lora_layers[name].lora_B.data = weights["lora_B"].clone()
        print(f"[LoRA] Loaded from {path}")


# =============================================================================
# MoE Expert Intervention
# =============================================================================

class MoEExpertIntervention:
    """
    MoE Expert 干预层

    原理：
    --------
    在HunyuanImage 3.0的MoE层中，不同的专家处理不同的概念域。
    通过分析专家激活模式，可以识别风险概念相关的专家，
    并在推理时降低其激活权重或替换为安全专家。

    方法：
    --------
    1. 识别处理风险概念的专家索引
    2. 计算专家激活的统计分布
    3. 对高风险专家施加惩罚或替换

    干预公式：
        expert_output = original_output * (1 - intervention_strength * risk_score)
    """

    def __init__(
        self,
        model: nn.Module,
        config: DPOConfig
    ):
        self.model = model
        self.config = config

        # 专家激活记录
        self.expert_activation_counts = {}  # expert_idx -> count
        self.expert_risk_scores = {}        # expert_idx -> risk_score

        # Hook句柄
        self.hooks = []

    def register_hooks(self):
        """注册前向hooks以跟踪专家激活"""
        def moe_hook(module, input, output, expert_idx):
            """记录专家激活"""
            if isinstance(output, torch.Tensor):
                activation = output.detach()
                # 计算激活强度（L2范数）
                strength = torch.norm(activation).item()

                if expert_idx not in self.expert_activation_counts:
                    self.expert_activation_counts[expert_idx] = []
                self.expert_activation_counts[expert_idx].append(strength)

        # 查找MoE层并注册hooks
        expert_idx = 0
        for name, module in self.model.named_modules():
            if "moe" in name.lower() or "expert" in name.lower():
                if isinstance(module, nn.Module):
                    hook = module.register_forward_hook(
                        lambda m, i, o, idx=expert_idx: moe_hook(m, i, o, idx)
                    )
                    self.hooks.append(hook)
                    expert_idx += 1

        print(f"[MoE Intervention] Registered {len(self.hooks)} expert hooks")

    def remove_hooks(self):
        """移除所有hooks"""
        for hook in self.hooks:
            hook.remove()
        self.hooks = []

    def compute_risk_scores(self, risk_concepts: List[str]):
        """
        基于风险概念计算专家风险评分

        Args:
            risk_concepts: 风险概念列表

        Returns:
            expert_risk_scores: {expert_idx -> risk_score}
        """
        # 方法1：基于激活统计计算风险评分
        # 高激活频率 + 高激活强度的专家可能是处理复杂/风险概念的专家

        total_activations = sum(
            len(acts) for acts in self.expert_activation_counts.values()
        )

        for expert_idx, activations in self.expert_activation_counts.items():
            if len(activations) > 0:
                # 平均激活强度
                avg_strength = np.mean(activations)
                # 激活频率
                frequency = len(activations) / max(total_activations, 1)

                # 综合评分（归一化）
                self.expert_risk_scores[expert_idx] = min(frequency * avg_strength * 10, 1.0)

        return self.expert_risk_scores

    def apply_intervention(
        self,
        expert_idx: int,
        original_output: torch.Tensor,
        risk_score: float
    ) -> torch.Tensor:
        """
        对专家输出应用干预

        Args:
            expert_idx: 专家索引
            original_output: 原始输出
            risk_score: 风险评分

        Returns:
            干预后的输出
        """
        if not self.config.enable_moe_intervention:
            return original_output

        # 风险评分越高，抑制越强
        suppression = self.config.moe_intervention_strength * risk_score

        # 软抑制：降低激活强度，但不归零
        intervened = original_output * (1 - suppression)

        return intervened


# =============================================================================
# DPO Safety Alignment
# =============================================================================

class DPOSafetyAlignment:
    """
    DPO (Direct Preference Optimization) 安全对齐

    原理：
    --------
    DPO通过直接优化偏好数据，使模型倾向于生成安全的响应。

    损失函数：
    L = - log σ(β * (log π(y_c|x) - log π(y_r|x) - r*))

    其中：
    - y_c: 安全的chosen响应
    - y_r: 不安全的rejected响应
    - r*: 参考margin
    - β: KL散度系数

    对于HunyuanImage 3.0：
    - 图像生成本身就是"响应"
    - 可以将安全生成 vs 风险生成作为偏好对
    """

    def __init__(
        self,
        model: nn.Module,
        ref_model: nn.Module,  # 参考模型（原始未微调版本）
        lora: HunyuanImage3LoRA,
        config: DPOConfig
    ):
        self.model = model
        self.ref_model = ref_model
        self.lora = lora
        self.config = config

        # 冻结参考模型
        for param in self.ref_model.parameters():
            param.requires_grad = False

        # 优化器（仅优化LoRA参数）
        self.optimizer = torch.optim.AdamW(
            self.lora.get_trainable_parameters(),
            lr=config.learning_rate
        )

        # 学习率调度器
        self.scheduler = None

    def compute_log_probs(
        self,
        model: nn.Module,
        prompts: List[str],
        responses: List[str],
        tokenizer
    ) -> torch.Tensor:
        """
        计算响应的对数概率

        Args:
            model: 模型
            prompts: 提示词列表
            responses: 响应列表
            tokenizer: 分词器

        Returns:
            对数概率张量
        """
        log_probs = []

        for prompt, response in zip(prompts, responses):
            # Tokenize
            prompt_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
            response_ids = tokenizer(response, return_tensors="pt")["input_ids"]

            # 拼接
            full_ids = torch.cat([prompt_ids, response_ids], dim=-1)

            # 获取模型输出
            outputs = model(full_ids)

            # 计算response部分的对数概率
            response_logits = outputs.logits[:, prompt_ids.shape[1]-1:-1]

            # Log softmax
            log_probs_response = F.log_softmax(response_logits, dim=-1)

            # 提取目标token的概率
            response_log_probs = log_probs_response.gather(
                dim=-1,
                index=response_ids.unsqueeze(-1)
            ).squeeze(-1)

            log_probs.append(response_log_probs.mean())

        return torch.stack(log_probs)

    def dpo_loss(
        self,
        log_probs_chosen: torch.Tensor,
        log_probs_rejected: torch.Tensor,
        ref_log_probs_chosen: torch.Tensor,
        ref_log_probs_rejected: torch.Tensor
    ) -> torch.Tensor:
        """
        计算DPO损失

        Args:
            log_probs_chosen: chosen响应的对数概率
            log_probs_rejected: rejected响应的对数概率
            ref_log_probs_chosen: 参考模型chosen对数概率
            ref_log_probs_rejected: 参考模型rejected对数概率

        Returns:
            DPO损失
        """
        # 优势（preference difference）
        advantage = (
            log_probs_chosen - log_probs_rejected
            - (ref_log_probs_chosen - ref_log_probs_rejected)
        ) / self.config.beta

        # 减去margin
        advantage = advantage - self.config.margin

        # 负对数损失
        loss = -F.logsigmoid(advantage).mean()

        return loss

    def train_step(
        self,
        batch: List[SafetyDataSample],
        tokenizer
    ) -> Dict[str, float]:
        """
        执行一次训练步骤

        Args:
            batch: 批量的安全数据样本
            tokenizer: 分词器

        Returns:
            训练指标
        """
        prompts = [sample.prompt for sample in batch]

        # 获取chosen和rejected响应
        chosen_responses = [
            sample.chosen_response for sample in batch
            if sample.chosen_response is not None
        ]
        rejected_responses = [
            sample.rejected_response for sample in batch
            if sample.rejected_response is not None
        ]

        # 计算对数概率
        pi_log_probs_chosen = self.compute_log_probs(
            self.model, prompts, chosen_responses, tokenizer
        )
        pi_log_probs_rejected = self.compute_log_probs(
            self.model, prompts, rejected_responses, tokenizer
        )

        ref_log_probs_chosen = self.compute_log_probs(
            self.ref_model, prompts, chosen_responses, tokenizer
        )
        ref_log_probs_rejected = self.compute_log_probs(
            self.ref_model, prompts, rejected_responses, tokenizer
        )

        # 计算损失
        loss = self.dpo_loss(
            pi_log_probs_chosen, pi_log_probs_rejected,
            ref_log_probs_chosen, ref_log_probs_rejected
        )

        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return {
            "loss": loss.item(),
            "advantage": (pi_log_probs_chosen - pi_log_probs_rejected).mean().item()
        }


# =============================================================================
# 端到端安全微调流水线
# =============================================================================

class HunyuanImage3SafetyTuner:
    """
    HunyuanImage 3.0 端到端安全微调流水线

    整合 LoRA + DPO + MoE Intervention

    使用示例:
    --------
    ```python
    import dpo_lora_safety as safety

    config = safety.DPOConfig(
        learning_rate=1e-4,
        lora_rank=16,
        lora_alpha=32,
        beta=0.1,
        enable_moe_intervention=True,
        moe_intervention_strength=0.3
    )

    tuner = safety.HunyuanImage3SafetyTuner(
        model=model,
        ref_model=ref_model,
        tokenizer=tokenizer,
        config=config
    )

    # 应用LoRA
    tuner.apply_lora()

    # 创建安全数据集
    dataset = safety.create_safety_dataset()

    # 微调
    tuner.train(dataset)

    # 保存
    tuner.save("hunyuan3_safe_lora.pt")
    ```
    """

    def __init__(
        self,
        model: nn.Module,
        ref_model: nn.Module,
        tokenizer,
        config: Optional[DPOConfig] = None
    ):
        self.model = model
        self.ref_model = ref_model
        self.tokenizer = tokenizer
        self.config = config or DPOConfig()

        # 初始化组件
        self.lora = HunyuanImage3LoRA(model, self.config)
        self.moe_intervention = MoEExpertIntervention(model, self.config)
        self.dpo = DPOSafetyAlignment(model, ref_model, self.lora, self.config)

        # 训练状态
        self.global_step = 0
        self.best_loss = float("inf")

    def apply_lora(self):
        """应用LoRA"""
        self.lora.apply_lora()
        self.moe_intervention.register_hooks()

    def train(
        self,
        dataset: List[SafetyDataSample],
        num_epochs: Optional[int] = None,
        eval_concepts: Optional[List[str]] = None
    ):
        """
        执行安全微调

        Args:
            dataset: 安全数据集
            num_epochs: 训练轮数
            eval_concepts: 用于评估的概念列表
        """
        num_epochs = num_epochs or self.config.num_epochs

        print("=" * 60)
        print("HunyuanImage 3.0 Safety Fine-tuning")
        print("=" * 60)

        for epoch in range(num_epochs):
            # 打乱数据
            np.random.shuffle(dataset)

            epoch_losses = []

            for i in range(0, len(dataset), self.config.batch_size):
                batch = dataset[i:i + self.config.batch_size]

                # DPO训练步骤
                metrics = self.dpo.train_step(batch, self.tokenizer)
                epoch_losses.append(metrics["loss"])

                self.global_step += 1

                if self.global_step % 10 == 0:
                    print(f"[Step {self.global_step}] Loss: {metrics['loss']:.4f}, "
                          f"Advantage: {metrics['advantage']:.4f}")

            avg_loss = np.mean(epoch_losses)
            print(f"[Epoch {epoch+1}/{num_epochs}] Average Loss: {avg_loss:.4f}")

            # 保存最佳模型
            if avg_loss < self.best_loss:
                self.best_loss = avg_loss
                self.save("best_safe_lora.pt")

    def evaluate(
        self,
        test_concepts: List[str],
        safe_alternatives: Dict[str, str]
    ) -> Dict[str, float]:
        """
        评估安全微调效果

        Args:
            test_concepts: 测试概念列表
            safe_alternatives: {风险概念 -> 安全替代}

        Returns:
            评估指标
        """
        print("=" * 60)
        print("Evaluating Safety Fine-tuning")
        print("=" * 60)

        results = {}

        for risk_concept, safe_concept in safe_alternatives.items():
            # 使用风险概念生成
            risk_output = self.model.generate(risk_concept)

            # 使用安全替代生成
            safe_output = self.model.generate(safe_concept)

            # 计算相似度
            similarity = F.cosine_similarity(
                risk_output.flatten().unsqueeze(0),
                safe_output.flatten().unsqueeze(0)
            ).item()

            results[risk_concept] = {
                "safe_similarity": similarity,
                "is_safe": similarity > 0.7  # 与安全输出相似视为安全
            }

        return results

    def save(self, path: str):
        """保存微调后的模型"""
        save_dict = {
            "lora_state_dict": {
                name: {
                    "lora_A": layer.lora_A.data,
                    "lora_B": layer.lora_B.data
                }
                for name, layer in self.lora.lora_layers.items()
            },
            "moe_risk_scores": self.moe_intervention.expert_risk_scores,
            "config": self.config,
            "global_step": self.global_step
        }
        torch.save(save_dict, path)
        print(f"[SafetyTuner] Saved to {path}")

    def merge_and_export(self, output_path: str):
        """合并LoRA权重并导出（推理用）"""
        for lora_layer in self.lora.lora_layers.values():
            lora_layer.merge_weights()

        # 保存合并后的模型
        torch.save(self.model.state_dict(), output_path)
        print(f"[SafetyTuner] Merged and exported to {output_path}")


# =============================================================================
# 数据集创建工具
# =============================================================================

def create_safety_dataset(
    language: str = "both"
) -> List[SafetyDataSample]:
    """
    创建安全微调数据集

    Args:
        language: "chinese", "english", 或 "both"

    Returns:
        安全数据样本列表
    """
    dataset = []

    if language in ["chinese", "both"]:
        dataset.extend([
            # 色情/暴露
            SafetyDataSample(
                prompt="一张照片",
                is_safe=True,
                chosen_response="一张穿着得体衣服的人像照片",
                rejected_response="一张裸体照片",
                risk_level=0.9
            ),
            # 暴力
            SafetyDataSample(
                prompt="一个人",
                is_safe=True,
                chosen_response="一个和平地站着的人",
                rejected_response="一个手持武器的人",
                risk_level=0.8
            ),
            # 血腥
            SafetyDataSample(
                prompt="场景描写",
                is_safe=True,
                chosen_response="阳光明媚的草地场景",
                rejected_response="鲜血淋漓的战场场景",
                risk_level=0.8
            ),
        ])

    if language in ["english", "both"]:
        dataset.extend([
            # 色情/暴露
            SafetyDataSample(
                prompt="a person",
                is_safe=True,
                chosen_response="a person wearing formal clothes",
                rejected_response="a naked person",
                risk_level=0.9
            ),
            SafetyDataSample(
                prompt="a photo of",
                is_safe=True,
                chosen_response="a photo of a landscape",
                rejected_response="a photo of explicit content",
                risk_level=0.95
            ),
            # 暴力
            SafetyDataSample(
                prompt="a scene",
                is_safe=True,
                chosen_response="a peaceful park scene",
                rejected_response="a violent battlefield scene",
                risk_level=0.8
            ),
        ])

    return dataset


def create_contrastive_dataset(
    concepts: List[str],
    safe_alternatives: Dict[str, str]
) -> List[SafetyDataSample]:
    """
    创建对比数据集

    Args:
        concepts: 风险概念列表
        safe_alternatives: 概念映射 {风险 -> 安全}

    Returns:
        对比数据样本
    """
    dataset = []

    for risk_concept, safe_concept in safe_alternatives.items():
        dataset.append(SafetyDataSample(
            prompt=f"generate an image of {risk_concept}",
            is_safe=False,
            rejected_response=f"image of {risk_concept}",
            risk_level=0.8
        ))
        dataset.append(SafetyDataSample(
            prompt=f"generate an image of {safe_concept}",
            is_safe=True,
            chosen_response=f"image of {safe_concept}",
            risk_level=0.0
        ))

    return dataset


# =============================================================================
# 入口点
# =============================================================================

if __name__ == "__main__":
    print("DPO + LoRA Safety Fine-tuning for HunyuanImage 3.0")
    print("=" * 60)
    print()
    print("使用说明:")
    print("  1. 导入本模块")
    print("  2. 配置DPOConfig")
    print("  3. 初始化HunyuanImage3SafetyTuner")
    print("  4. 应用LoRA并训练")
    print()
    print("代码示例:")
    print("""
    import sys
    sys.path.insert(0, '/path/to/')
    import dpo_lora_safety

    config = dpo_lora_safety.DPOConfig(
        learning_rate=1e-4,
        lora_rank=16,
        lora_alpha=32,
        enable_moe_intervention=True,
        moe_intervention_strength=0.3
    )

    tuner = dpo_lora_safety.HunyuanImage3SafetyTuner(
        model=hunyuan_model,
        ref_model=hunyuan_model_ref,
        tokenizer=tokenizer,
        config=config
    )

    tuner.apply_lora()
    dataset = dpo_lora_safety.create_safety_dataset(language='both')
    tuner.train(dataset)
    tuner.save('hunyuan3_safe_lora.pt')
    """)
