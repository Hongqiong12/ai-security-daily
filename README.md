# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 安全对齐 · T2T 越狱与评测 · Agentic Search 攻防</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-198-green.svg">
    <img src="https://img.shields.io/badge/Papers-198-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--04--22-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--04--22-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/ageisliu/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/ageisliu/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具破坏力论文评测 (2026-04-22)

> **为什么要关注本仓库？** 每天 08:00，我们的自动化 Agent 会拦截 ArXiv 最新 AI 安全论文，不仅提取摘要，更执行**端到端深度解读（攻击原理、实验复现、防御建议）**。

| 核心威胁领域 | 🚨 破局级论文推荐 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I (双通道溯源水印)** | [Dual-Guard](./categories/t2i/papers/2604.19090_dual_guard.md) | 把扩散起点与 VAE latent 同时变成可验证指纹，首次把 provenance、篡改定位与画质保持做成一体化方案。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-22_AI安全每日深度情报.md) |
| **T2I (推理时去偏)** | [Embedding Arithmetic](./categories/t2i/papers/2604.18167_embedding_arithmetic.md) | 不改模型权重，只在文本嵌入空间做属性向量算术，就能显著压低 gender/race 偏置，说明 fairness 治理开始进入 inference-time control。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-22_AI安全每日深度情报.md) |
| **T2I (增量归因评测)** | [IncreFA](./categories/t2i/papers/2604.17736_increfa.md) | 把生成器归因从闭集分类推进到 incremental open-set setting，并配套 IABench，让 attribution 真正贴近模型持续演化现实。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-22_AI安全每日深度情报.md) |
| **T2T (模式补全越狱)** | [IICL](./categories/t2t/papers/2604.19461_iicl.md) | 把 jailbreak 从显式危险请求改写为抽象算子与 pattern completion，说明 few-shot 语境本身就是安全边界的软化器。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-22_AI安全每日深度情报.md) |
| **T2T (协同写作灰区基准)** | [HarDBench](./categories/t2t/papers/2604.19274_hardbench.md) | 首次把 draft-based co-authoring 里的灰区 harmful request 形式化成 benchmark，揭示“帮你润色/补完”是当前对齐系统的真实盲区。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-22_AI安全每日深度情报.md) |
| **Agentic (隐私执行环境)** | [GAAP](./categories/agentic-search/papers/2604.19657_gaap.md) | 把 agent 私有数据保护重写成 deterministic execution environment，用 IFC、权限库与 disclosure log 把隐私泄露约束进执行语义本身。 | [📄 立即阅读](./daily-reports/2026-04/2026-04-22_AI安全每日深度情报.md) |

*(每日自动更新。如果觉得这些解读为你节省了时间，请给一个 ⭐ 支持！)*

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **198** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | provenance / attribution / 隐私执行环境(NEW) · 上游控制面安全化 · 可信载体中的隐式风险组合 · 评测系统反身安全化 | 2026-04-22 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | IICL 模式补全越狱(NEW) · HarDBench 协同写作灰区基准(NEW) · gray-zone jailbreak 与部署后安全修补主线汇合 | 2026-04-22 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | Dual-Guard 双通道溯源(NEW) · Embedding Arithmetic 推理时去偏(NEW) · IncreFA / IABench 增量归因(NEW) | 2026-04-22 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | GAAP 确定性隐私执行环境(NEW) · CASCADE 协议级级联防线 · Visual Inception 长期记忆投毒 | 2026-04-22 |
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
