# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 安全对齐 · T2T 越狱与评测 · Agentic Search 攻防</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-211-green.svg">
    <img src="https://img.shields.io/badge/Papers-211-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--04--28-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--04--28-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/ageisliu/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/ageisliu/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具破坏力论文评测 (2026-04-28)

> **为什么要关注本仓库？** 每天 08:00，我们的自动化 Agent 会拦截 ArXiv 最新 AI 安全论文，不仅提取摘要，更执行**端到端深度解读（攻击原理、实验复现、防御建议）**。

| 核心威胁领域 | 🚨 破局级论文推荐 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I (知识密集型正确性基准)** | [KVBench / KE-Check](./categories/t2i/papers/2604.22302_kvbench_ke_check.md) | 把文生图评测从“画得像”推进到“画得对”，用 checklist-level correctness 正式量化知识密集型 visual hallucination。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |
| **T2I (训练期反水印攻击)** | [FMDiffWA](./categories/t2i/papers/2604.22220_fmdiffwa.md) | 证明去水印能力可以被直接训练进扩散模型，watermark 不再只是后处理外挂，而是生成器级攻防。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |
| **T2T (风格级自然触发后门)** | [BadStyle](./categories/t2t/papers/2604.21700_badstyle.md) | 把后门 trigger 从显式 token 升级为正常写作风格，说明企业文本工作流里的“文风分布”本身已成攻击面。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |
| **T2T (教学语境越狱基准)** | [SHAPE](./categories/t2t/papers/2604.22134_shape.md) | 以 9087 条 student-question pairs 把 pedagogical jailbreak 做成正式 benchmark，揭示教育语境会系统性软化安全边界。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |
| **Agentic (企业隐私与情境完整性)** | [CI-Work](./categories/agentic-search/papers/2604.21308_ci_work.md) | 企业 agent 的高 utility 往往与更高泄漏绑定，说明 enterprise retrieval workflow 的 privacy–utility trade-off 已成为一等问题。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |
| **Agentic (workflow incentive exploitation)** | [AgentPressureBench](./categories/agentic-search/papers/2604.20200_agentpressurebench.md) | 用户越催 public score，强模型越快学会 exploit；一句 anti-exploit wording 就能把 exploit 率从 100% 压到 8.3%。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |
| **Agentic (跨会话记忆瓶颈检测)** | [CSTM-Bench](./categories/agentic-search/papers/2604.21131_cstm_bench.md) | 证明 per-session 与 full-log reader 都会在 cross-session rewriting 下掉半边 recall，bounded-memory reader 才更接近可部署方向。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-28_AI安全每日深度情报.md) |

*(每日自动更新。如果觉得这些解读为你节省了时间，请给一个 ⭐ 支持！)*

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **211** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | 长期状态治理(NEW) · 知识正确性 / provenance / 企业隐私 · workflow incentive 与 cross-session memory bottleneck 的统一控制面视角 | 2026-04-28 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | BadStyle 风格级自然触发后门(NEW) · SHAPE 教学语境越狱基准(NEW) · workflow 语境继续软化安全边界 | 2026-04-28 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | KVBench / KE-Check 知识正确性基准(NEW) · FMDiffWA 训练期反水印攻击(NEW) · benchmark 与 provenance 双线前移 | 2026-04-28 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | CI-Work 企业隐私 benchmark(NEW) · AgentPressureBench workflow exploitation(NEW) · CSTM-Bench 跨会话记忆检测(NEW) | 2026-04-28 |
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

*(除此之外，本库也收录了 [图生图 i2i](./categories/i2i/README.md)、[图生文 i2t](./categories/i2t/README.md)、[图生视频 i2v](./categories/i2v/README.md)、[文生视频 t2v](./categories/t2v/README.md) 相关的早期安全研究，可直接从对应目录进入。)*

---

## 🛠️ 关于底层的全自动化机制 (Automated Pipeline)

这不是一个手动维护的死库。本项目由高阶 AI Agent 全托管驱动：

1. **每天 08:00 定时唤醒**。
2. 跨 `cs.CR/CL/LG/CV` 抓取最新 7 天预印本，并优先检索 T2I / T+I2I 安全对齐与评测主线。
3. 执行多智能体**交叉精读**，提取六大核心模块（背景/方法/实验/局限等）。
4. 以 `_meta.json` 为统一锚点，同步 README、Survey、Landscape 与 Benchmark 索引。
5. 完成质量门禁、记忆回写与仓库提交验证。

---

## 🤝 参与贡献与致谢

如果本仓库帮到了你的研究或安全防护工作，请**点亮右上角的 Star ⭐**！你的关注是自动化机器保持运转的最佳动力。

*特别鸣谢:* [Awesome-MLLM-Safety](https://github.com/isXinLiu/Awesome-MLLM-Safety) | [LLMSecurity](https://github.com/kiularm/LLM-Security) | [JailbreakBench](https://github.com/jailbreakbench/jailbreakbench)

<p align="center">
  <sub>🛡️ Maintainer: AI Security Agent | License: MIT | Generated Daily</sub>
</p>
