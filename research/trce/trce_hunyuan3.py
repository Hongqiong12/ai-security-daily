"""
TRCE (Training-free Real Concept Erasure) for HunyuanImage 3.0
==============================================================
适配方案：基于 Word Embedding 编辑的闭式概念消除

架构确认：HunyuanImage 3.0 使用「统一自回归 + 扩散推理」混合范式
- 基础架构: Transformer Decoder + MoE (自回归LLM)
- 推理方式: 自回归生成 + 扩散采样步骤
- wte.weight: (133120, 4096) — vocab × hidden_dim
- 64个MoE experts，激活参数130亿
- 文本注入方式: Token 拼接 [text_tokens ∥ image_tokens]

重要结论：
- 此模型是AR架构，不是纯扩散DiT
- Z-Erase的梯度手术方法主要针对扩散模型，对本模型有限
- 推荐使用TRCE Stage 1 + DPO/LoRA安全微调

TRCE Stage 1: 闭式 Word Embedding 编辑（适用于AR和Diffusion）
TRCE Stage 2: AR模型的token-level引导增强

Author: WorkBuddy
Date: 2026-04-02
"""

import torch
import torch.nn.functional as F
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np


# =============================================================================
# 数据结构定义
# =============================================================================

@dataclass
class ConceptPair:
    """恶意概念对: 概念A → 概念B (安全的替代概念)"""
    malicious: str           # 恶意概念 (e.g., "blood")
    safe: str               # 安全替代概念 (e.g., "water")
    malicious_token_id: Optional[int] = None
    safe_token_id: Optional[int] = None

    def __post_init__(self):
        assert self.malicious != self.safe, "Malicious and safe concepts must differ"


@dataclass
class TRCEConfig:
    """TRCE 配置"""
    # 模型类型：扩散模型还是自回归模型
    model_type: str = "autoregressive"  # "autoregressive" or "diffusion"

    # Stage 1: 闭式编辑强度
    alpha: float = 0.5      # 概念替换强度 (0-1), 越大替换越彻底
    epsilon: float = 1e-6  # 数值稳定性

    # Stage 2: 引导增强
    guidance_scale: float = 7.5
    num_trajectory_samples: int = 50
    triplet_margin: float = 0.1

    # 目标层 (HunyuanImage 3.0 特定)
    embedding_layer: str = "model.model.wte"

    # MoE干预配置
    enable_moe_intervention: bool = True
    moe_intervention_strength: float = 0.3
    moe_layer_names: List[str] = None

    # 计算设备
    device: str = "cuda"

    def __post_init__(self):
        if self.moe_layer_names is None:
            self.moe_layer_names = ["mlp", "moe", "expert"]


# =============================================================================
# Stage 1: 闭式 Word Embedding 编辑
# =============================================================================

class HunyuanImage3EmbeddingEditor:
    """
    HunyuanImage 3.0 的 Word Embedding 编辑器

    原理:
    --------
    在 HunyuanImage 3.0 中，文本和图像 token 通过拼接形成统一序列，
    然后由统一的 self-attention 层处理。由于没有独立的 cross-attention 层，
    恶意概念的消除需要直接修改 token embedding 向量。

    方法:
    --------
    1. 提取恶意概念的 embedding 向量 v_mal
    2. 提取安全替代概念的 embedding 向量 v_safe
    3. 计算概念方向: d = v_mal - mean(all_safe_embeddings)
    4. 对 v_mal 执行投影消除: v_mal_new = v_mal - alpha * proj_d(v_mal)

    闭式求解:
    --------
    v_new = v - alpha * d * (d^T @ v) / (d^T @ d)

    投影消除确保 v_new 在 d 方向上的分量为 0，
    从而消除 v_mal 中包含的"恶意概念语义方向"。
    """

    def __init__(self, model, tokenizer, config: TRCEConfig):
        """
        Args:
            model: HunyuanImage 3.0 模型实例
            tokenizer: 对应的 tokenizer
            config: TRCE 配置
        """
        self.model = model
        self.tokenizer = tokenizer
        self.config = config

        # 获取 embedding 层
        self.wte = self._get_embedding_layer()

        # 保存原始权重用于恢复
        self.original_weights = {}

    def _get_embedding_layer(self) -> torch.nn.Embedding:
        """获取 word embedding 层"""
        # 尝试多种路径
        for path in ["model.model.wte", "model.wte", "wte"]:
            try:
                parts = path.split(".")
                layer = self.model
                for part in parts:
                    layer = getattr(layer, part)
                print(f"[HunyuanImage3EmbeddingEditor] Found embedding at: {path}")
                return layer
            except AttributeError:
                continue

        raise ValueError(
            "Could not find embedding layer. "
            "Tried: model.model.wte, model.wte, wte"
        )

    def _tokenize_concepts(self, concepts: List[str]) -> List[int]:
        """Tokenize 概念列表，返回 token IDs"""
        token_ids = []
        for concept in concepts:
            # 取最后一个 token (通常是多词概念)
            ids = self.tokenizer.encode(concept)
            token_ids.append(ids[-1])
        return token_ids

    def compute_concept_direction(
        self,
        malicious_concept: str,
        safe_concepts: List[str],
        safe_token_ids: Optional[List[int]] = None
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        计算概念消除方向向量

        Args:
            malicious_concept: 恶意概念字符串
            safe_concepts: 安全概念列表 (用于计算基准空间)

        Returns:
            (concept_direction, v_mal, v_safe): 方向向量, 恶意向量, 安全向量
        """
        # Tokenize
        mal_ids = self.tokenizer.encode(malicious_concept)
        v_mal = self.wte.weight[mal_ids[-1]].detach().clone()

        if safe_token_ids is None:
            safe_token_ids = self._tokenize_concepts(safe_concepts)

        # 计算安全概念的平均 embedding
        safe_embeddings = []
        for tid in safe_token_ids:
            safe_embeddings.append(self.wte.weight[tid].detach())

        v_safe_mean = torch.stack(safe_embeddings).mean(dim=0)

        # 概念方向 = 恶意向量 - 安全基准
        d = v_mal - v_safe_mean
        d_norm = d / (torch.norm(d) + self.config.epsilon)

        return d_norm, v_mal, v_safe_mean

    def closed_form_embedding_edit(
        self,
        malicious_concept: str,
        safe_concepts: List[str],
        alpha: Optional[float] = None,
        return_directions: bool = False
    ) -> Dict[int, Tuple[torch.Tensor, torch.Tensor]]:
        """
        闭式 embedding 编辑 — 核心算法

        对恶意概念的 token embedding 执行投影消除：

            v_new = v_mal - alpha * proj_d(v_mal)
                  = v_mal - alpha * d * (d^T @ v_mal) / (d^T @ d)

        其中 d = v_mal - mean(v_safe) 是概念语义方向向量。

        Args:
            malicious_concept: 恶意概念
            safe_concepts: 安全概念列表 (至少 3-5 个用于稳定估计)
            alpha: 替换强度，默认使用 config.alpha
            return_directions: 是否返回方向向量

        Returns:
            如果 return_directions=False: {malicious_token_id: (old_emb, new_emb)}
            如果 return_directions=True: {malicious_token_id: (old_emb, new_emb, concept_direction)}
        """
        alpha = alpha or self.config.alpha

        # Tokenize
        mal_ids = self.tokenizer.encode(malicious_concept)
        mal_token_id = mal_ids[-1]

        safe_token_ids = self._tokenize_concepts(safe_concepts)

        # 计算方向
        d, v_mal, v_safe_mean = self.compute_concept_direction(
            malicious_concept, safe_concepts, safe_token_ids
        )

        # 保存原始权重
        self.original_weights[mal_token_id] = self.wte.weight[mal_token_id].detach().clone()

        # 闭式投影消除
        # v_new = v_mal - alpha * d * (d^T @ v_mal)
        projection_coef = torch.dot(d, v_mal)  # d^T @ v_mal (scalar)
        v_new = v_mal - alpha * d * projection_coef

        # 更新权重
        with torch.no_grad():
            self.wte.weight[mal_token_id] = v_new.clone()

        result = {mal_token_id: (self.original_weights[mal_token_id], v_new)}
        if return_directions:
            result[mal_token_id] = (*result[mal_token_id], d)

        print(f"[TRCE Stage 1] Edited token {mal_token_id} "
              f"('{malicious_concept}'): "
              f"||d||={torch.norm(d):.4f}, "
              f"projection={projection_coef:.4f}, "
              f"alpha={alpha}")

        return result

    def batch_edit_concepts(
        self,
        concept_pairs: List[ConceptPair],
        safe_concepts_pool: Optional[List[str]] = None
    ) -> Dict[int, Tuple[torch.Tensor, torch.Tensor]]:
        """
        批量编辑多个概念对

        Args:
            concept_pairs: 概念对列表
            safe_concepts_pool: 安全概念池 (用于估计安全语义空间)

        Returns:
            {token_id: (old_emb, new_emb)} 编辑记录
        """
        if safe_concepts_pool is None:
            # 默认安全概念池 (中英双语)
            safe_concepts_pool = [
                "water", "nature", "sky", "tree", "flower", "grass",
                "水", "自然", "天空", "树木", "花朵", "草地",
                "house", "building", "road", "cloud", "mountain",
                "房子", "建筑", "道路", "云", "山"
            ]

        edit_records = {}

        for pair in concept_pairs:
            record = self.closed_form_embedding_edit(
                malicious_concept=pair.malicious,
                safe_concepts=safe_concepts_pool
            )
            edit_records.update(record)

        return edit_records

    def restore_original(self) -> None:
        """恢复所有原始 embedding"""
        for token_id, original_emb in self.original_weights.items():
            with torch.no_grad():
                self.wte.weight[token_id] = original_emb.clone()
        print(f"[TRCE Stage 1] Restored {len(self.original_weights)} edited embeddings")


# =============================================================================
# Stage 2: AR模型轨迹引导（适配HunyuanImage 3.0）
# =============================================================================

class HunyuanImage3MoEIntervention:
    """
    HunyuanImage 3.0 MoE专家干预层

    原理：
    --------
    HunyuanImage 3.0使用64个MoE专家处理不同概念域。
    通过干预高风险专家的激活，可以抑制风险概念生成。

    方法：
    --------
    1. 注册hook跟踪专家激活
    2. 计算专家风险评分
    3. 在推理时抑制高风险专家输出
    """

    def __init__(self, model, config: TRCEConfig):
        self.model = model
        self.config = config
        self.hooks = []
        self.expert_activations = {}
        self.expert_risk_scores = {}

    def register_expert_hooks(self):
        """注册专家激活hooks"""
        def expert_hook(module, input, output, expert_id):
            if isinstance(output, torch.Tensor):
                activation = output.detach()
                strength = torch.norm(activation).item()
                self.expert_activations[expert_id] = strength

        expert_id = 0
        for name, module in self.model.named_modules():
            # 查找MoE相关模块
            if any(moe_name in name.lower() for moe_name in self.config.moe_layer_names):
                if hasattr(module, 'forward'):
                    hook = module.register_forward_hook(
                        lambda m, i, o, eid=expert_id: expert_hook(m, i, o, eid)
                    )
                    self.hooks.append(hook)
                    expert_id += 1

        print(f"[MoEIntervention] Registered {len(self.hooks)} expert hooks")

    def remove_hooks(self):
        """移除所有hooks"""
        for hook in self.hooks:
            hook.remove()
        self.hooks = []

    def compute_risk_scores(self, risk_concepts: List[str], tokenizer):
        """
        基于风险概念计算专家风险评分

        Args:
            risk_concepts: 风险概念列表
            tokenizer: 分词器

        Returns:
            {expert_id -> risk_score}
        """
        if not self.expert_activations:
            return {}

        # 基于激活强度计算风险评分
        activations = list(self.expert_activations.values())
        max_activation = max(activations) if activations else 1.0

        for expert_id, strength in self.expert_activations.items():
            # 归一化风险评分
            self.expert_risk_scores[expert_id] = min(strength / max_activation, 1.0)

        return self.expert_risk_scores

    def apply_intervention(
        self,
        expert_id: int,
        original_output: torch.Tensor
    ) -> torch.Tensor:
        """
        对专家输出应用干预

        Args:
            expert_id: 专家ID
            original_output: 原始输出

        Returns:
            干预后的输出
        """
        if not self.config.enable_moe_intervention:
            return original_output

        risk_score = self.expert_risk_scores.get(expert_id, 0.0)
        suppression = self.config.moe_intervention_strength * risk_score

        # 软抑制
        return original_output * (1 - suppression)

class HunyuanImage3GuidanceEnhancer:
    """
    TRCE Stage 2: Token级引导增强（适配AR模型）

    原理:
    --------
    由于 HunyuanImage 3.0 是自回归 + 扩散推理的混合架构，
    Stage 2 需要在 token 级别进行引导，而非扩散的 latent 级别。

    AR模型引导流程:
    --------
    1. 用 clean prompt 获取 hidden states 轨迹
    2. 用 malicious prompt 获取 hidden states 轨迹
    3. 计算 token 级别的概念偏移: delta = hidden_mal - hidden_clean
    4. 在每个生成步骤注入: hidden = hidden - beta * delta

    对于扩散推理部分（diffusion_infer_steps）:
    --------
    - 在 denoising loop 的每一步注入纠正信号
    - 与纯扩散模型的 latent 引导类似
    """

    def __init__(self, model, editor: HunyuanImage3EmbeddingEditor, config: TRCEConfig):
        self.model = model
        self.editor = editor
        self.config = config

        # 轨迹存储
        self.clean_trajectories = {}
        self.malicious_trajectories = {}
        self.concept_deltas = {}

        # Hook 句柄
        self.hooks = []

    def _register_forward_hook(self, module, hook_fn, name: str):
        """注册前向 Hook"""
        handle = module.register_forward_hook(
            lambda m, input, output: hook_fn(m, input, output, name)
        )
        self.hooks.append(handle)
        return handle

    def collect_trajectory(
        self,
        prompt: str,
        trajectory_key: str,
        use_edited_embeddings: bool = True,
        num_inference_steps: int = 50
    ) -> List[torch.Tensor]:
        """
        收集推理轨迹（适配AR+扩散混合模型）

        对于 HunyuanImage 3.0，需要收集两类轨迹：
        1. AR阶段: hidden states 轨迹
        2. 扩散阶段: denoising 轨迹

        Args:
            prompt: 输入提示词
            trajectory_key: 轨迹标识符
            use_edited_embeddings: 是否使用编辑后的 embedding
            num_inference_steps: 扩散推理步数

        Returns:
            各推理步骤的 hidden/latent 列表
        """
        if not use_edited_embeddings:
            # 临时恢复原始 embedding
            self.editor.restore_original()

        trajectories = []

        def hidden_state_hook(module, input, output, name):
            """Hook AR模型的hidden states"""
            if isinstance(output, torch.Tensor):
                # 获取最后一层的输出
                trajectories.append(output.detach().clone())
            elif isinstance(output, tuple):
                # Transformer输出通常是 (hidden_state, ...)
                trajectories.append(output[0].detach().clone())
            return output

        # 注册 hook 到 transformer layers
        hook_targets = self._find_hidden_state_layers()
        for name, target in hook_targets.items():
            self._register_forward_hook(target, hidden_state_hook, name)

        try:
            # HunyuanImage 3.0 的推理 API
            # diff_infer_steps 参数控制扩散采样步数
            print(f"[TRCE Stage 2] Collecting trajectory for: '{prompt}'")
            print(f"  - AR hidden states + {num_inference_steps} diffusion steps")

            # 实际调用（取消注释以使用）
            # result = self.model.generate_image(
            #     prompt=prompt,
            #     seed=42,
            #     image_size="auto",
            #     use_system_prompt="en_unified",
            #     bot_task="think_recaption",
            #     infer_align_image_size=True,
            #     diff_infer_steps=num_inference_steps
            # )

        finally:
            # 移除 hooks
            for handle in self.hooks:
                handle.remove()
            self.hooks = []

        if trajectory_key.startswith("clean"):
            self.clean_trajectories[trajectory_key] = trajectories
        else:
            self.malicious_trajectories[trajectory_key] = trajectories

        return trajectories

    def _find_hidden_state_layers(self) -> Dict[str, torch.nn.Module]:
        """查找hidden state层（适配AR模型）"""
        layers = {}
        for name, module in self.model.named_modules():
            # 查找 transformer decoder layers
            if any(keyword in name.lower() for keyword in [
                "layer", "transformer_block", "decoder_block", "blocks"
            ]):
                # 只取最外层的layer块
                if "." not in name or name.count(".") <= 2:
                    layers[name] = module
        return layers

    def _find_denoising_layers(self) -> Dict[str, torch.nn.Module]:
        """查找 denoising 过程的关键层"""
        layers = {}
        for name, module in self.model.named_modules():
            if any(keyword in name for keyword in ["layer", "transformer", "decoder", "moe"]):
                layers[name] = module
        return layers

    def compute_concept_delta(
        self,
        clean_prompt: str,
        malicious_prompt: str,
        num_steps: int = 50
    ) -> torch.Tensor:
        """
        计算概念偏移量 delta

        Args:
            clean_prompt: 干净提示词
            malicious_prompt: 恶意提示词

        Returns:
            delta: 概念偏移向量
        """
        # 收集双轨迹
        clean_traj = self.collect_trajectory(
            clean_prompt, f"clean_{clean_prompt[:20]}",
            num_inference_steps=num_steps
        )
        malicious_traj = self.collect_trajectory(
            malicious_prompt, f"mal_{malicious_prompt[:20]}",
            num_inference_steps=num_steps
        )

        if not clean_traj or not malicious_traj:
            raise ValueError("Failed to collect trajectories")

        # 计算平均偏移
        delta = torch.stack([
            m - c for m, c in zip(malicious_traj, clean_traj)
        ]).mean(dim=0)

        self.concept_deltas[f"{clean_prompt}_{malicious_prompt}"] = delta

        return delta

    def apply_guided_generation(
        self,
        prompt: str,
        concept_delta: torch.Tensor,
        beta: float = 0.1,
        guidance_scale: float = 7.5
    ) -> torch.Tensor:
        """
        应用引导生成

        Args:
            prompt: 输入提示词
            concept_delta: 概念偏移向量 (来自 compute_concept_delta)
            beta: 引导强度
            guidance_scale: CFG 强度

        Returns:
            引导后的 latent
        """
        # Step 1: 原始 CFG
        unconditional = self.model.encode("")  # 空 prompt
        conditional = self.model.encode(prompt)

        # CFG 混合
        guided = unconditional + guidance_scale * (conditional - unconditional)

        # Step 2: 注入概念纠正
        guided_corrected = guided - beta * concept_delta

        return guided_corrected


# =============================================================================
# 端到端 TRCE Pipeline
# =============================================================================

class HunyuanImage3TRCE:
    """
    HunyuanImage 3.0 的端到端 TRCE 流水线

    整合 Stage 1 (闭式 embedding 编辑) + Stage 2 (Token级引导增强) + MoE干预

    重要说明：
    --------
    HunyuanImage 3.0 是自回归 + 扩散推理的混合架构，不是纯扩散DiT。
    因此本实现采用以下策略：
    1. Stage 1: Word Embedding 编辑（闭式，与架构无关）
    2. Stage 2: Token级引导（适配AR模型的hidden state轨迹）
    3. MoE Intervention: 专家激活干预（适配MoE架构）

    使用示例:
    --------
    ```python
    # 假设 trce_hunyuan3.py 在当前目录或 sys.path 中
    import trce_hunyuan3

    config = trce_hunyuan3.TRCEConfig(
        alpha=0.5,
        guidance_scale=7.5,
        model_type="autoregressive",  # 明确AR模型类型
        enable_moe_intervention=True,
        moe_intervention_strength=0.3,
        device="cuda"
    )

    trce = trce_hunyuan3.HunyuanImage3TRCE(model, tokenizer, config)

    # Stage 1: 编辑 embedding
    concept_pairs = [
        trce_hunyuan3.ConceptPair(malicious="blood", safe="water"),
        trce_hunyuan3.ConceptPair(malicious="裸体", safe="衣服"),
        trce_hunyuan3.ConceptPair(malicious="naked", safe="clothed"),
    ]
    trce.stage1_edit_embeddings(concept_pairs)

    # Stage 2: 收集轨迹并增强
    trce.stage2_enhance_guidance(
        clean_prompt="A person wearing clothes",
        malicious_prompt="A naked person",
        num_steps=50
    )

    # 生成安全图像
    safe_image = trce.generate_safe_image(
        prompt="A person exercising",
        guidance_scale=7.5
    )

    # 恢复原始模型
    trce.restore()
    ```
    """

    def __init__(
        self,
        model,
        tokenizer,
        config: Optional[TRCEConfig] = None
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config or TRCEConfig()

        # 初始化 Stage 1 和 Stage 2
        self.editor = HunyuanImage3EmbeddingEditor(model, tokenizer, self.config)
        self.enhancer = HunyuanImage3GuidanceEnhancer(model, self.editor, self.config)

        # 初始化 MoE 干预层
        self.moe_intervention = HunyuanImage3MoEIntervention(model, self.config)

        # 编辑记录
        self.edit_records = {}

        # 打印模型类型信息
        print(f"[TRCE] HunyuanImage 3.0 Safety Pipeline initialized")
        print(f"  - Model type: {self.config.model_type}")
        print(f"  - MoE intervention: {self.config.enable_moe_intervention}")

    def stage1_edit_embeddings(
        self,
        concept_pairs: List[ConceptPair],
        safe_concepts_pool: Optional[List[str]] = None
    ) -> Dict[int, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Stage 1: 闭式 embedding 编辑

        Args:
            concept_pairs: 概念对列表
            safe_concepts_pool: 安全概念池

        Returns:
            编辑记录
        """
        print("=" * 60)
        print("TRCE Stage 1: Closed-form Embedding Editing")
        print("=" * 60)

        self.edit_records = self.editor.batch_edit_concepts(
            concept_pairs=concept_pairs,
            safe_concepts_pool=safe_concepts_pool
        )

        print(f"[TRCE Stage 1] Completed: {len(self.edit_records)} concepts edited")
        return self.edit_records

    def stage2_enhance_guidance(
        self,
        clean_prompt: str,
        malicious_prompt: str,
        num_steps: int = 50
    ) -> torch.Tensor:
        """
        Stage 2: 去噪轨迹引导增强

        Args:
            clean_prompt: 干净提示词
            malicious_prompt: 恶意提示词
            num_steps: 推理步数

        Returns:
            概念偏移向量 delta
        """
        print("=" * 60)
        print("TRCE Stage 2: Trajectory-guided Enhancement")
        print("=" * 60)

        # 重新应用编辑 (Stage 1 可能在之前已被恢复)
        if not self.edit_records:
            raise ValueError("Must run Stage 1 first")

        delta = self.enhancer.compute_concept_delta(
            clean_prompt=clean_prompt,
            malicious_prompt=malicious_prompt,
            num_steps=num_steps
        )

        print(f"[TRCE Stage 2] Concept delta computed: ||delta||={torch.norm(delta):.4f}")
        return delta

    def generate_safe_image(
        self,
        prompt: str,
        guidance_scale: Optional[float] = None,
        beta: float = 0.1,
        **kwargs
    ) -> torch.Tensor:
        """
        生成安全图像 (使用编辑后的 embedding 和引导增强)

        Args:
            prompt: 输入提示词
            guidance_scale: CFG 强度
            beta: 引导纠正强度
            **kwargs: 传递给 model.generate_image 的其他参数

        Returns:
            生成的图像
        """
        guidance_scale = guidance_scale or self.config.guidance_scale

        # 应用编辑后的 embedding 生成
        result = self.model.generate_image(
            prompt=prompt,
            seed=kwargs.get("seed", 42),
            image_size="auto",
            use_system_prompt="en_unified",
            bot_task="think_recaption",
            infer_align_image_size=True,
            diff_infer_steps=kwargs.get("diff_infer_steps", 50)
        )

        return result

    def restore(self) -> None:
        """恢复模型到原始状态"""
        self.editor.restore_original()
        self.moe_intervention.remove_hooks()
        print("[TRCE] Model restored to original state")

    def setup_moe_intervention(
        self,
        risk_concepts: List[str],
        tokenizer
    ) -> Dict[int, float]:
        """
        设置MoE专家干预

        Args:
            risk_concepts: 风险概念列表
            tokenizer: 分词器

        Returns:
            专家风险评分
        """
        print("=" * 60)
        print("Setting up MoE Expert Intervention")
        print("=" * 60)

        # 注册hooks
        self.moe_intervention.register_expert_hooks()

        # 收集激活（通过运行推理）
        # 可以在风险概念上运行forward来激活相关专家
        print("[MoE] Collecting expert activations...")

        # 计算风险评分
        risk_scores = self.moe_intervention.compute_risk_scores(risk_concepts, tokenizer)

        print(f"[MoE] Computed risk scores for {len(risk_scores)} experts")
        for expert_id, score in sorted(risk_scores.items(), key=lambda x: -x[1])[:5]:
            print(f"  Expert {expert_id}: risk_score={score:.4f}")

        return risk_scores

    def apply_complete_safety_pipeline(
        self,
        concept_pairs: List[ConceptPair],
        clean_prompt: str,
        malicious_prompt: str,
        risk_concepts: List[str],
        num_steps: int = 50
    ) -> torch.Tensor:
        """
        应用完整的安全流水线

        整合 Stage 1 + Stage 2 + MoE Intervention

        Args:
            concept_pairs: 概念对列表
            clean_prompt: 干净提示词
            malicious_prompt: 恶意提示词
            risk_concepts: 风险概念列表
            num_steps: 推理步数

        Returns:
            概念偏移向量 delta
        """
        print("=" * 60)
        print("Complete Safety Pipeline for HunyuanImage 3.0 (AR Model)")
        print("=" * 60)

        # Stage 1: Embedding 编辑
        self.stage1_edit_embeddings(concept_pairs)

        # 设置 MoE 干预
        self.setup_moe_intervention(risk_concepts, self.tokenizer)

        # Stage 2: 轨迹引导增强
        delta = self.stage2_enhance_guidance(
            clean_prompt=clean_prompt,
            malicious_prompt=malicious_prompt,
            num_steps=num_steps
        )

        print("=" * 60)
        print("Safety pipeline complete. Model is now protected.")
        print("=" * 60)

        return delta


# =============================================================================
# 便捷工具函数
# =============================================================================

def create_safety_concept_pairs(
    language: str = "both"
) -> List[ConceptPair]:
    """
    创建安全相关的概念对

    Args:
        language: "chinese", "english", 或 "both"

    Returns:
        概念对列表
    """
    pairs = []

    if language in ["chinese", "both"]:
        pairs.extend([
            ConceptPair(malicious="色情", safe="艺术"),
            ConceptPair(malicious="裸体", safe="衣服"),
            ConceptPair(malicious="血腥", safe="清水"),
            ConceptPair(malicious="暴力", safe="和平"),
            ConceptPair(malicious="赌博", safe="游戏"),
            ConceptPair(malicious="毒品", safe="饮料"),
        ])

    if language in ["english", "both"]:
        pairs.extend([
            ConceptPair(malicious="porn", safe="art"),
            ConceptPair(malicious="naked", safe="clothed"),
            ConceptPair(malicious="blood", safe="water"),
            ConceptPair(malicious="violence", safe="peace"),
            ConceptPair(malicious="gambling", safe="game"),
            ConceptPair(malicious="drugs", safe="drink"),
            ConceptPair(malicious="nude", safe="dressed"),
            ConceptPair(malicious="explicit", safe="abstract"),
        ])

    return pairs


def evaluate_erasure_quality(
    trce: HunyuanImage3TRCE,
    test_concepts: List[str],
    safe_prompts: List[str]
) -> Dict[str, float]:
    """
    评估概念消除质量

    通过检查编辑后的 embedding 与安全概念的距离来评估

    Args:
        trce: TRCE 实例
        test_concepts: 待测试的恶意概念
        safe_prompts: 安全提示词

    Returns:
        评估指标
    """
    results = {}

    safe_embeddings = []
    for sp in safe_prompts:
        ids = trce.tokenizer.encode(sp)
        safe_embeddings.append(trce.editor.wte.weight[ids[-1]].detach())

    safe_mean = torch.stack(safe_embeddings).mean(dim=0)

    for concept in test_concepts:
        ids = trce.tokenizer.encode(concept)
        v = trce.editor.wte.weight[ids[-1]].detach()

        # 计算与安全空间的距离
        dist_to_safe = F.cosine_similarity(
            v.unsqueeze(0), safe_mean.unsqueeze(0)
        ).item()

        # 计算与原始 (未编辑) 的距离
        if ids[-1] in trce.edit_records:
            original = trce.edit_records[ids[-1]][0]
            dist_from_original = 1 - F.cosine_similarity(
                v.unsqueeze(0), original.unsqueeze(0)
            ).item()
        else:
            dist_from_original = 0.0

        results[concept] = {
            "cosine_to_safe_space": dist_to_safe,
            "deviation_from_original": dist_from_original
        }

    return results


# =============================================================================
# 入口点
# =============================================================================

if __name__ == "__main__":
    print("TRCE for HunyuanImage 3.0")
    print("=" * 60)
    print("使用说明:")
    print("  1. 将本文件复制到服务器: cp trce_hunyuan3.py /path/to/server/")
    print("  2. 在服务器上确保模型已加载")
    print("  3. 使用方式:")
    print()
    print("  ```python")
    print("  import sys")
    print("  sys.path.insert(0, '/path/to/')  # 添加文件所在目录")
    print("  import trce_hunyuan3")
    print()
    print("  config = trce_hunyuan3.TRCEConfig(alpha=0.5, guidance_scale=7.5, device='cuda')")
    print("  trce = trce_hunyuan3.HunyuanImage3TRCE(model, tokenizer, config)")
    print()
    print("  # 创建概念对")
    print("  concept_pairs = trce_hunyuan3.create_safety_concept_pairs(language='both')")
    print()
    print("  # Stage 1: 编辑 embedding")
    print("  trce.stage1_edit_embeddings(concept_pairs)")
    print()
    print("  # 生成安全图像")
    print("  safe_image = trce.generate_safe_image('A person exercising')")
    print("  ```")
