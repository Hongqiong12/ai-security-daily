# AI Security Daily Intelligence

<p align="center">
  <img src="assets/logo.png" alt="AI Security Daily" width="200"/>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-30+-green.svg">
    <img src="https://img.shields.io/badge/Papers-30+-green.svg" alt="Total Papers"/>
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
| i2i | Image-to-Image | 图生图 | 7+ 篇 |
| i2v | Image-to-Video | 图生视频 | 7+ 篇 |
| t2t | Text-to-Text | 文生文 | 15+ 篇 |
| t2i | Text-to-Image | 文生图 | 6+ 篇 |
| i2t | Image-to-Text | 图生文 | 6+ 篇 |
| t2v | Text-to-Video | 文生视频 | 5+ 篇 |

### 分类体系

每个模态下包含三个子类别：

- **Benchmark**: 基础评测集、基准测试论文
- **Attack**: 攻击类论文（对抗攻击、越狱攻击、后门攻击等）
- **Defense**: 防御类论文（安全对齐、鲁棒性防御等）

---

## 🖼️ Image-to-Image (i2i)

图生图生成模型的安全研究，包括图像翻译、风格迁移、图像编辑等任务。

### 📊 Benchmark

| 论文 | ArXiv | 说明 |
|------|-------|------|
| Generative AI in Vision | [2402.16369](https://arxiv.org/abs/2402.16369) | 生成式AI视觉综述，覆盖扩散模型、GAN等 |
| Watermarking Diffusion Model | [2305.12502](https://arxiv.org/abs/2305.12502) | 首个DM水印方案 |
| Image-to-Image Translation with Conditional GANs | [1611.07004](https://arxiv.org/abs/1611.07004) | Pix2Pix奠基性论文 |

### 🔴 Attack

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Adv-Diffusion | [GitHub](https://github.com/kopper-xdu/Adv-Diffusion) | 基于潜在扩散模型的不可感知对抗人脸身份攻击 |
| TAIGen | [2508.15020](https://arxiv.org/abs/2508.15020) | 无需训练的对抗图像生成，采样步数减少10倍 |
| Backdoor Attacks on Face Detection | [2508.00620](https://arxiv.org/abs/2508.00620) | 人脸检测系统的后门攻击 |

### 🟢 Defense

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Watermarking Diffusion Model | [2305.12502](https://arxiv.org/abs/2305.12502) | 扩散模型水印保护 |

[← Back to Top](#table-of-contents)

---

## 🎬 Image-to-Video (i2v)

图生视频生成模型的安全研究，包括视频生成、视频编辑等任务。

### 📊 Benchmark

| 论文 | ArXiv | 说明 |
|------|-------|------|
| AnyV2V | [2403.14468](https://arxiv.org/abs/2403.14468) | 无调优视频编辑框架 |
| FrameBridge | [2410.15371](https://arxiv.org/abs/2410.15371) | 桥接模型改善I2V生成质量 |
| MobileI2V | [2511.21475](https://arxiv.org/abs/2511.21475) | 移动端高效I2V生成方案 |

### 🔴 Attack

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Vulnerability of Face Recognition to Deepfakes | [2311.17655](https://arxiv.org/abs/2311.17655) | 首个逼真音视频深度伪造数据库SWAN-DF |
| Adversarial Attacks on Deepfake Detectors | [ACM MM 2025](https://iplab.dmi.unict.it/mfs/acm-aadd-challenge-2025/) | AADD-2025挑战赛对抗攻击研究 |

### 🟢 Defense

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Deepfake Detection | [2001.00179](https://arxiv.org/abs/2001.00179) | 深度伪造检测技术综述 |
| Cross-Modal Fusion for WS-VAD | [CVPR 2024](https://blog.csdn.net/L1783516140/article/details/140087932) | 多模态弱监督视频异常检测框架 |

[← Back to Top](#table-of-contents)

---

## 📝 Text-to-Text (t2t)

文本生成模型（LLM）的安全研究，包括对话系统、文本生成等任务。

### 📊 Benchmark

| 论文 | ArXiv | 说明 |
|------|-------|------|
| From LLMs to MLLMs to Agents | [2506.15170](https://arxiv.org/abs/2506.15170) | 系统综述越狱攻击与防御范式演进 |
| PandaGuard | [2505.13862](https://arxiv.org/abs/2505.13862) | 统一模块化框架，19种攻击+12种防御 |
| A Survey of Large Language Models | [2303.18223](https://arxiv.org/abs/2303.18223) | LLM领域奠基性综述 |

### 🔴 Attack

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| DeepInception | [2311.03191](https://arxiv.org/abs/2311.03191) | 利用嵌套场景诱导LLM越狱 |
| PISmith | [2603.13026](https://arxiv.org/abs/2603.13026) | GRPO + 自适应熵正则化，ASR@10 达 100% |
| FlipAttack | [2410.02832](https://arxiv.org/abs/2410.02832) | 利用 LLM 自回归特性，1 次查询 ASR 约 98% |
| Paper Summary Attack | [2507.13474](https://arxiv.org/abs/2507.13474) | 利用 LLM 对权威来源的信任倾向 |
| InfoFlood | [2506.12274](https://arxiv.org/abs/2506.12274) | 通过信息过载淹没安全注意力机制 |
| Red Teaming the Mind of the Machine | [2505.04806](https://arxiv.org/abs/2505.04806) | 1400+ 对抗性提示的系统性红队测试 |
| Adversarial Attack-Defense Co-Evolution | [2511.19218](https://arxiv.org/abs/2511.19218) | 攻防协同进化框架 |

### 🟢 Defense

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| PandaGuard | [2505.13862](https://arxiv.org/abs/2505.13862) | 评测基准框架 |
| AutoDefense | [2403.04783](https://arxiv.org/abs/2403.04783) | 多智能体协作防御，降低误判率 30%+ |
| KG-DF | [2511.07480](https://arxiv.org/abs/2511.07480) | 基于知识图谱的语义关系网络检测 |
| DOOR | [2503.03710](https://arxiv.org/abs/2503.03710) | 双重优化目标，同时提升安全性和任务效用 |

[← Back to Top](#table-of-contents)

---

## 🎨 Text-to-Image (t2i)

文生图生成模型的安全研究，包括扩散模型安全、NSFW过滤等。

### 📊 Benchmark

| 论文 | ArXiv | 说明 |
|------|-------|------|
| Generative AI in Vision | [2402.16369](https://arxiv.org/abs/2402.16369) | 生成式AI视觉综述 |
| FRAP | [2408.11706](https://arxiv.org/abs/2408.11706) | 自适应提示权重改善文本-图像对齐 |
| Adversarial Text-to-Image Synthesis | [1910.09399](https://arxiv.org/abs/1910.09399) | GAN时代文生图综述 |

### 🔴 Attack

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| SneakyPrompt | [2305.12082](https://arxiv.org/abs/2305.12082) | 首个自动化越狱T2I模型，绕过DALL·E 2安全过滤器 |

### 🟢 Defense

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Watermarking Diffusion Model | [2305.12502](https://arxiv.org/abs/2305.12502) | 扩散模型水印保护 |

[← Back to Top](#table-of-contents)

---

## 📖 Image-to-Text (i2t)

图生文模型的安全研究，包括图像描述、VQA等任务。

### 📊 Benchmark

| 论文 | ArXiv | 说明 |
|------|-------|------|
| Bottom-Up and Top-Down Attention | [1707.07998](https://arxiv.org/abs/1707.07998) | VQA和图像描述奠基性工作 |
| Multimodal ArXiv | [2404.10739](https://arxiv.org/abs/2404.10739) | MLLM科学理解评测数据集 |
| CapRL | [2509.22647](https://arxiv.org/abs/2509.22647) | 强化学习激发密集图像描述能力 |

### 🔴 Attack

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Generative Bias in VQA | [2208.00690](https://arxiv.org/abs/2208.00690) | VQA模型数据集偏置研究 |

### 🟢 Defense

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Unified Hallucination Mitigation | [2310.00754](https://arxiv.org/abs/2310.00754) | 统一幻觉缓解框架 |
| Semantic Refocused Tuning | [2409.16278](https://arxiv.org/abs/2409.16278) | 语义重聚焦调优改善VLM |

[← Back to Top](#table-of-contents)

---

## 🎥 Text-to-Video (t2v)

文生视频生成模型的安全研究。

### 📊 Benchmark

| 论文 | ArXiv | 说明 |
|------|-------|------|
| Generative AI in Vision | [2402.16369](https://arxiv.org/abs/2402.16369) | 生成式AI视觉综述 |
| AnyV2V | [2403.14468](https://arxiv.org/abs/2403.14468) | 无调优视频编辑 |
| Noise Rectification | [2403.02827](https://arxiv.org/abs/2403.02827) | 高保真度I2V生成的噪声校正方法 |

### 🔴 Attack

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Vulnerability of Face Recognition to Deepfakes | [2311.17655](https://arxiv.org/abs/2311.17655) | 音视频深度伪造攻击研究 |

### 🟢 Defense

| 论文 | ArXiv | 核心创新 |
|------|-------|----------|
| Deepfake Detection | [2001.00179](https://arxiv.org/abs/2001.00179) | 深度伪造检测技术综述 |

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
│   │   └── defense/
│   ├── i2v/           # 图生视频
│   ├── t2t/           # 文生文
│   ├── t2i/           # 文生图
│   ├── i2t/           # 图生文
│   └── t2v/           # 文生视频
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
