# 📊 文生图 - 基础评测集

文生图扩散模型的安全评测基准、数据集与评估框架论文。

> 最后回填: 2026-04-21 | 共 **15** 条

## 综述与全景

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| AI Security Landscape 2026 | — | 2026 (本项目) | 基于 192 篇论文的宏观安全格局分析（T2T/T2I/Agentic 三模态） |
| T2I Safety Seven-Year Survey | — | 2026 (本项目) | 文生图安全七年演进：从 reward model 偏置审计 / 阈值化公平，到 TICoE / TwoHamsters / DAMP / Fragile Reconstruction / T2I-BiasBench 的新信号沉淀 |
| Operationalizing Fairness in T2I Models | [2604.16516](https://arxiv.org/abs/2604.16516) | 2026 arXiv | 系统梳理 T2I 公平性审计与缓解文献，并提出 Target Fairness / Threshold Fairness 框架 |

## 安全评测基准 (Benchmark)

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| JailbreakBench | [2404.01318](https://arxiv.org/abs/2404.01318) | 2024 NeurIPS | 标准化越狱攻击评测基准，覆盖多种 LLM/T2I 模型 |
| SALMUBench | [2603.26316](https://arxiv.org/abs/2603.26316) | 2026 CVPR | Safe Unlearning 统一基准，支持概念擦除方法对比 |
| BPO-Verify | [2603.26328](https://arxiv.org/abs/2603.26328) | 2026 CVPR | 模型身份验证基准，检测生成内容是否来自目标模型 |
| AR Watermark Robustness | [2604.11720](https://arxiv.org/abs/2604.11720) | 2026 arXiv | 自回归图像生成水印在 removal / forgery / radioactive filtering 间存在结构性三难 |
| NTIRE 2026 Challenge | [2604.11487](https://arxiv.org/abs/2604.11487) | 2026 CVPR Workshop | 42 个生成器 + 36 种扰动的真实世界鲁棒 AIGC 检测挑战 |
| QuAD | [2604.15027](https://arxiv.org/abs/2604.15027) | 2026 CVPR Workshop | 首次把 near-duplicate 传播链与质量感知校准纳入 AIGI 检测，在 ReWIND 上带来约 8 个点 bAcc 提升 |
| T2I-BiasBench | [2604.12481](https://arxiv.org/abs/2604.12481) | 2026 arXiv | 用 13 指标统一审计 demographic bias、元素遗漏与 cultural collapse，补齐偏见评测维度 |
| Bias at the End of the Score | [2604.13305](https://arxiv.org/abs/2604.13305) | 2026 arXiv | 首次系统审计 reward models 的 demographic bias，揭示评分函数会放大 hypersexualization 与身份漂移 |
| TwoHamsters | [2604.15967](https://arxiv.org/abs/2604.15967) | 2026 arXiv | 首个 multi-concept compositional unsafety 基准，系统揭示组合语义风险与过滤器失效 |

## 防御范式代表

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| ImageProtector | [2604.09024](https://arxiv.org/abs/2604.09024) | 2026 ACL | VPI (Visual Prompt Injection) 攻击翻转为隐私保护工具，91% 保护率 |
| FlowGuard | [2604.07879](https://arxiv.org/abs/2604.07879) | 2026 arXiv | 线性潜空间解码实现生成中 NSFW 检测，F1 提升 30%，内存减少 97% |
| EGLOCE | [2604.09405](https://arxiv.org/abs/2604.09405) | 2026 arXiv | 训练无关双能量引导潜空间优化用于概念擦除 |

[← 返回文生图目录](../README.md)
