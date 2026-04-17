# 📊 文生文 - 基础评测集

文生文 LLM 的基础综述、安全评测基准论文。

> 最后回填: 2026-04-17 | 共 **9** 条

## 综述类

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| From LLMs to MLLMs to Agents | [2506.15170](https://arxiv.org/abs/2506.15170) | 2025 arXiv | 系统综述 LLM→MLLM→Agent 演进中的越狱攻击与防御范式 |
| A Survey of Large Language Models | [2303.18223](https://arxiv.org/abs/2303.18223) | 2023 arXiv | LLM 领域奠基性综述，涵盖预训练到对齐的完整技术栈 |

## 安全评测基准 (Benchmark)

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| PandaGuard | [2505.13862](https://arxiv.org/abs/2505.13862) | 2025 arXiv | 统一模块化框架，19 种攻击 + 12 种防御，49 个 LLM 评测基准 |
| ClawSafety | [2604.01438](https://arxiv.org/abs/2604.01438) | 2026 arXiv | Agent 安全综合评测，120 个对抗场景覆盖技能注入/邮件注入/Web 注入向量 |
| SelfGrader | [2604.01473](https://arxiv.org/abs/2604.01473) | 2026 arXiv | Token 级 logit 检测器，ASR 降低 22.66%，内存减少 173x，速度提升 26x |
| Defense Trilemma | [2604.06436](https://arxiv.org/abs/2604.06436) | 2026 arXiv | 形式化证明安全对齐的三难困境（有用性-安全性-鲁棒性不可兼得） |
| Art of Misalignment | [2604.07754](https://arxiv.org/abs/2604.07754) | 2026 ACL Findings | ORPO 是最强错位武器，DPO 是最强重对齐但牺牲效用 |
| CausalDetox | [2604.14602](https://arxiv.org/abs/2604.14602) | 2026 ACL | 以 PNS 因果标准选择 toxic heads，并提出 ParaTox 成对 benchmark 做反事实去毒评估 |
| RLVR Reward Hacking | [2604.15149](https://arxiv.org/abs/2604.15149) | 2026 arXiv | 用 IPT 揭示 RLVR verifier gaming，把“通过验证器”拆解为真实求解与 reward shortcut |

[← 返回文生文目录](../README.md)
