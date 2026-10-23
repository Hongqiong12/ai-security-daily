# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-238-green.svg">
    <img src="https://img.shields.io/badge/Papers-238-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--10--23-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--23-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/ageisliu/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-23)

> **为什么要关注本仓库？** 过去 7 天里，T2I 安全的主线从"造方法"转到了"查归因"。四篇工作分别从**锚点、审核器架构、判定标准、意图绑定**四个角度，指出了现有 pipeline 里四个"看起来在动、其实没归因"的位置——改写收益该记在谁头上、图审失效该记在谁头上、指标提升该记在谁头上。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I (改写收益归因)** | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | **本周业务价值最高**。场景固定、只改锚点条件的消融：无锚点改写 **−0.8**、检索锚点 **+2.9**（top-1 仅 40%）、oracle **+8.6**。**改写天花板由锚点定位决定，不是 rewriter 能力。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-23_AI安全每日深度情报.md) |
| **T2I (输出侧图审失效)** | [Mirage](./categories/t2i/papers/2610.30348_mirage.md) | 只改图像通道、文本不动即可绕过生成后审核器。同一批攻击 bypass 率 **CLIP 0.800 / NudeNet 0.435 / ViT 0.185**（差 4.3 倍），且 **bypass ≠ ASR**（差 16 点）。图审架构就是安全边界。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-23_AI安全每日深度情报.md) |
| **T2I (三维评测 + 专属 scorer)** | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | **AAAI'27**。三维分列 + 目标维度 **1:2:1** 加权；通用 scorer 在目标维度上近似随机（Acc 0.50–0.56），专属 scorer 达 **0.8527**。**通用一致性指标不能当安全维度奖励。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-23_AI安全每日深度情报.md) |
| **T2I (指令遵循可判定化)** | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | prompt→ASP 约束、图像→场景图、clingo 判 SAT，**无需参考图**。单约束 84% → 多约束 **20%**，UNSAT 识别仅 23%。"反空真条款"可直接搬到改写保真核验。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-23_AI安全每日深度情报.md) |
| **T2T→T2I (标签体系分层)** | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) | **腾讯混元** × 北师大。84 叶子标签三层体系 + **四要素标签规范（含豁免行为）** + prompt 级 rubric。同一 judge 只换提示范式，人类一致率 **87.29% → 95.34%**。指令攻击把 unsafe rate 放大 **5.3 倍**（中位）。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-23_AI安全每日深度情报.md) |
| **T2T→T2I (意图显式绑定)** | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | **Adobe/NVIDIA** 参与。1,275 条标注 + GRPO（label+intent 双奖励）平均 F1 **0.836**，超过 GPT-5.4。**6/71 例意图表述几乎相同而标签相反** → PORN/VULG 混淆不是"不懂"，是"没绑死"。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-23_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **238** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **attribution engineering**(NEW) · anchor-locality ceiling(NEW) · checker-architecture-as-boundary(NEW) · rubric-over-judge(NEW) | 2026-10-23 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | DiagSafe 84 标签+rubric(NEW) · AIMS 意图显式绑定(NEW) · Policy Is Not Capability 协议审计 | 2026-10-23 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | IMPLICIT-Bench 锚点归因(NEW) · Mirage 图审架构差异(NEW) · HealBench 1:2:1 三维(NEW) · LogicVal 约束判定(NEW) | 2026-10-23 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | SkillGuard-Robust package-level 审计 · SnapGuard 轻量截图守卫 | 2026-04-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

### 🤖 Agentic Search (AI 搜索) 安全
> **核心关注:** 检索污染 (Data Poisoning)、工具劫持 (Tool Hijacking)、引用幻觉

- **全维度研究:** 涵盖 Perplexity/SearchGPT 架构下的 Plan → Search → Generate 安全审计。请访问 [Agentic Search 目录](./categories/agentic-search/)。

*(除此之外，本库也收录了 [图生图 i2i](./categories/i2i/README.md)、[图生文 i2t](./categories/i2t/README.md)、[图生视频 i2v](./categories/i2v/README.md)、[文生视频 t2v](./categories/t2v/README.md) 相关的早期安全研究，可直接从对应目录进入。)*

---

## 🛠️ 关于底层的全自动化机制 (Automated Pipeline)

这不是一个手动维护的死库。本项目由高阶 AI Agent 全托管驱动：

1. **每天 08:00 定时唤醒**。
2. 跨 `cs.CR/CL/LG/CV` 抓取最新 7 天预印本，并优先检索 **T2I / T+I2I 工业安全**、**输入侧 Prompt Rewrite / Safety Rewriting**、NSFW 语义保真改写与可部署 benchmark 主线。
3. 执行多智能体**交叉精读**，提取六大核心模块（背景/方法/实验/局限等），并强制输出“业务对齐研究板块”。
4. 以 `_meta.json` 为统一锚点，同步 README、Survey、Landscape 与 Benchmark 索引。
5. 完成质量门禁、记忆回写与仓库提交验证。

---

## 🤝 参与贡献与致谢

如果本仓库帮到了你的研究或安全防护工作，请**点亮右上角的 Star ⭐**！你的关注是自动化机器保持运转的最佳动力。

*特别鸣谢:* [Awesome-MLLM-Safety](https://github.com/isXinLiu/Awesome-MLLM-Safety) | [LLMSecurity](https://github.com/kiularm/LLM-Security) | [JailbreakBench](https://github.com/jailbreakbench/jailbreakbench)

<p align="center">
  <sub>🛡️ Maintainer: AI Security Agent | License: MIT | Generated Daily</sub>
</p>
