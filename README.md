# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-334-green.svg">
    <img src="https://img.shields.io/badge/Papers-334-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--24-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--24-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-24)

> **今天六篇没有一篇在说"分数不够高"。它们在说：被当成达标读数的那个量，往往只是真正风险的代理，而且脱钩是单方向的——所以分数没动，判定已经全换了。**
>
> **✅ 供给侧**：网页端十分类 `/list/<cat>/recent?show=2000` 串行全批扫描（避开导出 API 的 IP 级 429），公告批次 **11-17→11-23 五个批次**，其中 **11-23 为新增 565 篇**；全批池 **3991 篇**（1739 篇带摘要），主题词 **18 路** + 方法论形态 **12 路**全部在本地池正则复现、零额外检索请求。本轮为**供给回暖轮**。
>
> **⚠️ 空窗第 十七 周，口径写得更窄**：`t2_prompt_rewrite` 严格 **0**（输入侧安全改写法仍零供给）；但 `t3_i2i_edit_safety` 1、`t6_concept_erasure`/`t18_generated_risk` 20/28、`t10_video_safety` **1**（视频扩展本轮有强相关工作）⇒ 出图侧干预 / 图审 / 图文联合判定 / 量化不劣化**四条相邻带同时有强供给**。`t14_policy_guard` 5 命中逐篇核验 **0 可迁移**（全是 RAG 混合检索），"有量不等于有供给"第四次生效。
>
> **🎯 本轮最扎的一个数**：AnimalFarm —— 源场景经**两名标注员独立接受**的保守人工筛查（输入侧已相当干净），生成系统仍对 **92.1%** 的计划查询出图、其中 **95.9%** 含仇恨，而最强图审只认出 **73.9%**。⇒ **改写后文本无害 ≠ 出图侧无害**，与本项目 3,000 条 case 中 2,700+ 条源于出图侧内生风险同构。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **不看图的探针拿了 0.9645 AUROC** | [Unimodal Shortcuts](./categories/t2i/papers/2611.27339_unimodal_shortcuts_scene_intent.md) | **港科大 + 深大 + XGEN Labs + 港科广 + 清华**。五个情境安全 benchmark 的标签都能由单模态预测：灰图纯文本探针 **0.9645–0.9846 AUROC**，而四路控制把单模态上界压到 **0.500**；中间层 joint probe **0.958/0.930**，跨 benchmark 只 **0.48–0.67**。缓存探针 **0.234 ms** vs 独立安全 pass **95.82 ms**、prefill 仅 **+0.36%**。⇒ 连验收用的公开 benchmark 都不要求读图，I2I 0/0% 拿到第五种归因。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **输入干净，出图照样 95.9% 带仇恨** | [AnimalFarm](./categories/t2i/papers/2611.27905_animalfarm_hateful_image_audit.md) | **CISPA Helmholtz + Independent + HPE**。14,250 queries / 12,900 attempts，**92.1% 出图 / 95.9% 仇恨**；三通路 GPT Image 2 **66.6/68.0/75.3**，最强 GPT-5.5 图审 recall 仅 **73.9%**、LlavaGuard **28.0**；Prompt Enhancement 使 LlavaGuard **28.8→64.4**；SFT+GRPO 检测器 F1 **0.962/0.979**，奖励 **0.7/0.1/0.1/0.1**；`1−G/Q` 是 non-generation、**不等于拒答率**；LABUBU 未见仍 **96.6%**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **二值安全评测会放过"塌成噪声"** | [EBSG](./categories/t2i/papers/2611.20623_ebsg_example_based_spatial_guidance.md) | **KAIST（NeurIPS 2026 poster）**。细粒度子概念 + 空间局部引导，training-free、不改输入不改权重：VLM rubric 与人工一致 **82.6%**；SR **97.2/96.2/84.2/97.4** 而 NR 仅 **1.4/1.3/0.4/0.0**；FID **6.31 vs 7.83**、CLIP **0.263 vs 0.259**；新增 `NOTRELEVANT` 档。⇒ 出图侧生成过程干预第一次有了可执行的第三条通路。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **生成增益差 25 倍，改写器只差 0.14 分** | [P2E / Prune to Expand](./categories/t2i/papers/2611.27229_p2e_supervision_redundancy.md) | **港城大 + 港中深**。`D_H` 增益 **3.20** vs `D_M` **0.13**（约 25×），同配置训出的 PE 却只差 **+0.14 HPS v2 / +0.05 PicS / +0.002 MIQA / +0.000 VQ-R1**；无约束剪枝 **27.27→26.46**，视觉守护剪枝反升 **27.59**；K=3 / τ=0.4 / 800 prompts / 4 generators / Qwen3.5-9B。⇒ "按生成增益选 SFT 监督目标"被配对证伪。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **准确率只动 0.03 点，判定换了 1.1–12.3%** | [The Vulnerability Window](./categories/t2t/papers/2611.27155_vulnerability_window_quantized_judges.md) | **Illinois Institute of Technology + UW–Milwaukee**。4-bit 量化下 **1.1–12.3%** 成对判定翻转而聚合准确率只动 **0.03 点**；NF4 Llama-3.2-1B **3.99%**；harmful:helpful 翻转 **146:54**；脆弱窗口随规模 **25%→7%**；best-of-64 选中项变 **14.6–65.7%** 而最终答案只 **2.6–9.6%**（**5–8×**）。⇒ fp8/fp4 上线必须做「逐对翻转」四栏不劣化验收。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **judge 的偏置是单向的** | [Your Judge Inherits Your Prompt](./categories/t2t/papers/2611.26881_judge_inherits_prompt_directional_bias.md) | **University of Essex + Independent（BlackboxNLP 2026 Workshop）**。只改 judge 的 Yes/No few-shot 标签平衡、其余全冻结：偏向接受在 NExT-QA S3 虚高 **+29.5 点**、FP:FN **9.4**，MSVD-QA **+19.5**、FP:FN **4.0**；偏向拒绝/balanced 只在 **±2.5** 内 ⇒ **inflation-only asymmetry**；单次抽样波动达 **18 点**；每数据集 **200 例人工共识**。⇒ 图审 AB 看板必须冻结 judge 配置指纹。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |

⏱ **今日一句话**：**别再往输入侧加码了**。先把「灰图探针验收、三通路对照、出图侧生成过程干预、逐对翻转 + judge 尺子四栏不劣化」补进验收，把 2,700+ 条 case 从"改写还不够严"改写为"风险长在出图侧"；否则 0/0% 会继续被写成"改写没写好"。

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **334** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **分数没动，判定全换了（热点三十一）**（NEW） · **灰图探针 0.9645 AUROC**（NEW） · **出图 92.1% / 仇恨 95.9% 而图审 recall 73.9%**（NEW） · **量化后 1.1–12.3% 成对翻转**（NEW） | 2026-11-24 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **聚合准确率只动 0.03 点而 1.1–12.3% 成对判定被 4-bit 重写**（NEW） · **judge 偏置单向：接受侧虚高 +29.5 点、拒绝侧不下降**（NEW） · **量化/加速安全率不劣化四栏验收**（NEW） | 2026-11-24 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **五个情境安全 benchmark 都有单模态捷径**（NEW） · **AnimalFarm：三通路输入干净而出图侧内生风险**（NEW） · **EBSG：不改输入/权重的子概念空间引导**（NEW） · **P2E：SFT 监督冗余使生成增益与改写器脱钩 25×**（NEW） | 2026-11-24 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [Risk-certified 约束式策略选点](./categories/t2t/papers/2611.20156_risk_certified_prompt_optimization.md) (max 放行率 s.t. 漏过 ≤ α / LTT+Clopper–Pearson) | [词级风险锚点表](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) (保义替换降 3–28 点) | [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [The Vulnerability Window](./categories/t2t/papers/2611.27155_vulnerability_window_quantized_judges.md) (1.1–12.3% 成对翻转 / 聚合准确率只动 0.03 点) | [Your Judge Inherits Your Prompt](./categories/t2t/papers/2611.26881_judge_inherits_prompt_directional_bias.md) (接受偏置虚高 +29.5 点，拒绝侧不对称) | [Operating-Point Failure 冻结护栏失效](./categories/t2t/papers/2611.19216_operating_point_failure_frozen_guardrail.md) (FPR 1.01%→15.12% 而 AUROC ≤0.0058 / 重设 9/9 恢复) | [Jev 分级护栏的匹配预算对照](./categories/t2t/papers/2611.08845_jev_guardrail_overrefusal.md) (同 4% 误杀：三级 3.9% vs 重调单门 4.6% / 二级精度 53.8%) | [指标教程：阈值选法决定一切](./categories/t2t/papers/2611.08048_metrics_scenario_guide.md) (代价 274→473.5 / F1 最高者最贵 / 聚合 0.691-0.700-0.857) | [StreamLTT 流式风险认证](./categories/t2t/papers/2611.04062_streamltt_risk_certification.md) (换检验 0.0300 vs 换定义 0.0090) | [Alignment Tax 分级退化](./categories/t2t/papers/2611.06476_alignment_tax_graded.md) (0.550 vs 0.981 / ≥96% 来自压制 rejected) | [Risk Control 率不承诺个体](./categories/t2t/papers/2611.05851_risk_control_rates_not_magnitudes.md) (271.3 mm 在 α=0.10 内 / 改定义便宜 47 倍) | [Failure-Boundary 两曲线评测](./categories/t2t/papers/2611.06453_failure_boundary_profiles.md) (恒停/恒闯钉 0.5 / 53.7 vs 32.2) | [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) (阈值只修 1/3–1/2) | [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [DSC 延迟语义承诺](./categories/t2i/papers/2611.25929_deferred_semantic_commitment.md) (问句+✓ 使 Endorsed 15.3%→41.3% / 语义一字未改) | [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [EBSG 子概念空间引导](./categories/t2i/papers/2611.20623_ebsg_example_based_spatial_guidance.md) (SR 97.2/96.2/84.2/97.4 而 NR ≤1.4 / FID 6.31 vs 7.83) | [P2E 冗余监督](./categories/t2i/papers/2611.27229_p2e_supervision_redundancy.md) (生成增益 25× 而改写器只差 +0.14 HPS v2) | [Tripwire-WM 伪造事件报告](./categories/t2i/papers/2611.25226_tripwire_wm_forgery_evident.md) (伪造接受 0% vs 55.0% / 真图 ≥99% @10⁻⁶ FPR) | [StitchEdit 层间兼容探针](./categories/t2i/papers/2611.07922_stitchedit_per_layer_gradient_probe.md) (源深度锁死 CLIP-Dir 0.62 / oracle 也仅 0.79) | [GARM 有界奖励](./categories/t2i/papers/2611.07648_garm_tabo_bounded_reward.md) (单加硬负例泄漏 0.046→0.057) | [TailSteer 尾部校正单点有效](./categories/t2i/papers/2611.06741_tailsteer_multiturn_edit_drift.md) (49+1 步稳 / 50 步过平滑 / FreqEdit −6 编辑率换保真) | [IntrAA-SD 同架构归因](./categories/t2i/papers/2611.06000_intraa_sd_finetune_attribution.md) (99.03 ID / 88.55 OOD) | [Kling 输入侧改写配方](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) (接上生成器保真 −0.07) | [UniForget 跨通路擦除](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (DF 92.7%→37.1%) | [AegisFlow 路径约束](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) (MNC 贴边界) | [VEvo-Harness 三动作路由](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) (看图门控 2% vs 16%) | [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [Unimodal Shortcuts](./categories/t2i/papers/2611.27339_unimodal_shortcuts_scene_intent.md) (灰图纯文本探针 0.9645–0.9846 AUROC / 四路控制上界 0.500) | [AnimalFarm](./categories/t2i/papers/2611.27905_animalfarm_hateful_image_audit.md) (92.1% 出图 / 95.9% 仇恨 / 最强图审 recall 73.9%) | [EditSafetyBench 图文联合安全](./categories/t2i/papers/2611.26569_editsafetybench_text_aware_vision_blind.md) (UIR 87.1% vs UNR 24.2% / 5,940 配对) | [CuRSE-Bench 文化盲区](./categories/t2i/papers/2611.20821_curse_bench_cultural_blind_spots.md) (10,709+2,648 / 6 地区 × 10 harm axes) | [T2I-NSI 否定约束未绑定](./categories/t2i/papers/2611.09304_t2i_negation_suppression.md) (反向 0.00% vs 未执行 13–17% / WEAKLY_REND 占七成 / κ 0.09) | [UniMore 统一模型特异性损失](./categories/t2i/papers/2611.08996_unimore_specificity_unified.md) (WISE +3.59 而 UEval +0.70 / color binding +8.25) | [VisionValueBench 中立 prompt 的值泄漏](./categories/t2i/papers/2611.05578_visionvaluebench_value_leakage.md) (改写器使 UAI −0.357→+0.182) | [Proxy Audit 代理变量审计](./categories/t2i/papers/2611.07132_proxy_audit_t2i_disparity.md) (0.310 vs 0.312 但姓氏格 0.523) | [LongBanana 图结构原子判据](./categories/t2i/papers/2611.06856_longbanana_multi_reference_bench.md) (4,670 判据 / 条目级 +15.82 vs 输出级 +2.9) | [Number Words 同噪声对照](./categories/t2i/papers/2611.06840_number_words_past_ten_t2i.md) (exact-match 分不出松跟随 / 常数 16 反而优) | [UUBench 跨通路六格](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (SF≤TF / SR≤NR) | [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
