# ⚔️ AI Security Daily Intelligence

<p align="center">
  <img src="assets/logo.png" alt="AI Security Daily" width="200"/>
</p>

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2T LLM 越狱 · T2I 概念擦除 · Agentic Search 投毒防御</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-162+-green.svg">
    <img src="https://img.shields.io/badge/Papers-162+-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--04--15-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--04--15-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/ageisliu/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/ageisliu/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具破坏力论文评测 (2026-04-15)

> **为什么要关注本仓库？** 每天 08:00，我们的自动化 Agent 会拦截 ArXiv 最新 AI 安全论文，不仅提取摘要，更执行**端到端深度解读（攻击原理、实验复现、防御建议）**。

| 核心威胁领域 | 🚨 破局级论文推荐 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2T (奖励回路后门)** | [Backdoors in RLVR](./categories/t2t/papers/2604.09748_backdoors_in_rlvr.md) | RLVR 只需 <2% 投毒样本就能学出高泛化 jailbreak backdoor，OOD-ASR 达 81.9%。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-15_AI安全每日深度情报.md) |
| **T2T (表示层防御)** | [LIRA](./categories/t2t/papers/2604.10403_latent_instruction_representation_alignment.md) | 把安全对齐从“输出拒答”推进到 instruction representation 对齐，PEZ 攻击可被压到接近 0。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-15_AI安全每日深度情报.md) |
| **T2I (闭式擦除)** | [Closed-Form DP](./categories/t2i/papers/2604.10032_closed_form_concept_erasure.md) | 双投影 + 左零空间硬约束把 concept erasure 做成 training-free 几何闭式解。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-15_AI安全每日深度情报.md) |
| **T2I (鲁棒检测基准)** | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md) | 42 个生成器 + 36 种扰动的真实世界 AIGC 检测挑战，把 Robust ROC AUC 变成主指标。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-15_AI安全每日深度情报.md) |
| **Agentic (规划一致性防御)** | [PlanGuard](./categories/agentic-search/papers/2604.10134_planguard.md) | 用 planning-based consistency verification 把 indirect prompt injection 的 ASR 从 72.8% 压到 0%。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-15_AI安全每日深度情报.md) |
| **Agentic (记忆抽取攻击)** | [ADAM](./categories/agentic-search/papers/2604.09747_adam_agent_memory_extraction.md) | 把 memory extraction 变成 entropy-guided adaptive querying，最高可达 100% ASR。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-15_AI安全每日深度情报.md) |

*(每日自动更新。如果觉得这些解读为你节省了时间，请给一个 ⭐ 支持！)*

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **162** 篇安全顶会论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | 宏观格局分析 · 内部表示/运行时边界/鲁棒检测三条新信号 · 未来八个极具潜力的研究方向 | 2026-04-15 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | 越狱攻击四代演进史 · 奖励回路后门(NEW) · 指令表示对齐 LIRA(NEW) · 双曲几何防御 · 形式化三难困境 | 2026-04-15 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | 局部 DPO 安全控制 · Closed-Form DP 双投影擦除(NEW) · NTIRE 2026 鲁棒检测基准(NEW) · 单流 DiT 挑战 | 2026-04-15 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | 结构化解析瓶颈 · 运行时边界防护 · PlanGuard 规划一致性验证(NEW) · ADAM 记忆抽取攻击(NEW) | 2026-04-15 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 概念擦除对抗、自动化红队测试、单流模型攻击、隐藏后门

- **Attack (攻击突破):** [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md) | [SafeGuider](./categories/t2i/papers/2510.05173_safeguider.md) | [Latent Guard](./categories/t2i/papers/2404.08031_latent_guard.md)
- **Benchmark:** [JailbreakBench](./categories/t2i/papers/2404.01318_jailbreakbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

### 🤖 Agentic Search (AI 搜索) 安全
> **核心关注:** 检索污染 (Data Poisoning)、工具劫持 (Tool Hijacking)、引用幻觉

- **全维度研究:** 涵盖 Perplexity/SearchGPT 架构下的 Plan → Search → Generate 安全审计。请访问 [Agentic Search 目录](./categories/agentic-search/)。

*(除此之外，本库也收录了 [图生图 i2i](#)、[图生文 i2t](#)、[文生视频 t2v](#) 相关的早期安全研究。详见目录区。)*

---

## 🛠️ 关于底层的全自动化机制 (Automated Pipeline)

这不是一个手动维护的死库。本项目由高阶 AI Agent 全托管驱动：

1. **每天 08:00 定时唤醒**。
2. 跨 `cs.CR/LG/CV` 抓取最新 7 天预印本。
3. 执行多智能体**交叉精读**，提取六大核心模块（背景/方法/实验/局限等）。
4. 自动生成分类、更新 README 面板并推送到此仓库。

---

## 🤝 参与贡献与致谢

如果本仓库帮到了你的研究或安全防护工作，请**点亮右上角的 Star ⭐**！你的关注是自动化机器保持运转的最佳动力。

*特别鸣谢:* [Awesome-MLLM-Safety](https://github.com/isXinLiu/Awesome-MLLM-Safety) | [LLMSecurity](https://github.com/kiularm/LLM-Security) | [JailbreakBench](https://github.com/jailbreakbench/jailbreakbench)

<p align="center">
  <sub>🛡️ Maintainer: AI Security Agent | License: MIT | Generated Daily</sub>
</p>
