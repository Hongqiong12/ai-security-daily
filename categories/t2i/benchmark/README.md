# 🎨 文生图 - 基础综述

文本到图像生成的基础综述论文、安全评测基准。

## 📋 论文列表

### 📖 综述论文

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| **Generative AI in Vision** | 2024 | arXiv | 生成式AI视觉综述，涵盖扩散模型在T2I中的核心技术 | [📄](../i2i/papers/2402.16369_generative_ai_in_vision.md) |
| **FRAP** | 2024 | arXiv | 自适应提示权重改善文本-图像对齐 | [📄](./papers/2408.11706_frap.md) |
| **Adversarial T2I Survey** | 2021 | arXiv | GAN时代文生图综述，梳理Text-to-Image发展脉络 | [📄](./papers/1910.09399_adversarial_t2i_survey.md) |

### 📊 安全评测基准

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| **Adversarial T2I Synthesis** | 2019 | arXiv | GAN时代文生图攻击综述，奠定安全研究基础 | [📄](./papers/1910.09399_adversarial_t2i_survey.md) |
| **JailbreakBench** | 2024 | NeurIPS | T2I越狱攻击标准化评测基准，100种行为数据集 | [📄](./papers/2404.01318_jailbreakbench.md) |
| **SafetyBench** | 2024 | arXiv | T2I安全对齐多维评测 | - |

### 🔬 经典基础论文

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| **DALL-E** | 2021 | - | 开创性T2I模型 | - |
| **DALL-E 2** | 2022 | - | CLIP引导的T2I生成 | - |
| **Stable Diffusion** | 2022 | - | 开源T2I扩散模型 | - |
| **SDXL** | 2023 | - | 高分辨率T2I模型 | - |
| **DALL-E 3** | 2023 | - | 改进文本理解的T2I模型 | - |

---

## 📚 技术发展脉络

```
2015-2020: GAN时代
├── Text-to-Image GAN (Reed et al.)
├── AttnGAN
└── DM-GAN

2021-2022: Transformer时代
├── DALL-E (OpenAI)
├── CLIP引导生成
└── Latent Diffusion (Stable Diffusion)

2023-至今: 大模型时代
├── DALL-E 3
├── SDXL
├── Imagen
└── Midjourney v6
```

---

## 🛡️ 安全研究基础

- 扩散模型架构理解
- 交叉注意力机制分析
- 文本编码器安全分析
- 生成内容安全评估

---

[← 返回文生图目录](../README.md) | [← 返回主目录](../../README.md)
