# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-292-green.svg">
    <img src="https://img.shields.io/badge/Papers-292-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--05-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--05-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-05)

> **前两周的结论是"拆到能动手的那一层"。这周换一个角度：**六篇各自在拆同一颗雷——**我们汇报的每个数字，都绑定在产生它的那个配置上。** 配对图 97% 的像素在变，所以旧 benchmark 的分数不可比；12 个配置块的阈值从 10% 到 97%，所以阈值不可跨模型搬；同一模型在 13.9% 与 49.5% 之间切换，只是因为换了尺子。**换模型、换变体、换数据集、换评测协议，数字就作废。**
>
> **✅ 供给侧先说清楚**：最新批次仍是 **11-03**，**11-04 批次在 00:00 尚未生成** ⇒ 相对昨天 **T2I 新供给为 0**。全量 **78 路**查询去重 **542**（窗口 10-29 → 11-05），未收录候选 **530**，但**全部是昨天已扫过的存量**。因此本轮转为**存量深挖**：把昨天的"候选观察"升级为精读。空窗第 **十一** 周，证据同昨天一样硬：**542 篇按 NSFW 严格词边界扫描 0 命中**、（生成∩安全∩改写）**只剩 1 篇且是已读过的 VEvo**、**14 路专项查询归零**。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **I2I 评测（对照组设计）** | [CompoSET](./categories/t2i/papers/2610.41118_composet_single_edit_benchmark.md) | **Caltech（Perona 组）**。量了一件事：旧 benchmark 的配对图**平均 97% 像素在变**，模型只要看出"整张图不一样"就答对。把差异压到 **8%**（1,776 instance / 80 场景 / 每 base **~22 个 foil** / 16 种编辑），**22 个 dual-encoder 全部低于随机线**（最好 13.9% vs 随机 16.67%，聚类 bootstrap 后 22 个上界全 < 15.55%）。同模型在 BiVLC 是 49.5% ⇒ **不是模型差，是尺子换**。附带：**文本侧硬负样本不迁移**（NegCLIP 7.0% < base 7.8%）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-05_AI安全每日深度情报.md) |
| **阈值下发（工业真表）** | [PGuard](./categories/t2i/papers/2611.02791_pguard_native_streaming_guardrail.md) | **阿里巴巴 AAIG**。原生流式护栏读 backbone 的 residual stream，**不改推理路径**，百亿级 backbone 上开销仅 **0.82–2.26%**，文本 F1 **0.836**。附录 B 把 **12 个配置块 × 29 个子类目阈值**全公开，跨度 **10%–97%**。最扎的一行：**图-文 query 的 29 个阈值里 24 个恰压在下限 10%**（同模型文本 query 中位 40+）⇒ **图审没有可用的中间 operating point**。过度拒答同方法不同变体 **6.12% vs 16.09%**，差 2.6 倍。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-05_AI安全每日深度情报.md) |
| **输入侧（第二条路）** | [ODC](./categories/t2i/papers/2611.00819_odc_orthogonal_drift_correction.md) | **墨尔本大学**。文字一个字不动，改**嵌入**：漂移向量取对 prompt 的**正交分量** → 词表检索回词 → QR 秩缩减（ζ=1%）剔除。**先取正交再减**这个设计正是"风险锚点外科替换"的形式化——锚点不是词，是方向。代价：**CLIP +1.47 的同时 UniDet −20%**；A&E 专门做对齐却**比不改还差**（29.54 < 30.33）。⇒ 表征层手术的天花板就在这。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-05_AI安全每日深度情报.md) |
| **RL 奖励（价码表）** | [DeCoRL](./categories/t2i/papers/2610.39265_decore_rl_object_consistency_reward.md) | **小红书**。把整体一致性拆成**物体级奖励，缺失记 0**。DeCo-Bench **6.22 → 7.05(SFT) → 8.16(RL)**，6 参考图档 **3.64 → 7.61**。最该看的是 Table 3：**指令遵循 −0.8%，换主体相似度 +9.0%、自然度 +22.6%** —— 与昨天 Kling 的"保真 4.45→4.38"是同一个方向。另一个数：**vanilla VLM 奖励 7.21 vs 训练过 8.16**（差 SFT 增益的 7 倍）⇒ **接个现成 VLM 当奖励基本无效**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-05_AI安全每日深度情报.md) |
| **误杀根因（非阈值）** | [GOAL](./categories/t2t/papers/2610.39802_goal_over_refusal_gradient_orthogonalization.md) | **合工大 + NUS**。误杀不是阈值问题，是**梯度耦合**：有害样本梯度低秩且与"拒绝"目标对齐更强，把无害但像风险的样本一起推向拒答；深层表示**越来越重叠**。做**拒绝子空间正交化 + 对比学习**：拒答率 **19.5% → 9.0%**，安全分反升（JBB **0.90→0.97**），通用能力最大掉 **0.0071**，人工 Useful Compliance **66.5→76.0**。⇒ **如果表示已重叠，阈值只能在混叠的轴上切。** | [📄 立即阅读](./daily-reports/2026-11/2026-11-05_AI安全每日深度情报.md) |
| **多版本回归口径** | [SQM](./categories/t2t/papers/2611.00447_sqm_ordinal_judge_calibration.md) | **Upwork**。17 种校准方法大比武，SQM（分位数匹配）综合第一（MAE **+31.4%**、Wasserstein **+27.9%**）。最硬的数：**校准前后 Spearman 0.494、Kendall 0.450 完全不变** ⇒ **校准只改尺度，不改排序**。所以它能救"中等 judge"（补掉对 GPT-5 差距的 **83.9%/70.1%**），救不了小 judge（**34.5–45.5%**），`< 10ms` 单次、**第 1 百分位数据就收敛**。⇒ 5 节点下的正解是"20–30B + 校准"，不是"100B"。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-05_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **292** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **数字绑定配置：同一模型 13.9% vs 49.5%**（NEW） · **图-文阈值 24/29 压地板**（NEW） · **校准不改排序（0.494→0.494）**（NEW） · **RL 用 −0.8% 指令遵循换 +9.0% 相似度**（NEW） | 2026-11-05 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **GOAL：误杀是梯度耦合，拒答率 19.5%→9.0%**（NEW） · **SQM 校准不改排序**（NEW） · **中 judge + 校准补 70–84% 差距**（NEW） · **小 judge 只补 34–46%**（NEW） | 2026-11-05 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **CompoSET：97%→8% 像素变化，22 模型全部低于随机**（NEW） · **PGuard 12 块阈值表 10–97%**（NEW） · **ODC 正交分量改嵌入**（NEW） · **DeCoRL 物体级奖励缺失记 0**（NEW） | 2026-11-05 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [词级风险锚点表](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) (保义替换降 3–28 点) | [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) (阈值只修 1/3–1/2) | [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [Kling 输入侧改写配方](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) (接上生成器保真 −0.07) | [UniForget 跨通路擦除](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (DF 92.7%→37.1%) | [AegisFlow 路径约束](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) (MNC 贴边界) | [VEvo-Harness 三动作路由](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) (看图门控 2% vs 16%) | [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [UUBench 跨通路六格](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (SF≤TF / SR≤NR) | [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
