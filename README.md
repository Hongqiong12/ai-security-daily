# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-226-green.svg">
    <img src="https://img.shields.io/badge/Papers-232-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--06--24-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--22-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/ageisliu/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/ageisliu/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-22)

> **为什么要关注本仓库？** 过去 7 天里，T2I 安全出现了一次清晰的范式收敛：**安全控制正在从"条件依赖"转向"状态依赖"，而与此同时评测这把尺子本身正在被审计。** 前者解决"什么时候拦、拦多重、拦完剩多少语义"，后者回答"我们报的数字到底测的是什么"。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I (输入侧早期拦截)** | [CSTI](./categories/t2i/papers/2610.26452_csti.md) | 读 CFG 原生条件/无条件激活之差，step 15 就能判风险；不需攻击样本、不改生成器，拦截路径延迟降 60%+。是 rewriter 最理想的**前置 gate**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-22_AI安全每日深度情报.md) |
| **T2I (安全控制解耦)** | [DSC](./categories/t2i/papers/2610.21569_dsc.md) | **腾讯署名 · NeurIPS 2026**。点破"耦合安全控制链"缺陷，把干预拆成五段状态依赖环节——映射过来就是"风险标签不该同时决定要不要改/改哪/改成什么/改多狠"。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-22_AI安全每日深度情报.md) |
| **T2I (rewriter 的 RL 训练)** | [SCOPE](./categories/t2i/papers/2610.22264_scope.md) | 图像奖励不该摊到 subword，应按**语义 span** 分配信用。与业务形态（LLM rewriter + 冻结 Qwen-Image + RL）完全对齐，纯 loss 层改动，GeneVal +9.48%。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-22_AI安全每日深度情报.md) |
| **T2I (保真度量重构)** | [PPAA](./categories/t2i/papers/2610.27719_ppaa.md) | **ECCV 2026 Spotlight**。用**相对相似度比**取代绝对差，阈值直接表示"保留 X% 语义"；并首次定义"同域近邻保留"空白。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-22_AI安全每日深度情报.md) |
| **T2T→T2I (约束优先改写)** | [AMEND](./categories/t2t/papers/2610.23183_amend.md) | 加权和 reward 会让"换个主题"伪装成安全改写。改成**先卡语义硬门槛再排序**，是有界回路替代多轮辩论的直接依据。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-22_AI安全每日深度情报.md) |
| **T2T→T2I (评测协议审计)** | [Policy Is Not Capability](./categories/t2t/papers/2610.25060_policy_is_not_capability.md) | **NeurIPS 2026 TAE WS**。0.03% 参数就能把 benchmark 推过满量程而检测能力不变——PORN/VULG 边界混淆，先查标注口径再改模型。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-22_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **232** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **state-dependent safety control**(NEW) · **eval protocol reflexive audit**(NEW) · relative-ratio fidelity(NEW) · semantic-span credit(NEW) | 2026-10-22 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | Policy Is Not Capability 评测协议审计(NEW) · AMEND constraint-first 选择(NEW) | 2026-10-22 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | CSTI 输入侧早停 gate(NEW) · DSC 控制链解耦(NEW) · SCOPE 语义 span 信用(NEW) · PPAA 相对比值保真(NEW) | 2026-10-22 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | SkillGuard-Robust package-level 审计 · SnapGuard 轻量截图守卫 | 2026-04-30 |
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
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [HealBench](./categories/t2i/benchmark/README.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
