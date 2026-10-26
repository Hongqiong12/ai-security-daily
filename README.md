# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-250-green.svg">
    <img src="https://img.shields.io/badge/Papers-250-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--10--27-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--27-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-27)

> **为什么要关注本仓库？** 上周的关键词是"**分数不可信**"，今天更进一步：**分数装错了东西**。三篇独立工作证明——评测器会跟着被评对象一起变差、审核系统判的是词不是意图、奖励指标分不清"画质好"与"画面干净"。共同解法只有一个：**找一个模型之外的锚。**

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T+I2I（编辑评测的底座）** | [ABACUS](./categories/t2i/papers/2610.28316_abacus.md) | **CEA List / 巴黎萨克雷，WACV 2027**。用 VLM judge 评编辑是**循环论证**——I2EBench 甚至专设 counting 维度却用 GPT-4V 来判。改成"全景真值 + SAM3 + 匈牙利实例匹配 + 双检测器共识"的 judge-free 协议后：与人类计数一致性 **0.82**（纯 VLM 0.55、单检测器 0.28）；**跨 7 个编辑器的 σ 从 0.065 降到 0.013**。七个 SOTA 编辑器最高分只有 **0.31**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-27_AI安全每日深度情报.md) |
| **T+I2I（分流 0/0% 的解法）** | [EditJev](./categories/t2i/papers/2610.32635_editjev.md) | **北大 + 清华**。把"选哪个编辑器"从**分类**改成**两候选偏好排序**：pairwise ranking **4.6002** vs MCQ **4.5491** vs MSE 4.5545。路由开销 **94 ms**，端到端 **56.9 s → 22.3 s（2.55×）**。两个负结果更有用：路由骨干 2B/4B/32B 得分 4.5898/4.6002/4.5898（**32B 没有更好**），去掉图像输入只掉 0.029。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-27_AI安全每日深度情报.md) |
| **T2I（权重侧 vs 输入侧的分工）** | [Concept Acupuncturist](./categories/t2i/papers/2610.32059_concept_acp.md) | **中科院信工所 + 波士顿大学 + NUS**。SAE **只造监督、不进推理链路**：定位单一 cross-attn block 做局部微调，SDXL-Turbo T1 FSR **80.02**（最强基线 43.68）、训练成本 **−46.4%**、推理开销 **0**。**但只报 FSR 会骗人**——对照里有人 FSR 77.90 配 FID **197.32**。逐概念 FSR 从 Nudity **94.16** 掉到 Parachute **45.60**：可擦性由表示结构决定。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-27_AI安全每日深度情报.md) |
| **T2I（奖励缺维，不是偏置）** | [AdvFidelity](./categories/t2i/papers/2610.29380_advfidelity.md) | **阿里淘天 + 上交**。**8 步超过 50 步 RL**（HPSv2 0.4125 > 0.4096）。真正该抄的是附录：1,000 组"内容相同、只差伪影"的配对上，**HPSv3 胜出率仅 38.30%**（61.7% 的配对里它认为带伪影的图更好），HPSv2 胜率 79.90% 但**平均配对差分为负**。**奖励对低层保真近乎失明。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-27_AI安全每日深度情报.md) |
| **审核（判词不判意图 + 统计陷阱）** | [Harm Is Behavioural](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) | 5 系统 × 11 语言 = 55 组合，**51 个显著不如单个母语标注员**；**能力越强跨语言不平等越大**（0.6B→8B：均值 0.65→0.81，极差 0.20→0.29）。最狠的一刀在 6.1 节：**"最好减最差"是极值统计量**——各类同水平时，10 类×100 例的期望差距就有 **9.2 个点**，bootstrap 还覆盖不到零点。**"VULG-HINT-EDGE 最差"可能只是噪声峰值。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-27_AI安全每日深度情报.md) |
| **改写（语义保真的失效边界）** | [Polarity Blindness](./categories/t2t/papers/2610.27908_polarity_blindness.md) | **ELLIS Alicante + ČVUT + UA**。260 prompt × 10 模型 × 3 语言、187,200 次推理：**只改极性（否定/反义）就能击穿安全判定，只换同义词不能**。Grok 4.1 否定变体平均有害分 **4.12/5**。工程纪律一句话：**改写可以换词、可以弱化、可以抽象化，但不能改极性。** 否定式豁免条款 = 给下游塞一个极性盲探针。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-27_AI安全每日深度情报.md) |

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **250** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **judge-free 评测协议**(NEW) · **排序优于分类**(NEW) · **奖励伪影盲区**(NEW) · **极值统计陷阱**(NEW) · **极性盲**(NEW) | 2026-10-27 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **判词不判意图 51/55**(NEW) · **极性盲 4.12/5**(NEW) · 极值统计陷阱 · DiagSafe 84 标签+rubric | 2026-10-27 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **ABACUS judge-free 编辑评测**(NEW) · **EditJev 编辑路由**(NEW) · **ConceptACP SAE 定位擦除**(NEW) · **AdvFidelity 奖励审计**(NEW) | 2026-10-27 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | SkillGuard-Robust package-level 审计 · SnapGuard 轻量截图守卫 | 2026-04-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
