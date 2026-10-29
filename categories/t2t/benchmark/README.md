# 📊 文生文 - 基础评测集

文生文 LLM 的基础综述、安全评测基准论文。

> 最后回填: 2026-10-30 | 共 **20** 条

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
| Context Over Content | [2604.15224](https://arxiv.org/abs/2604.15224) | 2026 arXiv | 揭示 stakes signaling 会隐性污染 LLM-as-a-judge，峰值 Verdict Shift 达 -9.8 pp |
| Offensive Cyber Benchmark | [2604.17159](https://arxiv.org/abs/2604.17159) | 2026 arXiv | 用 NYU CTF Bench + Kali 工具环境系统评测 frontier LLM agent，证明环境与工具可发现性比大多数 prompt trick 更关键 |
| HarDBench | [2604.19274](https://arxiv.org/abs/2604.19274) | 2026 arXiv | 首个 draft-based co-authoring 灰区越狱基准，用 HS / ASR / RAR 衡量协同写作场景下的安全失效 |
| SHAPE | [2604.22134](https://arxiv.org/abs/2604.22134) | 2026 arXiv | 以 9087 条 student-question pairs 系统评测 pedagogical jailbreak，把教学语境下的 Safety / Helpfulness / Pedagogy 三指标正式 benchmark 化 |
| Conditional Misalignment | [2604.25891](https://arxiv.org/abs/2604.25891) | 2026 arXiv | 以标准 prompt vs context-triggered prompt 双入口评测揭示对齐干预可能只是在隐藏失配，而非真正消除风险 |
| Policy Is Not Capability | [2610.25060](https://arxiv.org/abs/2610.25060) | 2026 NeurIPS TAE WS | 用同一 5.3 万 prompt 池的**双策略标注**工业事故，证明 benchmark 分数大量测量的是"训练在哪套定义上"：JailbreakBench-benign 污染 **88%**、OR-Bench-hard **82%**；定义敏感度差 **23×**；**0.03% 参数**即可把 HarmBench-copyright 推过 **0→100** 而检测能力不变；验证准确率与策略一致性 $\rho=+0.74$ 而非检测能力 $\rho=+0.34$。主张把 contamination / seed floor / 被评定义作为一等变量报告 |
| DiagSafe | [2610.29225](https://arxiv.org/abs/2610.29225) | 2026 arXiv（**腾讯混元** × 北师大） | **84 叶子标签三层体系（11/34/84）+ 四要素标签规范 + prompt 级 rubric**；同一 judge（Hy3）只换提示范式，与人类一致率 **87.29% → 95.34%**，跨 judge 一致率 93.3%–94.8%（κ 0.83–0.86）；3,489 条中英双语；揭示**指令攻击把 unsafe rate 放大 1.9×–8.4×（中位 5.3×）**。数据将开源 ✅ 已精读 |
| Harm Is Behavioural, Moderation Is Lexical | [2610.31047](https://arxiv.org/abs/2610.31047) | 2026 arXiv | **跨语言审核评测协议**：5 系统 × 11 语言 = 55 组合，**51 个显著不如单个母语标注员**（差距 6–55 pt）；7 类"按形式判断"失效模式；**"最好减最差"是极值统计量**（同水平下 10 变体×100 例期望差距 9.2 pt，bootstrap 不覆盖零点） |
| Polarity Blindness | [2610.27908](https://arxiv.org/abs/2610.27908) | 2026 arXiv (ELLIS Alicante + ČVUT + UA) | 260 prompt 极性反转基准 × 10 模型 × 3 语言（187,200 推理 / 491,400 判分）：**否定/反义击穿安全判定、同义替换不能**，Grok 4.1 否定变体平均有害分 **4.12/5**；含"1/2/3 严重度无分辨率"发现 |
| AIMS | [2606.27210](https://arxiv.org/abs/2606.27210) | 2026 arXiv（**Adobe / NVIDIA** 参与） | 1,275 条 prompt / 1,724 条标注，用**集成不确定性筛选**困难样本；把 **intent 作为 prompt→label 的显式中间信号**，横跨 SFT / DPO / 推理蒸馏 / GRPO 四范式；GRPO（label+intent 双奖励）平均 F1 **0.836**，超过 GPT-5.4（0.815）与 Nemotron Safety 4B（0.809）✅ 已精读 |
| ANT-A / ANT-OR | [2610.32415](https://arxiv.org/abs/2610.32415) | 2026 EMNLP Findings（**蚂蚁集团** + 哈工大深圳） | **多标注者基准**：7 数据集 × 1,500 条 × **5 份独立人工标注** + 任务特定规范文档，用 **Fleiss κ 做分布感知评测**。κ 跨度 **38.77–83.50**，**2 类任务（医疗隐私 38.77）比 31 类任务（83.50）低 45 点** ⇒ 判定型任务比识别型难得多；含 3 个视觉-语言任务（56.37–81.27）。配套 ANT-OR：3 标注员 + 1 验证员 + **判别维度池**（2 正 1 负三元组蒸馏 → support ≥2 过滤），**不训练模型**，agreement@≥2 **+4.5 点**，κ 与人类差距 **2 点以内** ✅ 已精读 |

[← 返回文生文目录](../README.md)
