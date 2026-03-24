# AI Security Daily Intelligence

<p align="center">
  <img src="assets/logo.png" alt="AI Security Daily" width="200"/>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-100+-green.svg">
    <img src="https://img.shields.io/badge/Papers-100+-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--03--23-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--03--23-orange.svg" alt="Last Update"/>
  </a>
</p>

> 每日 AI 安全论文深度情报调研，自动追踪 ArXiv 最新论文，按模态类型分类整理

---

## Table of Contents

- [📖 Overview](#-overview)
- [🖼️ Image-to-Image (i2i)](#-image-to-image-i2i)
- [🎬 Image-to-Video (i2v)](#-image-to-video-i2v)
- [📝 Text-to-Text (t2t)](#-text-to-text-t2t)
- [🎨 Text-to-Image (t2i)](#-text-to-image-t2i)
- [📖 Image-to-Text (i2t)](#-image-to-text-i2t)
- [🎥 Text-to-Video (t2v)](#-text-to-video-t2v)
- [📋 Daily Reports](#-daily-reports)
- [🤖 Automation](#-automation)

---

## 📖 Overview

本项目系统性地追踪和整理 AI 安全领域的研究论文，覆盖 6 种核心模态转换类型：

| 模态 | 英文名称 | 中文名称 | 论文数 |
|------|----------|----------|--------|
| i2i | Image-to-Image | 图生图 | 15+ 篇 |
| i2v | Image-to-Video | 图生视频 | 12+ 篇 |
| t2t | Text-to-Text | 文生文 | 15+ 篇 |
| t2i | Text-to-Image | 文生图 | 55+ 篇 |
| i2t | Image-to-Text | 图生文 | 10+ 篇 |
| t2v | Text-to-Video | 文生视频 | 8+ 篇 |

### 分类体系

每个模态下包含三个子类别：

- **Benchmark**: 基础评测集、基准测试论文
- **Attack**: 攻击类论文（对抗攻击、越狱攻击、后门攻击等）
- **Defense**: 防御类论文（安全对齐、鲁棒性防御等）

---

## 🖼️ Image-to-Image (i2i)

图生图生成模型的安全研究，包括图像翻译、风格迁移、图像编辑等任务。

### 📊 Benchmark

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| [Generative AI in Vision](./categories/i2i/papers/2402.16369_generative_ai_in_vision.md) | 2024 | arXiv | 生成式AI视觉综述，覆盖扩散模型、GAN等 | [📄](./categories/i2i/papers/2402.16369_generative_ai_in_vision.md) |
| [Watermarking Diffusion Model](./categories/i2i/papers/2305.12502_watermarking_diffusion.md) | 2023 | arXiv | 首个DM水印方案 | [📄](./categories/i2i/papers/2305.12502_watermarking_diffusion.md) |
| [Pix2Pix](./categories/i2i/papers/1611.07004_pix2pix.md) | 2017 | CVPR | 图像翻译奠基性论文，CGAN经典应用 | [📄](./categories/i2i/papers/1611.07004_pix2pix.md) |

### 🔴 Attack

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| Adv-Diffusion | - | - | 基于潜在扩散模型的不可感知对抗人脸身份攻击 | - |
| TAIGen | 2025 | arXiv | 无需训练的对抗图像生成，采样步数减少10倍 | - |
| Backdoor Attacks on Face Detection | 2025 | arXiv | 人脸检测系统的后门攻击 | - |

### 🟢 Defense

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [Watermarking Diffusion Model](./categories/i2i/papers/2305.12502_watermarking_diffusion.md) | 2023 | arXiv | 扩散模型水印保护 | [📄](./categories/i2i/papers/2305.12502_watermarking_diffusion.md) |

[← Back to Top](#table-of-contents)

---

## 🎬 Image-to-Video (i2v)

图生视频生成模型的安全研究，包括视频生成、视频编辑等任务。

### 📊 Benchmark

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| [AnyV2V](./categories/i2v/papers/2403.14468_anyv2v.md) | 2024 | arXiv | 无调优视频编辑框架 | [📄](./categories/i2v/papers/2403.14468_anyv2v.md) |
| FrameBridge | 2024 | arXiv | 桥接模型改善I2V生成质量 | - |
| [MobileI2V](./categories/i2v/papers/2511.21475_mobilei2v.md) | 2025 | arXiv | 移动端高效I2V生成方案 | [📄](./categories/i2v/papers/2511.21475_mobilei2v.md) |

### 🔴 Attack

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [SWAN-DF Deepfake Vulnerability](./categories/i2v/papers/2311.17655_deepfake_vulnerability.md) | 2023 | arXiv | 首个逼真音视频深度伪造数据库SWAN-DF | [📄](./categories/i2v/papers/2311.17655_deepfake_vulnerability.md) |
| Adversarial Attacks on Deepfake Detectors | 2025 | ACM MM | AADD-2025挑战赛对抗攻击研究 | - |

### 🟢 Defense

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [DeepFakes and Beyond](./categories/i2v/papers/2001.00179_deepfakes_survey.md) | 2020 | arXiv | 深度伪造检测技术综述 | [📄](./categories/i2v/papers/2001.00179_deepfakes_survey.md) |
| Cross-Modal Fusion for WS-VAD | 2024 | CVPR | 多模态弱监督视频异常检测框架 | - |

[← Back to Top](#table-of-contents)

---

## 📝 Text-to-Text (t2t)

文本生成模型（LLM）的安全研究，包括对话系统、文本生成等任务。

### 📊 Benchmark

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| [From LLMs to MLLMs to Agents](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md) | 2025 | arXiv | 系统综述越狱攻击与防御范式演进 | [📄](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md) |
| [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) | 2025 | arXiv | 统一模块化框架，19种攻击+12种防御 | [📄](./categories/t2t/papers/2505.13862_pandaguard.md) |
| [A Survey of LLMs](./categories/t2t/papers/2303.18223_survey_llm.md) | 2023 | arXiv | LLM领域奠基性综述，持续更新 | [📄](./categories/t2t/papers/2303.18223_survey_llm.md) |

### 🔴 Attack

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [DeepInception](./categories/t2t/papers/2311.03191_deepinception.md) | 2023 | arXiv | 利用嵌套场景诱导LLM越狱 | [📄](./categories/t2t/papers/2311.03191_deepinception.md) |
| [PISmith](./categories/t2t/papers/2603.13026_pismith.md) | 2026 | arXiv | GRPO + 自适应熵正则化，ASR@10 达 100% | [📄](./categories/t2t/papers/2603.13026_pismith.md) |
| [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | 2024 | arXiv | 利用 LLM 自回归特性，1次查询 ASR 约 98% | [📄](./categories/t2t/papers/2410.02832_flipattack.md) |
| Paper Summary Attack | 2025 | arXiv | 利用 LLM 对权威来源的信任倾向 | - |
| InfoFlood | 2025 | arXiv | 通过信息过载淹没安全注意力机制 | - |
| Red Teaming the Mind of the Machine | 2025 | arXiv | 1400+ 对抗性提示的系统性红队测试 | - |
| Adversarial Attack-Defense Co-Evolution | 2025 | arXiv | 攻防协同进化框架 | - |

### 🟢 Defense

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) | 2025 | arXiv | 评测基准框架 | [📄](./categories/t2t/papers/2505.13862_pandaguard.md) |
| AutoDefense | 2024 | arXiv | 多智能体协作防御，降低误判率 30%+ | - |
| KG-DF | 2025 | arXiv | 基于知识图谱的语义关系网络检测 | - |
| DOOR | 2025 | arXiv | 双重优化目标，同时提升安全性和任务效用 | - |

[← Back to Top](#table-of-contents)

---

## 🎨 Text-to-Image (t2i)

文生图生成模型的安全研究，包括越狱攻击、概念擦除、内容安全过滤等。

### 📊 Benchmark

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|:----:|------|----------|:----:|
| [Generative AI in Vision](./categories/i2i/papers/2402.16369_generative_ai_in_vision.md) | 2024 | arXiv | 生成式AI视觉综述 | [📄](./categories/i2i/papers/2402.16369_generative_ai_in_vision.md) |
| [FRAP](./categories/t2i/papers/2408.11706_frap.md) | 2024 | arXiv | 自适应提示权重改善文本-图像对齐 | [📄](./categories/t2i/papers/2408.11706_frap.md) |
| [Adversarial T2I Survey](./categories/t2i/papers/1910.09399_adversarial_t2i_survey.md) | 2021 | arXiv | GAN时代文生图综述，奠定安全研究基础 | [📄](./categories/t2i/papers/1910.09399_adversarial_t2i_survey.md) |

### 🔴 Attack

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|:----:|------|----------|:----:|
| [SneakyPrompt](./categories/t2i/papers/2305.12082_sneakyprompt.md) | 2024 | IEEE S&P | 首个自动化越狱T2I，绕过DALL·E 2安全过滤器 | [📄](./categories/t2i/papers/2305.12082_sneakyprompt.md) |
| [JailLLM](./categories/t2i/papers/2503.01839_jailbreaking_via_llm.md) | 2025 | EACL | 利用微调LLM高效生成T2I越狱提示 | [📄](./categories/t2i/papers/2503.01839_jailbreaking_via_llm.md) |
| [Modifier Unlocked](./categories/t2i/papers/11023413_modifier_unlocked.md) | 2025 | IEEE S&P | 通过修饰符机制绕过T2I安全过滤 | [📄](./categories/t2i/papers/11023413_modifier_unlocked.md) |
| [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | 2025 | IEEE S&P | LLM智能体驱动的自动化越狱测试 | [📄](./categories/t2i/papers/2408.00523_jailfuzzer.md) |
| [DiffZOO](./categories/t2i/papers/2408.11071_diffzoo.md) | 2025 | NAACL | 零阶优化的纯黑盒越狱攻击 | [📄](./categories/t2i/papers/2408.11071_diffzoo.md) |
| [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | 2025 | arXiv | LLM驱动的T2I红队测试框架 | [📄](./categories/t2i/papers/2506.10047_genbreak.md) |
| [Reason2Attack](./categories/t2i/papers/2503.17987_reason2attack.md) | 2026 | AAAI | LLM推理驱动的越狱攻击 | [📄](./categories/t2i/papers/2503.17987_reason2attack.md) |
| [DAA Backdoor](./categories/t2i/papers/2504.20518_dynamic_attention_backdoor.md) | 2025 | TPAMI | 动态注意力分析T2I后门检测 | [📄](./categories/t2i/papers/2504.20518_dynamic_attention_backdoor.md) |

### 🟢 Defense

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|:----:|------|----------|:----:|
| [SPEED](./categories/t2i/papers/2503.07392_speed.md) | 2025 | arXiv | 可扩展精确高效的概念擦除 | [📄](./categories/t2i/papers/2503.07392_speed.md) |
| [TRCE](./categories/t2i/papers/2503.07389_trce.md) | 2025 | ICCV | 可靠的恶意概念擦除 | [📄](./categories/t2i/papers/2503.07389_trce.md) |
| [Concept Pinpoint Eraser](./categories/t2i/papers/2506.22806_concept_pinpoint_eraser.md) | 2025 | ICLR | 残差注意力门精准概念擦除 | [📄](./categories/t2i/papers/2506.22806_concept_pinpoint_eraser.md) |
| [SafeGuider](./categories/t2i/papers/2510.05173_safeguider.md) | 2025 | ACM CCS | 鲁棒实用的内容安全控制 | [📄](./categories/t2i/papers/2510.05173_safeguider.md) |
| [PromptGuard](./categories/t2i/papers/2501.03544_promptguard.md) | 2025 | arXiv | 软提示引导的不安全内容审核 | [📄](./categories/t2i/papers/2501.03544_promptguard.md) |
| [Watermarking Diffusion](./categories/i2i/papers/2305.12502_watermarking_diffusion.md) | 2023 | arXiv | 扩散模型水印内容保护 | [📄](./categories/i2i/papers/2305.12502_watermarking_diffusion.md) |

> 📂 完整论文列表: [全部攻击论文](./categories/t2i/attack/) · [全部防御论文](./categories/t2i/defense/) · [基础综述](./categories/t2i/benchmark/)

[← Back to Top](#table-of-contents)

---

## 📖 Image-to-Text (i2t)

图生文模型的安全研究，包括图像描述、VQA等任务。

### 📊 Benchmark

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| [Bottom-Up and Top-Down Attention](./categories/i2t/papers/1707.07998_bottom_up_attention.md) | 2018 | CVPR (Oral) | VQA和图像描述奠基性工作 | [📄](./categories/i2t/papers/1707.07998_bottom_up_attention.md) |
| [Multimodal ArXiv](./categories/i2t/papers/2404.10739_multimodal_arxiv.md) | 2024 | arXiv | MLLM科学理解评测数据集ArXivQA/ArXivCap | [📄](./categories/i2t/papers/2404.10739_multimodal_arxiv.md) |
| CapRL | 2025 | arXiv | 强化学习激发密集图像描述能力 | - |

### 🔴 Attack

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| Generative Bias in VQA | 2022 | arXiv | VQA模型数据集偏置研究 | - |

### 🟢 Defense

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [Object Hallucination Mitigation](./categories/i2t/papers/2310.00754_hallucination_mitigation.md) | 2023 | arXiv | 统一幻觉缓解框架 | [📄](./categories/i2t/papers/2310.00754_hallucination_mitigation.md) |
| [Semantic Refocused Tuning](./categories/i2t/papers/2409.16278_semantic_refocused.md) | 2024 | arXiv | 语义重聚焦调优改善VLM | [📄](./categories/i2t/papers/2409.16278_semantic_refocused.md) |

[← Back to Top](#table-of-contents)

---

## 🎥 Text-to-Video (t2v)

文生视频生成模型的安全研究。

### 📊 Benchmark

| 论文 | 年份 | 会议 | 核心贡献 | 详情 |
|------|------|------|----------|------|
| [Generative AI in Vision](./categories/i2i/papers/2402.16369_generative_ai_in_vision.md) | 2024 | arXiv | 生成式AI视觉综述，涵盖视频生成扩散模型 | [📄](./categories/i2i/papers/2402.16369_generative_ai_in_vision.md) |
| [AnyV2V](./categories/i2v/papers/2403.14468_anyv2v.md) | 2024 | arXiv | 无调优视频编辑 | [📄](./categories/i2v/papers/2403.14468_anyv2v.md) |
| [Noise Rectification](./categories/t2v/papers/2403.02827_noise_rectification.md) | 2024 | arXiv | 高保真度I2V生成的噪声校正方法 | [📄](./categories/t2v/papers/2403.02827_noise_rectification.md) |

### 🔴 Attack

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [SWAN-DF Deepfake Vulnerability](./categories/i2v/papers/2311.17655_deepfake_vulnerability.md) | 2023 | arXiv | 音视频深度伪造攻击研究 | [📄](./categories/i2v/papers/2311.17655_deepfake_vulnerability.md) |

### 🟢 Defense

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| [DeepFakes and Beyond](./categories/i2v/papers/2001.00179_deepfakes_survey.md) | 2020 | arXiv | 深度伪造检测技术综述 | [📄](./categories/i2v/papers/2001.00179_deepfakes_survey.md) |

[← Back to Top](#table-of-contents)

---

## 📋 Daily Reports

| 日期 | 报告 | 论文数 | 链接 |
|------|------|--------|------|
| 2026-03-23 | AI安全每日深度情报 | 9 篇 | [📄](./daily-reports/2026-03/2026-03-23_AI安全每日深度情报.md) |

---

## 🤖 Automation

本项目由自动化任务驱动，每天 00:00 自动执行：

1. 搜索 ArXiv (cs.CR, cs.CL, cs.LG, cs.CV) 最新论文
2. 按模态分类（i2i, i2v, t2t, t2i, i2t, t2v）
3. 按子类别分类（benchmark, attack, defense）
4. **去重检查**：确保不重复已收录的论文

### 数据来源

- [ArXiv cs.CR](https://arxiv.org/list/cs.CR/recent) - 计算机安全
- [ArXiv cs.CL](https://arxiv.org/list/cs.CL/recent) - 计算语言学
- [ArXiv cs.LG](https://arxiv.org/list/cs.LG/recent) - 机器学习
- [ArXiv cs.CV](https://arxiv.org/list/cs.CV/recent) - 计算机视觉

---

## 📁 Project Structure

```
ai-security-daily/
├── README.md
├── LICENSE
├── assets/
├── categories/
│   ├── i2i/           # 图生图
│   │   ├── benchmark/
│   │   ├── attack/
│   │   ├── defense/
│   │   └── papers/    # 详细论文分析
│   ├── i2v/           # 图生视频
│   │   ├── benchmark/
│   │   ├── attack/
│   │   ├── defense/
│   │   └── papers/
│   ├── t2t/           # 文生文
│   │   ├── benchmark/
│   │   ├── attack/
│   │   ├── defense/
│   │   └── papers/
│   ├── t2i/           # 文生图
│   │   ├── benchmark/
│   │   ├── attack/
│   │   ├── defense/
│   │   └── papers/
│   ├── i2t/           # 图生文
│   │   ├── benchmark/
│   │   ├── attack/
│   │   ├── defense/
│   │   └── papers/
│   └── t2v/           # 文生视频
│       ├── benchmark/
│       ├── attack/
│       ├── defense/
│       └── papers/
├── daily-reports/
│   └── 2026-03/
└── scripts/
```

---

## 🙏 Acknowledgements

本项目参考了以下优秀项目：

- [Awesome-MLLM-Safety](https://github.com/isXinLiu/Awesome-MLLM-Safety)
- [LLMSecurity](https://github.com/kiularm/LLM-Security)
- [JailbreakBench](https://github.com/jailbreakbench/jailbreakbench)

---

## 📝 License

MIT License

---

<p align="center">
  <sub>Generated by AI Security Daily Intelligence | Last Updated: 2026-03-23</sub>
</p>
