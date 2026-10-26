# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-244-green.svg">
    <img src="https://img.shields.io/badge/Papers-244-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--10--26-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--26-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-26)

> **为什么要关注本仓库？** 今天的关键词是"**分数不可信**"。四篇核心工作从训练配方、评测协议、锚点距离、奖励偏置四个角度，同时指向一件事：**我们现有的图审 AB 与改写评测，报出来的数字可能不反映真实能力**。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I (图审基座配方)** | [Yuvion VL](./categories/t2i/papers/2606.25034_yuvion_vl.md) | **阿里安全 AGI Lab**。核心是 C2FT：用**模型自己的错误**挖混淆集，再用 Teacher Forcing 验证困难负样本，最后多图拼接做跨图对比（ρ=0.3）。8B 相对骨干 **+12.4**（公开安全）/ **+11.3**（内部业务）/ **+17.8**（AI 生成图检测）。**单样本 SFT 给不出边界判别信号**，这句被写成了配方。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-26_AI安全每日深度情报.md) |
| **T2I (图审判定依据)** | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) | **阿里 + 浙大**。掩码消融给出硬证据：把有害语义全换成等长占位符（空白图/静音）后，Qwen2.5-Omni-3B 仍有 **0.99–1.00 召回**，平均 **FPR 0.87**。**它读的不是内容，是形状。** 三维里 reliability 这一维我们现在完全没测。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-26_AI安全每日深度情报.md) |
| **T2I (锚点距离 = 擦除边界)** | [SELECT](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | 北邮。锚点不是终点，**它定义"擦到哪儿为止"**。五类锚点里 **Sibling Exclusive**（同父类+核心属性互斥）BCTS 最高。NSFW 的现成模板：把裸露换成 **"a gardener in overalls and long sleeves"**——保留主体与场景，只换敏感属性。名人擦除 H_c **81.99 → 87.99**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-26_AI安全每日深度情报.md) |
| **T2I (奖励偏置删能力)** | [Attractive Faces Skew](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | 偏好奖励会**覆盖保真判断**：Elo 模拟里好看的 AI 队领先 **+124**；5 个偏好模型有 **4 个**的 top-1 相关属性是 "attractive"；最强一击是 ReNO 优化 "an unattractive face" **反而变漂亮**。**奖励语义是图文对齐，实际行为是变好看。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-26_AI安全每日深度情报.md) |
| **工业审核 (管线是偏向采样器)** | [AVLM Failure Taxonomy](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) | **TikTok/字节 + 悉尼大学，NeurIPS 2026**。`q(x) = p(x)·S_retain(x)/E[S_retain]`：**原始语料规模会高估可学覆盖**，且重加权救不回"保留概率为 0"的样本类型。五类失效签名 → 干预，每类都有可证伪诊断信号。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-26_AI安全每日深度情报.md) |
| **T2T→T2I (匹配误报率)** | [Faithful Harm Monitors](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) | 分布内 AUROC **0.998** 的监控器，在改写集上掉到 **0.62**，而**不看模型**的 TF-IDF 能到 **0.75**。匹配误报率下拒绝本身抓 **32.1%**、读出抓 **44%**，但增益全是"换词拒绝"被字符串匹配漏标的部分。**图审 AB 必须改成同误报预算比召回。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-26_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **244** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **C2FT 混淆对比**(NEW) · **masking-probe**(NEW) · **matched-FAR**(NEW) · **anchor-distance-curve**(NEW) · reward-semantics-vs-behavior(NEW) | 2026-10-26 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **Matched-FAR 监控器批判**(NEW) · DiagSafe 84 标签+rubric · AIMS 意图显式绑定 | 2026-10-26 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **Yuvion VL C2FT 图审配方**(NEW) · **Omni-UBench 掩码消融**(NEW) · **SELECT 锚点距离**(NEW) · **奖励偏置删能力**(NEW) | 2026-10-26 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | SkillGuard-Robust package-level 审计 · SnapGuard 轻量截图守卫 | 2026-04-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
