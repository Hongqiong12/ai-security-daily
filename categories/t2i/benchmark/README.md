# 📊 文生图 - 基础评测集

文生图扩散模型的安全评测基准、数据集与评估框架论文。

> 最后回填: 2026-04-28 | 共 **20** 条
> 延伸索引: [《T2I 安全 Benchmark 短名单（2026 年前高引用版）》](../../../insights/t2i-benchmark-shortlist-pre2026.md)

## 综述与全景

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| AI Security Landscape 2026 | — | 2026 (本项目) | 基于 198 篇论文的宏观安全格局分析（T2T/T2I/Agentic 三模态） |
| T2I Safety Seven-Year Survey | — | 2026 (本项目) | 文生图安全七年演进：从 Dual-Guard / Embedding Arithmetic / IncreFA，到 TwoHamsters / TICoE / BiasBench 的新信号沉淀 |
| Operationalizing Fairness in T2I Models | [2604.16516](https://arxiv.org/abs/2604.16516) | 2026 arXiv | 系统梳理 T2I 公平性审计与缓解文献，并提出 Target Fairness / Threshold Fairness 框架 |

## 安全评测基准 (Benchmark)

> 说明：**JailbreakBench** 已从本表移出，因为它本质是 LLM jailbreak benchmark，不属于 T2I benchmark。

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| HRS-Bench | [2304.05390](https://arxiv.org/abs/2304.05390) | 2023 ICCV | Holistic / Reliable / Scalable 三位一体的 T2I 综合评测框架，覆盖 50 类应用与多维能力指标 |
| HEIM (Holistic Evaluation) | [2311.04287](https://arxiv.org/abs/2311.04287) | 2023 NeurIPS Datasets & Benchmarks | 把质量、对齐与 bias / toxicity / fairness / robustness 纳入统一 T2I holistic evaluation |
| UnsafeBench | [2405.03486](https://arxiv.org/abs/2405.03486) | 2024 arXiv | 面向真实图像与 AI 生成图像的 image safety classifier 评测框架，代表生成后审核安全基准 |
| T2ISafety | [2501.12612](https://arxiv.org/abs/2501.12612) | 2025 CVPR | 系统覆盖 fairness / toxicity / privacy 的 T2I 安全专项 benchmark |
| SALMUBench | [2603.26316](https://arxiv.org/abs/2603.26316) | 2026 CVPR | Safe Unlearning 统一基准，支持概念擦除方法对比 |
| BPO-Verify | [2603.26328](https://arxiv.org/abs/2603.26328) | 2026 CVPR | 模型身份验证基准，检测生成内容是否来自目标模型 |
| AR Watermark Robustness | [2604.11720](https://arxiv.org/abs/2604.11720) | 2026 arXiv | 自回归图像生成水印在 removal / forgery / radioactive filtering 间存在结构性三难 |
| NTIRE 2026 Challenge | [2604.11487](https://arxiv.org/abs/2604.11487) | 2026 CVPR Workshop | 42 个生成器 + 36 种扰动的真实世界鲁棒 AIGC 检测挑战 |
| QuAD | [2604.15027](https://arxiv.org/abs/2604.15027) | 2026 CVPR Workshop | 首次把 near-duplicate 传播链与质量感知校准纳入 AIGI 检测，在 ReWIND 上带来约 8 个点 bAcc 提升 |
| T2I-BiasBench | [2604.12481](https://arxiv.org/abs/2604.12481) | 2026 arXiv | 用 13 指标统一审计 demographic bias、元素遗漏与 cultural collapse，补齐偏见评测维度 |
| Bias at the End of the Score | [2604.13305](https://arxiv.org/abs/2604.13305) | 2026 arXiv | 首次系统审计 reward models 的 demographic bias，揭示评分函数会放大 hypersexualization 与身份漂移 |
| TwoHamsters | [2604.15967](https://arxiv.org/abs/2604.15967) | 2026 arXiv | 首个 multi-concept compositional unsafety 基准，系统揭示组合语义风险与过滤器失效 |
| IncreFA / IABench | [2604.17736](https://arxiv.org/abs/2604.17736) | 2026 arXiv | 把生成器归因推进到 incremental open-set setting，并配套 IABench 衡量 Avg. Acc. / Auth. Acc. / Unseen Acc. |
| KVBench / KE-Check | [2604.22302](https://arxiv.org/abs/2604.22302) | 2026 arXiv | 以 1800 个双语教材级样本和 5158 条 checklist 把 T2I 正确性评测推进到知识密集 visual correctness，并用约束修正框架降低 scientific hallucination |

## 防御范式代表

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| ImageProtector | [2604.09024](https://arxiv.org/abs/2604.09024) | 2026 ACL | VPI (Visual Prompt Injection) 攻击翻转为隐私保护工具，91% 保护率 |
| FlowGuard | [2604.07879](https://arxiv.org/abs/2604.07879) | 2026 arXiv | 线性潜空间解码实现生成中 NSFW 检测，F1 提升 30%，内存减少 97% |
| EGLOCE | [2604.09405](https://arxiv.org/abs/2604.09405) | 2026 arXiv | 训练无关双能量引导潜空间优化用于概念擦除 |

[← 返回文生图目录](../README.md)
