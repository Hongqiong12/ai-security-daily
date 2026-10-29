# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-262-green.svg">
    <img src="https://img.shields.io/badge/Papers-262-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--10--29-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--29-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-29)

> **为什么要关注本仓库？** 上周的关键词是"**机制装错了位置**"，今天更糟一层：**我们把六个"实际是变量"的东西当成常数在用**——指令措辞、指令位置、总体分数、聚合方式、推理步数、动作空间。每一个都能单独推翻结论。**共同点：所有"固定项"都在被测量之外悄悄改变答案。**

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I（输入侧改写的结构保真）** | [StruPO](./categories/t2i/papers/2610.36146_strupo.md) | **浙江大学 + 腾讯 AI Lab**。把"改写要保留什么"变成**标定过的场景图**，同一个表示**既当条件又当奖励**。DSE 非对称规则直击要害：**图只能否掉"你以为用户要的"，不能否掉"用户真要的"**。RR **69.64**（+7.96）、SGR **80.74**、跨主干 FLUX 上 RR **62.43 vs 53.41**。最狠的消融：**换自由生成，图条件+奖励+GRPO 全保留，SGR 依然 −7.06** ⇒ **动作空间本身就是保真机制**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-29_AI安全每日深度情报.md) |
| **T2I（权重侧失效的机制）** | [DICE](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) | **Tel Aviv，IEEE S&P 2027**。少步蒸馏让模型更不安全（SD3.5 NudeNet **0.2432→0.3232**），更关键的是**擦除方向被转掉了**：与教师方向余弦只有 **0.30 / 0.07**，成因定位到 **CFG 烘焙**（guidance 1.0→3.5 使 ‖δ‖ **17.8→64.1**）。顺带证明：**推理步数是一个安全旋钮**（50→8 步相似度 **+9%**）。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-29_AI安全每日深度情报.md) |
| **T2I（溯源与问责）** | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) | **Edinburgh + Oxford**。只用出图的**内在维度直方图**做黑盒签名，判断服务端跑的是底模还是 LoRA 适配。Problem II **AUROC 1.000 / F1 0.943**；而**有监督归因在开放世界留一域崩到 0.400**（比随机还差）。**Food101 失效**——适配域与底模太像时签不出来。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-29_AI安全每日深度情报.md) |
| **T+I2I（编辑评测方法论）** | [MoI-Bench](./categories/t2i/papers/2610.37599_moi_bench.md) | **UCL + 南大 + 港理工 + 华东师大**。**16 操作 × 8 目标**稀疏矩阵 → 64 子任务/1150 样本。四条纪律可直接抄：**稀疏 rubric 立方体**、**条件先写后跑**、**几何平均禁跨维补偿**、**能力缺失记 0 不移除**。双 judge 排名 **ρ=0.968**，但作者自承"档位一致不算独立验证"（阈值被反向校准）。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-29_AI安全每日深度情报.md) |
| **分类 SFT（层级标签的代价）** | [AK_QMUL @ ArGuard](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) | **QMUL**。单卡 4-bit QLoRA 拿下两个赛道（B1 **0.984**、B2 **0.790**）。三行消融最重要：**标签因子化 +0.001（等于零），去掉长尾补数据 −0.360**。分层表：总体 **0.79** 但 MSA 切片 **0.70**，`Bully` 总体 0.57、**MSA 上 0.46**。**最难的永远是最规范的那一档。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-29_AI安全每日深度情报.md) |
| **图审/judge（指标被污染）** | [VLM 拒答指令敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) | **IIT Hyderabad**。图像-问题对固定，只换同义话术，拒答率变 **18.4–45.2pp**、样本翻转 **13.9–32.1%**；换指令位置，InternVL **−8.1** 而 Qwen **+14.9（方向相反）**。**故意错配的安全指令几乎无效**（−2.3~+13.2，半数区间含 0）。SFT 拒答 **94.9%** 的同时 **24.1% 是"又拒又答"混合体**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-29_AI安全每日深度情报.md) |

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **262** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **参数被当成常数六连**(NEW) · **权重/输入/溯源三层边界量化**(NEW) · **擦除方向 cos 0.07**(NEW) · **几何平均禁补偿**(NEW) | 2026-10-29 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **因子化 +0.001 / −0.360**(NEW) · **拒答率被话术污染 45pp**(NEW) · **混合响应 24–33%**(NEW) · 模板 reason 零收益 · 判词不判意图 51/55 | 2026-10-29 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **StruPO 结构保真配方**(NEW) · **DICE 少步擦除方向退化**(NEW) · **LoRA 溯源签名**(NEW) · **MoI-Bench 二维评测**(NEW) | 2026-10-29 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | SkillGuard-Robust package-level 审计 · SnapGuard 轻量截图守卫 | 2026-04-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
