# 🎨 文生图 - 防御类

文生图模型的安全过滤器、版权保护、概念擦除等防御研究。

## 📋 论文列表

### 🆕 2025 最新防御研究

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **SPEED** | 2025 | arXiv | 可扩展、精确、高效的概念擦除 | [📄](../papers/2503.07392_speed.md) |
| **TRCE** | 2025 | ICCV | 可靠的恶意概念擦除 | [📄](../papers/2503.07389_trce.md) |
| **Concept Pinpoint Eraser** | 2025 | ICLR | 残差注意力门的精准概念擦除 | [📄](../papers/2506.22806_concept_pinpoint_eraser.md) |
| **SafeGuider** | 2025 | ACM CCS | 鲁棒实用的内容安全控制 | [📄](../papers/2510.05173_safeguider.md) |
| **PromptGuard** | 2025 | arXiv | 软提示引导的不安全内容审核 | [📄](../papers/2501.03544_promptguard.md) |
| **Concept Corrector** | 2025 | arXiv | 即时概念擦除框架 | [📄](../papers/2502.16368_concept_corrector.md) |
| **SAeUron** | 2025 | arXiv | 稀疏自编码器实现可解释概念遗忘 | [📄](../papers/2501.18052_saeuron.md) |

### 🔒 概念擦除 (Concept Erasure)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **ESD** | 2023 | ICCV | 从扩散模型中擦除概念（永久擦除，非推理时修改） | [📄](../papers/2303.07345_esd.md) |
| **Concept Ablation** | 2023 | ICCV | CLIP空间对齐的概念消融方法 | [📄](../papers/2303.13516_concept_ablation.md) |
| **UCE** | 2024 | WACV | 统一概念编辑，支持并发去偏/风格擦除/内容审核 | [📄](../papers/2308.14761_uce.md) |
| **R.A.C.E.** | 2024 | ECCV | 鲁棒对抗概念擦除，降低ASR 30个百分点 | [📄](../papers/2405.16341_race.md) |
| **Receler** | 2024 | ECCV | 轻量级可靠概念擦除，3秒完成 | [📄](../papers/2407.12383_receler.md) |
| **SafeGen** | 2024 | ACM CCS | 文本无关的NSFW内容缓解，99.4%移除率 | [📄](../papers/2404.06666_safegen.md) |
| **Forget-Me-Not** | 2024 | CVPRW | 遗忘学习框架，M-Score评估 | [📄](../papers/2303.17591_forget_me_not.md) |
| **Safe Latent Diffusion** | 2023 | CVPR | 潜在空间安全干预，无需训练 | [📄](../papers/2211.05105_sld.md) |

### 🛡️ 安全过滤 (Safety Filtering)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **Latent Guard** | 2024 | ECCV | T2I安全的潜在空间防护框架，LLM辅助数据生成 | [📄](../papers/2404.08031_latent_guard.md) |
| **GuardT2I** | 2024 | NeurIPS | 对抗提示防御，优于OpenAI-Moderation | [📄](../papers/2403.01446_guardt2i.md) |
| **SEGA** | 2023 | NeurIPS | 语义引导的T2I生成控制 | [📄](../papers/2301.12247_sega.md) |
| **Stable Signature** | 2023 | ICCV | 图像水印与模型签名（Facebook） | [📄](../papers/2303.15435_stable_signature.md) |

### 📊 后门检测 (Backdoor Detection)

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **DAA** | 2025 | TPAMI | 动态注意力分析后门检测 | [📄](../papers/2504.20518_dynamic_attention_backdoor.md) |
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

[← 返回文生图目录](../README.md) | [← 返回主目录](../../../README.md)
