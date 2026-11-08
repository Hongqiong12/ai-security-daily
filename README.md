# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-304-green.svg">
    <img src="https://img.shields.io/badge/Papers-304-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--08-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--08-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-08)

> **过去十二周我们反复在证明"这个数不可信"。今天换一个更冷的角度：这些数是对的，只是它们保证的东西比我们以为的窄一圈。** 覆盖率保证完好无损（旧类覆盖变化 **≤0.01**），但 **60–67% 的图像这一轮被改了标签**；探针 **AUC 1.000**，而真去干预只降了 **2.5** 点安全率（随机方向还降 **10.5**）；组间 FNR 差距 **15.8→2.6pp** 看起来"公平了"，其中 **74% 是靠该组自己恶化换来的**，每万人多漏 **82 例**，而总体准确率变化全部 **<0.1pp**。**没有一个保证是假的，但它们守的不是我们要的那件事。**
>
> **✅ 供给侧先说清楚**：最新批次只推进到 **11-05**（cs.CV 123 / cs.CR 25），**11-06 未生成、11-07/08 为周末** ⇒ 相对上一轮只多一个批次。本轮把 **11-05 七分类 406 篇全批逐篇扫**（cs.CV 123 / cs.LG 122 / cs.CL 68 / cs.AI 67 / cs.CR 25 / eess.IV 1 / cs.MM 0）：**NSFW 严格词边界 0 命中**、审核类 1 篇、T2I 类 2 篇（均非安全）⇒ 又一个**纯能力型批次**。全量 94 路去重 **490**（11-01:79 / 11-02:117 / 11-03:103 / 11-04:94 / 11-05:85）、未收录 **478**、多路命中 142。
>
> **⚠️ 空窗第 十三 周，证据形态再变一次**：不再是"多路归零"，而是 **19 路专项查询严格归零** + 406 篇全批 0 命中 + 一路高量假阳性（`h3` 回 16 篇，逐篇核验 **0 篇相关**，命中的是 adult / explicit / synthetic 这类宽松词）⇒ 实际 **20 路**。记一条：**有量不等于有供给**。
>
> **🎯 本轮唯一头部公司供给**：腾讯微信视觉 **WeLM-Image**——三个月来第一篇公开的统一 T2I+I2I 技术报告。编辑奖励设计得很硬（乘性门 $r_P$、27 类动作难度 3:5:2、Turbo 单图 4.98s），但**安全全文只有一句"训练前排除 NSFW"**。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **工业统一 T2I+I2I（安全空位）** | [WeLM-Image](./categories/t2i/papers/2611.07392_welm_image_unified_generation_editing.md) | **腾讯微信视觉**。统一生成+编辑的工业技术报告。奖励是**乘性门**：$r_{\text{edit}}=r_P(0.4+0.4r_C+0.2r_Q)$，$r_P$ 不满足时后两项加权全失效（前提不是可补偿项）；27 类编辑动作按难度 **3:5:2** 配比并**剔除两端极简/极难**；过滤算子"保留分数、不断言二值"。MoT+MoE **31.7B 存储 / 5.4B 激活**，Turbo 单图 **4.98 s**（Qwen-Image-Edit-2511 需 **133.04 s**）。**安全部分全文仅一句"训练前排除 NSFW"，零安全评测、零输入侧改写、零输出侧图审**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-08_AI安全每日深度情报.md) |
| **覆盖保证的暗面** | [Coverage Hides Churn](./categories/t2i/papers/2611.07502_coverage_hides_churn_conformal.md) | **Virginia Tech + Accenture**（WACV 2027）。符合预测的覆盖保证有效，但它约束的是**集合的长期频率**，不是**这张图这次的标签**：HPS-Refresh 改变 **53–90%** 图像的旧决策；只动归一化项时受影响图像 **60–67%**、而**旧类覆盖变化 ≤0.01**；撤销 **8.4–52.7%** vs 新增 **0.1–2.5%**（几何不对称：放开容易收回难）；PrefixCP 恢复 **40.9–58.5%** 的差距、代价 **0.49–3.14** 个标签；Table 5 排期让 **49.6–65.8%** 图像集合全变而 macro 覆盖 ≤0.0015。一句原话：**"A stable rule also preserves its mistakes"**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-08_AI安全每日深度情报.md) |
| **AUC 与干预反号** | [Compositional Unalignment](./categories/t2i/papers/2611.07216_compositional_unalignment_lvlm.md) | **Emory University**。**1,400 条** SFT 得 SIUO **69.5** / 过度拒答 **7.0**，反超 **123k 条**四阶段 GRPO 的 **61.1 / 42.3**（数据质量 > 数据量）。Table 3 是教科书级反例：mass-mean 探针 **AUC 1.000 但 Δsafe 仅 −2.5**，**随机方向 AUC 0.678 却 Δsafe −10.5**（更"不准"的方向反而更有效）⇒ **可检出性 ≠ 可干预性**。真能降的：LEACE **−26.3**（连贯性只剩 5.5%）、PCA5-8 **−41.0**（54.2%）、RePE **−45.0**（40.4%）。CMaG 降 65 点且 >98% 连贯；LAT ε=11 伤害 **64.7→22.4** 仍没守住。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-08_AI安全每日深度情报.md) |
| **编辑式水印归因** | [TRACEMARK](./categories/t2i/papers/2611.07632_tracemark_editor_aware_watermark.md) | **Queen's University**。把水印从"能不能解"推进到"**是谁编的**"：editor-aware training，梯度穿过冻结编辑器。最扎的一行是**消融反号**——完整模型 **0.866**，去掉一致性项 **$-\mathcal{L}_{cons}$ 反而升到 0.918（三个域全升）** ⇒ 你声称必要的那一项在拖后腿，指标在奖励"不做事"。编辑前 **0.983 vs 0.980** 几乎打平，编辑后 **0.420 vs 0.920**（差的就是归因能力）；VINE-R 256px **0.062** → 512px **0.997**；换一条指令掉到 **0.635**（极差 0.120–0.975）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-08_AI安全每日深度情报.md) |
| **组间公平的价码** | [Reweighting is not Harmless](./categories/t2t/papers/2611.07258_reweighting_is_not_harmless.md) | **Cedars-Sinai Medical Center**。重加权把组间 FNR 差异从 **15.8pp 压到 2.6pp**——但 **74% 的收窄来自该组自己变差**（相等加权 42%、多数加权 15%）；高基线少数群体 **ΔFNR +6.08pp、每万人多漏 82 例**；**总体准确率变化全部 <0.1pp**，所以任何聚合指标都看不见这件事。log-odds 平移：少数 **−0.26** / 相等 −0.16~−0.18 / 多数 **−0.07**；决策树上还出现 **4.3pp 反向差异**。结论很实用：**改用组特定决策阈值，别动权重**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-08_AI安全每日深度情报.md) |
| **流式护栏的捷径** | [HaloGuard 2.0](./categories/t2t/papers/2611.02134_haloguard2_streaming_output_guard.md) | **Astroware AI + Karunya Institute**。F1 从 72.8 涨到 **83.6**、onset 召回 +5 点，但**匹配安全孪生对**（同长度、同分布、只差有害与否）**332 对只判对 13.9%**，其中"**只在安全孪生上触发**"的比例是 **0%** ⇒ 它学的是"回答像不像有害"，不是"有害在哪"。**37.4% 的误报发生在前 3 个 token**（首 token 分数 0.59 vs 0.24）；同模型判 prompt **95.9** vs 判回答 **71.9**。工程细节全是坑：线性头必须**零初始化**（RMS 4.2 → 梯度 >500 直接塌成常数）、**不能 sequence packing**（隐状态差异 0.23）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-08_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **304** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **保证还在、判断已经换了：覆盖 ≤0.01 变而 60–67% 图像改判**（NEW） · **AUC 1.000 而 Δsafe 仅 −2.5（随机方向 −10.5）**（NEW） · **组间 FNR 差收窄 74% 靠恶化该组**（NEW） · **消融反号：去掉一致性项 0.866→0.918**（NEW） | 2026-11-08 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **Reweighting：FNR 差 15.8→2.6pp 但 74% 靠该组恶化、每万人多漏 82 例**（NEW） · **HaloGuard：匹配对只判对 13.9%、安全孪生触发 0%**（NEW） · **37.4% 误报在前 3 token**（NEW） · **线性头必须零初始化**（NEW） | 2026-11-08 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **WeLM-Image：乘性门奖励 $r_P$ 与安全全文仅一句**（NEW） · **Coverage：撤销 8.4–52.7% vs 新增 0.1–2.5%**（NEW） · **Compositional：1,400 条 SFT 反超 123k 条 GRPO**（NEW） · **TRACEMARK：编辑后 0.420 vs 0.920**（NEW） | 2026-11-08 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [词级风险锚点表](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) (保义替换降 3–28 点) | [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Risk Control 率不承诺个体](./categories/t2t/papers/2611.05851_risk_control_rates_not_magnitudes.md) (271.3 mm 在 α=0.10 内 / 改定义便宜 47 倍) | [Failure-Boundary 两曲线评测](./categories/t2t/papers/2611.06453_failure_boundary_profiles.md) (恒停/恒闯钉 0.5 / 53.7 vs 32.2) | [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) (阈值只修 1/3–1/2) | [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [TailSteer 尾部校正单点有效](./categories/t2i/papers/2611.06741_tailsteer_multiturn_edit_drift.md) (49+1 步稳 / 50 步过平滑 / FreqEdit −6 编辑率换保真) | [IntrAA-SD 同架构归因](./categories/t2i/papers/2611.06000_intraa_sd_finetune_attribution.md) (99.03 ID / 88.55 OOD) | [Kling 输入侧改写配方](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) (接上生成器保真 −0.07) | [UniForget 跨通路擦除](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (DF 92.7%→37.1%) | [AegisFlow 路径约束](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) (MNC 贴边界) | [VEvo-Harness 三动作路由](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) (看图门控 2% vs 16%) | [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [LongBanana 图结构原子判据](./categories/t2i/papers/2611.06856_longbanana_multi_reference_bench.md) (4,670 判据 / 条目级 +15.82 vs 输出级 +2.9) | [Number Words 同噪声对照](./categories/t2i/papers/2611.06840_number_words_past_ten_t2i.md) (exact-match 分不出松跟随 / 常数 16 反而优) | [UUBench 跨通路六格](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (SF≤TF / SR≤NR) | [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
