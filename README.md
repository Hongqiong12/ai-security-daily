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
  <a href="https://img.shields.io/badge/Papers-174+-green.svg">
    <img src="https://img.shields.io/badge/Papers-174+-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--04--17-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--04--17-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/ageisliu/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/ageisliu/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具破坏力论文评测 (2026-04-17)

> **为什么要关注本仓库？** 每天 08:00，我们的自动化 Agent 会拦截 ArXiv 最新 AI 安全论文，不仅提取摘要，更执行**端到端深度解读（攻击原理、实验复现、防御建议）**。

| 核心威胁领域 | 🚨 破局级论文推荐 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I (结构化类遗忘)** | [DAMP](./categories/t2i/papers/2604.15166_damp.md) | 把 class unlearning 从输出层 masking 推进到分层 forget-specific direction 投影，绝大多数设置下 Forget Accuracy 压到 0。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-17_AI安全每日深度情报.md) |
| **T2I (野外检测校准)** | [QuAD](./categories/t2i/papers/2604.15027_quad.md) | 首次把 near-duplicate 传播链与质量感知校准合并进 AIGC 检测，在 ReWIND 上把 bAcc 从 63.0 拉到 70.3。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-17_AI安全每日深度情报.md) |
| **T2T (因果头去毒)** | [CausalDetox](./categories/t2t/papers/2604.14602_causaldetox.md) | 用 PNS 选出真正对 toxic generation 必要且充分的 attention heads，在 12/12 组合上优于普通 ITI。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-17_AI安全每日深度情报.md) |
| **T2T (验证器漏洞评测)** | [RLVR Reward Hacking](./categories/t2t/papers/2604.15149_rlvr_hacking.md) | 证明 RLVR 会把模型推向 verifier gaming，GPT-5 Nano 在 Hard tier 上 shortcut 达到 184/250。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-17_AI安全每日深度情报.md) |
| **Agentic (经济型路由攻击)** | [R2A](./categories/agentic-search/papers/2604.15022_r2a.md) | 通过通用对抗后缀把普通 query 引流到昂贵模型，OpenRouter 上平均成本可被放大到约 2.7×–2.9×。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-17_AI安全每日深度情报.md) |
| **Agentic (协议级通信治理)** | [CBCL](./categories/agentic-search/papers/2604.14512_cbcl.md) | 用 DCFL 约束自扩展通信语言，让运行时方言扩展首次同时具备 extensibility 与 verifiability。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-17_AI安全每日深度情报.md) |

*(每日自动更新。如果觉得这些解读为你节省了时间，请给一个 ⭐ 支持！)*

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **174** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | 宏观格局分析 · verifier gaming / 路由经济攻击 / 质量感知检测三条新信号 · 未来研究方向重排 | 2026-04-17 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | 越狱攻击四代演进史 · CausalDetox 因果头去毒(NEW) · RLVR 奖励黑客诊断(NEW) · 指令表示对齐 LIRA | 2026-04-17 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | DAMP 深度感知类遗忘(NEW) · QuAD 近重复质量校准(NEW) · Closed-Form DP 双投影擦除 · 单流 DiT 挑战 | 2026-04-17 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | 路由经济攻击 R2A(NEW) · 协议级通信治理 CBCL(NEW) · 运行时边界防护 · MCP 生态威胁 | 2026-04-17 |
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
