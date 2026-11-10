# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-316-green.svg">
    <img src="https://img.shields.io/badge/Papers-316-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--10-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--10-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-10)

> **今天六篇没有一篇在说"模型不够强"。它们在说：你下发的那条约束（否定词、水印、细节、奖励上界、阈值、过滤规则）在执行层被平滑掉了，而你用来验收的那个指标，恰好测不出它有没有被平滑掉。**
>
> **✅ 供给侧**：cs.CV **11-06 批次首次到货**（95 篇），11-07/08 周末、11-09/10 未生成 ⇒ 相对上一轮**新增 1 个批次**。按纪律**不加查询路数**，直接全批扫描 **1564 篇 × 十分类**（11-04:554 / 11-05:578 / 11-06:432）。
>
> **⚠️ 空窗第 十五 周**：1564 篇严格 NSFW 词边界 **0 命中**（第三周连续）；`t2_prompt_rewrite` / `t3_i2i_edit_safety` / `t10_video_safety` **三条通道严格归零**；10 路探测逐篇核验后只有 3 篇可用。`t7_threshold` 返 30 篇（历史最高）而**只有 1 篇可迁移**——"有量不等于有供给"第二次生效。
>
> **🎯 本轮最扎的一个数**：NotaryMark 的 α 扫描——**α=0.2 时审计判定已经满分（TPR 100% / FPR 0%），而单图可解信息只有 60.69%**。如果你的验收口径只有 TPR/FPR，这个"完美"是个二分类器的完美。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **否定约束根本没绑上** | [T2I-NSI](./categories/t2i/papers/2611.09304_t2i_negation_suppression.md) | **IIT Jodhpur + Colorado State**。759,869 配对原子 / **916,272 图** / 6 生成器。**反向理解 0.00%**（45.6 万次评测），但**两个 prompt 都画出被否定概念占 13.0–16.9%**，干净成功只 **0.03–0.29%**。Robust NSI 开源 **0.0198–0.0378**、GPT-Image-1.5 **0.0934**。最要命的是 **WEAKLY_REND 占 71.8–74.2%**——"太弱测不到"的残差主导了聚合分，而这个指标和人工的 **κ 只有 0.09**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-10_AI安全每日深度情报.md) |
| **不改模型、只改输入端** | [LeNO](./categories/t2i/papers/2611.06255_leno_frozen_generator_noise.md) | **KAIST AI**。生成器**完全冻结**，只学一个初始噪声的残差输运，奖励是**标量黑盒不必可微**——和我们"输入侧热更新改写"同构。**2 NFE 拿 ImageReward 0.761→1.019（+34%）**，而 **LeNO+BoN 用 100 NFE 三项全超 800 NFE 的 ψ-Sampler**。保真用的是**KL 上界**（退化成 $\|\mu_\theta\|^2$），明确只约束"离先验多远"、**不约束语义**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-10_AI安全每日深度情报.md) |
| **统一模型两通路丢同一样东西** | [UniMore](./categories/t2i/papers/2611.08996_unimore_specificity_unified.md) | **William & Mary + CMU + UIUC + UW–Madison**。生成"物体对属性错"与理解"说不出细节"是**同一个病**。同一次后训练：**WISE +3.59 而 UEval 只 +0.70**；**DOCCI 细节保留 +1.55 而 GenEval 颜色绑定 +8.25**；**ME +21.99 但 IC −0.94 / UGG −1.35**。给 I2I 0/0% 一个新假设：**不是改写没生效，是把编辑要的细节一并抹了**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-10_AI安全每日深度情报.md) |
| **判定满分 ≠ 读得出是谁** | [NotaryMark](./categories/t2i/papers/2611.08985_notarymark_multibit_watermark.md) | **西安交大 + VU Amsterdam + 浙大**。水印被当噪声滤掉，所以改成嵌进扩散一致潜变量。**α=0.2 时 TPR 100%/FPR 0% 而 $BA_{img}$ 仅 60.69%**；容量 8→1024 **TPR 全线 100%** 而 $BA_{img}$ 89.50→**67.04**。**唯一打穿判定的朴素攻击是前置高斯模糊（TPR 83%，FID 135.91）**；**唯一真正有效是继续微调（TPR 32%、FID 155.72）**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-10_AI安全每日深度情报.md) |
| **加了二级复审并没更好** | [Jev Guardrail](./categories/t2t/papers/2611.08845_jev_guardrail_overrefusal.md) | **USC Viterbi**。单门把有害回答从 73.2% 压到 2.4%，代价是良性拒答 **1.2%→10.8%（9 倍）**。**匹配 4% 误杀预算后：重调单门漏过 4.6% vs 三级 3.9%（10 条 vs 11.5 条，不可分）**，报告点上三级反而更差（18.5% vs 14.5%）。**人工审计：输出复审拦下的 13 条里 6 条（46.2%）是无谓拦截。** | [📄 立即阅读](./daily-reports/2026-11/2026-11-10_AI安全每日深度情报.md) |
| **阈值选法决定一切** | [指标教程](./categories/t2t/papers/2611.08048_metrics_scenario_guide.md) | **Erzurum Technical + Firat**。同一组分数、五种合理选法，**代价 274.0–473.5**，而且 **F1 最高的规则代价最贵（0.738↔473.5）、F1 最差的代价最低（0.515↔274.0）**；**验证集最优 ≠ 测试集最优**。**约束规则（TPR≥0.95）在测试集上恰好达标** ⇒ **约束比目标更可迁移**。聚合层级三个答案 **0.691 / 0.700 / 0.857**，朴素区间比 cluster bootstrap 窄 **3 倍**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-10_AI安全每日深度情报.md) |

⏱ **今日一句话**：这六篇的共同结构是——**约束下发之后，绑定发生在别处**；而验收指标如果只测"判定"，就永远看不见"没绑上"。

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **316** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **约束下发之后，绑定发生在别处：否定 0.00% 反向 vs 13–17% 未执行**（NEW） · **判定 100% 而信息 60.69%**（NEW） · **五种阈值选法 274→473.5，F1 最高者最贵**（NEW） · **三级复审在匹配预算下 3.9% vs 单门 4.6%**（NEW） | 2026-11-10 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **Jev：匹配 4% 误杀预算后三级 3.9% vs 重调单门 4.6%，而二级精度仅 53.8%**（NEW） · **指标教程：五种阈值选法代价 274→473.5，F1 最高者最贵**（NEW） · **聚合层级 0.691/0.700/0.857**（NEW） · **留出集误杀超预算 10%→14.0%**（NEW） | 2026-11-10 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **T2I-NSI：反向理解 0.00% 而 13–17% 两个 prompt 都画出，κ 仅 0.09**（NEW） · **NotaryMark：TPR 100% 时可解信息仅 60.69%**（NEW） · **LeNO：冻结生成器 2 NFE 拿 +34%**（NEW） · **UniMore：WISE +3.59 而 UEval 只 +0.70**（NEW） | 2026-11-10 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [词级风险锚点表](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) (保义替换降 3–28 点) | [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Jev 分级护栏的匹配预算对照](./categories/t2t/papers/2611.08845_jev_guardrail_overrefusal.md) (同 4% 误杀：三级 3.9% vs 重调单门 4.6% / 二级精度 53.8%) | [指标教程：阈值选法决定一切](./categories/t2t/papers/2611.08048_metrics_scenario_guide.md) (代价 274→473.5 / F1 最高者最贵 / 聚合 0.691-0.700-0.857) | [StreamLTT 流式风险认证](./categories/t2t/papers/2611.04062_streamltt_risk_certification.md) (换检验 0.0300 vs 换定义 0.0090) | [Alignment Tax 分级退化](./categories/t2t/papers/2611.06476_alignment_tax_graded.md) (0.550 vs 0.981 / ≥96% 来自压制 rejected) | [Risk Control 率不承诺个体](./categories/t2t/papers/2611.05851_risk_control_rates_not_magnitudes.md) (271.3 mm 在 α=0.10 内 / 改定义便宜 47 倍) | [Failure-Boundary 两曲线评测](./categories/t2t/papers/2611.06453_failure_boundary_profiles.md) (恒停/恒闯钉 0.5 / 53.7 vs 32.2) | [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) (阈值只修 1/3–1/2) | [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [StitchEdit 层间兼容探针](./categories/t2i/papers/2611.07922_stitchedit_per_layer_gradient_probe.md) (源深度锁死 CLIP-Dir 0.62 / oracle 也仅 0.79) | [GARM 有界奖励](./categories/t2i/papers/2611.07648_garm_tabo_bounded_reward.md) (单加硬负例泄漏 0.046→0.057) | [TailSteer 尾部校正单点有效](./categories/t2i/papers/2611.06741_tailsteer_multiturn_edit_drift.md) (49+1 步稳 / 50 步过平滑 / FreqEdit −6 编辑率换保真) | [IntrAA-SD 同架构归因](./categories/t2i/papers/2611.06000_intraa_sd_finetune_attribution.md) (99.03 ID / 88.55 OOD) | [Kling 输入侧改写配方](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) (接上生成器保真 −0.07) | [UniForget 跨通路擦除](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (DF 92.7%→37.1%) | [AegisFlow 路径约束](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) (MNC 贴边界) | [VEvo-Harness 三动作路由](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) (看图门控 2% vs 16%) | [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [T2I-NSI 否定约束未绑定](./categories/t2i/papers/2611.09304_t2i_negation_suppression.md) (反向 0.00% vs 未执行 13–17% / WEAKLY_REND 占七成 / κ 0.09) | [UniMore 统一模型特异性损失](./categories/t2i/papers/2611.08996_unimore_specificity_unified.md) (WISE +3.59 而 UEval +0.70 / color binding +8.25) | [VisionValueBench 中立 prompt 的值泄漏](./categories/t2i/papers/2611.05578_visionvaluebench_value_leakage.md) (改写器使 UAI −0.357→+0.182) | [Proxy Audit 代理变量审计](./categories/t2i/papers/2611.07132_proxy_audit_t2i_disparity.md) (0.310 vs 0.312 但姓氏格 0.523) | [LongBanana 图结构原子判据](./categories/t2i/papers/2611.06856_longbanana_multi_reference_bench.md) (4,670 判据 / 条目级 +15.82 vs 输出级 +2.9) | [Number Words 同噪声对照](./categories/t2i/papers/2611.06840_number_words_past_ten_t2i.md) (exact-match 分不出松跟随 / 常数 16 反而优) | [UUBench 跨通路六格](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (SF≤TF / SR≤NR) | [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
