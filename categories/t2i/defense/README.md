# 🎨 文生图 - 防御类

文生图模型的安全过滤器、版权保护、概念擦除等防御研究。

## 📋 论文列表

### 🆕 2025 最新防御研究

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **SPEED** | 2025 | arXiv | 可扩展、精确、高效的概念擦除 | [📄](./papers/2503.07392_speed.md) |
| **TRCE** | 2025 | ICCV | 可靠的恶意概念擦除 | [📄](./papers/2503.07389_trce.md) |
| **Concept Pinpoint Eraser** | 2025 | ICLR | 残差注意力门的精准概念擦除 | [📄](./papers/2506.22806_concept_pinpoint_eraser.md) |
| **SafeGuider** | 2025 | ACM CCS | 鲁棒实用的内容安全控制 | [📄](./papers/2510.05173_safeguider.md) |
| **PromptGuard** | 2025 | arXiv | 软提示引导的不安全内容审核 | [📄](./papers/2501.03544_promptguard.md) |
| **Concept Corrector** | 2025 | arXiv | 即时概念擦除框架 | [📄](./papers/2502.16368_concept_corrector.md) |
| **SAeUron** | 2025 | arXiv | 稀疏自编码器实现可解释概念遗忘 | [📄](./papers/2501.18052_saeuron.md) |

### 🔒 概念擦除 (Concept Erasure)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **ESD** | 2023 | ICCV | 从扩散模型中擦除概念 | - |
| **Concept Ablation** | 2023 | ICCV | T2I扩散模型的概念消融 | - |
| **Unified Concept Editing** | 2024 | WACV | 统一的扩散模型概念编辑 | - |
| **R.A.C.E.** | 2024 | ECCV | 鲁棒对抗概念擦除 | - |
| **Receler** | 2024 | ECCV | 轻量级可靠概念擦除 | - |
| **SafeGen** | 2024 | ACM CCS | 缓解不安全性内容生成 | - |
| **Forget-Me-Not** | 2024 | CVPRW | 遗忘学习框架 | - |
| **Forget-FL** | 2024 | NeurIPS | 利用灾难性遗忘开发安全扩散模型 | - |
| **AntiRed** | 2024 | NeurIPS | 对抗重学习攻击的遗忘 | - |

### 🛡️ 安全过滤 (Safety Filtering)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **Latent Guard** | 2024 | ECCV | T2I安全的潜在空间防护框架 | - |
| **GuardT2I** | 2024 | NeurIPS | 对抗提示防御 | - |
| **Safe Latent Diffusion** | 2023 | CVPR | 缓解不当内容生成 | - |
| **SEGA** | 2023 | NeurIPS | 语义引导的T2I生成 | - |
| **SafetyDPO** | 2024 | arXiv | T2I生成的安全对齐 | - |
| **PromptOptimizer** | 2024 | NAACL | 安全T2I的统一提示优化 | - |
| **SAFREE** | 2025 | ICLR | 无训练自适应安全守卫 | - |

### 💧 水印保护 (Watermarking)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **Watermarking Diffusion** | 2023 | arXiv | 扩散模型水印保护 | [📄](../i2i/papers/2305.12502_watermarking_diffusion.md) |
| **Stable Signature** | 2023 | ICCV | 图像水印与模型签名 | - |

### 📊 后门检测 (Backdoor Detection)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **DAA** | 2025 | TPAMI | 动态注意力分析后门检测 | [📄](./papers/2504.20518_dynamic_attention_backdoor.md) |
| **T2I-Backdoor-Defense** | 2024 | ECCVW | 文本扰动防御后门攻击 | - |

---

## 📊 防御方法分类

### 训练时防御 (Training-time)
- 概念擦除
- 安全对齐微调
- 对抗训练

### 推理时防御 (Inference-time)
- 输入过滤
- 输出检测
- 提示重写

### 模型级防御 (Model-level)
- 安全架构设计
- 水印嵌入
- 权限控制

---

## 🔬 关键评估指标

| 指标 | 描述 |
|------|------|
| 概念擦除率 | 目标概念被移除的程度 |
| 效用保持率 | 正常功能保留程度 |
| 鲁棒性 | 对对抗攻击的抵抗能力 |
| 计算开销 | 防御带来的延迟 |

---

[← 返回文生图目录](../README.md) | [← 返回主目录](../../README.md)
