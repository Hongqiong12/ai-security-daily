# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-310-green.svg">
    <img src="https://img.shields.io/badge/Papers-310-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--09-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--09-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-09)

> **过去十三周我们一直在换检索方式（换措辞、加路数、改分类、全批扫描）。今天把池子扩到 5 倍（2000 篇 × 10 分类 × 5 批次），T2I 安全供给仍然是 0。** 所以今天六篇全部来自"方法论形态"通道，而且它们指向同一件事：**六篇里五篇的最大收益来自"把量的是什么写清楚"，不是"把模型做强"；而唯一一篇真正换了检验方法的，结论是"换检验没用"。**
>
> **✅ 供给侧先说清楚**：arXiv 最新批次**仍停在 11-05**（cs.CV 123），**11-06/11-07/11-08 三个批次连续未生成** ⇒ 相对上一轮**新增供给 = 0 篇**。这是本仓库第一次出现"周五批次也未生成"。**按 11-06 立下的纪律，不跑第三遍主题词检索，直接全批扫描。**
>
> **⚠️ 空窗第 十四 周，证据形态第三次换挡**：1987 篇未读候选（**5 倍于上轮的 406 篇**）严格 NSFW 词边界 **0 命中**，`(safety)×(text-to-image/diffusion)` **0 命中**，`(rewrite/sanitize)×(safety)` **0 命中**，`unified generation and editing` **0 命中**，8 路方法论形态探测**实质归零**。⇒ **"是不是检索方式的问题"这条路已经走到头，从下周起主线供给默认按"零"规划。**
>
> **🎯 本轮最扎的一个数**：StreamLTT 实测——两种**专门为相依性设计**的推断（HAC、block bootstrap）把风险差距从 0.0302 只降到 **0.0300**，而换成"可预测风险"这个定义直接到 **0.0090**。**换检验的价值 ≈ 0，换定义的价值 3.3 倍。**

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **换检验 vs 换定义** | [StreamLTT](./categories/t2t/papers/2611.04062_streamltt_risk_certification.md) | **佐治亚大学**。LTT 认证的是**固定总体风险**，但线上损失是相依且非平稳的。改为认证**平均可预测风险** $R_{\text{pred}}=\frac1N\sum\mathbb{E}[L_n\mid\mathcal{F}_{n-1}]$，条件中心化把偏差变成鞅和。硬证据：**HAC 0.0300 / BlockBootstrap 0.0300 / IID 0.0302，而 StreamLTT 0.0090**；interval miss 上基线全部卡在 0.043–0.052，StreamLTT 落在 **0.095–0.097**（α=0.10）；FWER 实测 **0.0902**；认证比例 **76.7%**。消融显示**收益的 76% 来自换定义**（只换定义已到 0.0118）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-09_AI安全每日深度情报.md) |
| **尺子造出的能力崩塌** | [Alignment Tax](./categories/t2t/papers/2611.06476_alignment_tax_graded.md) | **独立研究者**。对齐税是**分级且任务选择性**的：extraction **−0.55**（等价，8/8 种子）、json **−3.52**（点估计在 ±5 内但 item 区间到 **−5.31** ⇒ 不等价）、router **−30.16**。最扎的是**评分器伪影**：严格字符串匹配 **0.550**，规范化后 **0.981**——翻转的 69 条全是 "Item 1" vs "1" 这种表面形式。退化来源极不对称：rejected 压到 **−14.2**、chosen 只动 −0.072~+0.052，**≥96% 来自压制 rejected**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-09_AI安全每日深度情报.md) |
| **中性 prompt 也在表达取向** | [VisionValueBench](./categories/t2i/papers/2611.05578_visionvaluebench_value_leakage.md) | **UW–Madison + 微软亚洲研究院**。价值中立的 prompt 仍产出稳定的价值取向，**六个系统高度一致**（960 场景 × 6 系统 × 4 语言）。换语言位移中位数只 **0.07**，换地理线索只改强度不改方向，**无线索剖面更接近 US 线索**（默认值本身是取向）。最有杀伤力的是 Appendix D.4：**HiDream 的 UAI 维 $\Delta S=+0.602$，从 −0.357 翻到 +0.182** ⇒ 改写器能把语义维度改反。两套判据在 UAI 上**方向相反**（SAE 77.50%/κ=0.513 vs IAE 82.92%/κ=0.731）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-09_AI安全每日深度情报.md) |
| **显式条件锁死原图** | [StitchEdit](./categories/t2i/papers/2611.07922_stitchedit_per_layer_gradient_probe.md) | **港科大**（NeurIPS 2026）。逐层梯度探针证明编辑与深度目标**早期兼容、晚期冲突**。Table 4 是给我们的直接证据：挂**源**深度图使 CLIP-Dir 掉到 **0.62**，**即使给 oracle 目标深度也只到 0.79**，仍输给隐式先验（**0.81**）⇒ **信息给对了，不如给的方式对**。Table 5 更狠：把冲突区也一起训，**DCS 仍是 0.92，CLIP-Dir 掉到 0.75**——代价全在你没看的那个指标里。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-09_AI安全每日深度情报.md) |
| **总分相同，失败位置不同** | [Proxy Audit](./categories/t2i/papers/2611.07132_proxy_audit_t2i_disparity.md) | **弗吉尼亚大学**。借反歧视法的**代理变量**（职业/地理/姓氏 × 50 变体 × 100 图/prompt）。Flux **0.310** vs Imagen **0.312**——总体分不开，但 Imagen 在职业代理上白人过代表 **20%**、SD 在姓氏代理上 **0.523**。姓氏偏差大小取决于"姓氏—国别"相关强度：Schmidt/Chen/Kim 全部 **<0.1**。同 prompt 两张不同地点的图，面部 cosine **0.838**——比例对了，人还是同一个人。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-09_AI安全每日深度情报.md) |
| **加一个更准的部件反而更差** | [GARM / TABO](./categories/t2i/papers/2611.07648_garm_tabo_bounded_reward.md) | **中国电信 TeleAI + 悉尼大学**。奖励引导后训练的三个故障（分布错配/内容混淆/无界过优化）。**Vintage Faded 上只加"内容匹配硬负例"，泄漏从 0.046 涨到 0.057，比什么都不做还差**；两者合起来才降到 0.029。有界化 $B(R)=-\eta\,\mathrm{softplus}((T-R)/\eta)$，$T$ 取真实正例 75 分位：无界最大化目标 **69.543** 但 VBench **0.5774**，有界 **68.722 / 0.5885**——**但两者都低于原模型 0.6166**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-09_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **310** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **换检验救不了错的定义：HAC/bootstrap 0.0300 vs 换定义 0.0090**（NEW） · **尺子把"掉 1 点"报成"崩 44 点"：0.550 vs 0.981**（NEW） · **显式条件锁死原图：CLIP-Dir 0.62 vs 隐式 0.81**（NEW） · **加一个更准的部件反而更差：泄漏 0.046→0.057**（NEW） | 2026-11-09 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **StreamLTT：换检验 0.0300 vs 换定义 0.0090，收益 76% 来自换定义**（NEW） · **Alignment Tax：0.550 vs 0.981、±5 内但区间越界**（NEW） · **退化 ≥96% 来自压制 rejected（−14.2）**（NEW） · **格式断裂退潮 ≠ 内容变对**（NEW） | 2026-11-09 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **VisionValueBench：改写器把 UAI 从 −0.357 翻到 +0.182**（NEW） · **StitchEdit：源深度使 CLIP-Dir 掉到 0.62，oracle 也只 0.79**（NEW） · **Proxy：0.310 vs 0.312 但姓氏格 0.523**（NEW） · **GARM：单加硬负例泄漏 0.046→0.057**（NEW） | 2026-11-09 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [词级风险锚点表](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) (保义替换降 3–28 点) | [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [StreamLTT 流式风险认证](./categories/t2t/papers/2611.04062_streamltt_risk_certification.md) (换检验 0.0300 vs 换定义 0.0090) | [Alignment Tax 分级退化](./categories/t2t/papers/2611.06476_alignment_tax_graded.md) (0.550 vs 0.981 / ≥96% 来自压制 rejected) | [Risk Control 率不承诺个体](./categories/t2t/papers/2611.05851_risk_control_rates_not_magnitudes.md) (271.3 mm 在 α=0.10 内 / 改定义便宜 47 倍) | [Failure-Boundary 两曲线评测](./categories/t2t/papers/2611.06453_failure_boundary_profiles.md) (恒停/恒闯钉 0.5 / 53.7 vs 32.2) | [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) (阈值只修 1/3–1/2) | [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [StitchEdit 层间兼容探针](./categories/t2i/papers/2611.07922_stitchedit_per_layer_gradient_probe.md) (源深度锁死 CLIP-Dir 0.62 / oracle 也仅 0.79) | [GARM 有界奖励](./categories/t2i/papers/2611.07648_garm_tabo_bounded_reward.md) (单加硬负例泄漏 0.046→0.057) | [TailSteer 尾部校正单点有效](./categories/t2i/papers/2611.06741_tailsteer_multiturn_edit_drift.md) (49+1 步稳 / 50 步过平滑 / FreqEdit −6 编辑率换保真) | [IntrAA-SD 同架构归因](./categories/t2i/papers/2611.06000_intraa_sd_finetune_attribution.md) (99.03 ID / 88.55 OOD) | [Kling 输入侧改写配方](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) (接上生成器保真 −0.07) | [UniForget 跨通路擦除](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (DF 92.7%→37.1%) | [AegisFlow 路径约束](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) (MNC 贴边界) | [VEvo-Harness 三动作路由](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) (看图门控 2% vs 16%) | [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [VisionValueBench 中立 prompt 的值泄漏](./categories/t2i/papers/2611.05578_visionvaluebench_value_leakage.md) (改写器使 UAI −0.357→+0.182) | [Proxy Audit 代理变量审计](./categories/t2i/papers/2611.07132_proxy_audit_t2i_disparity.md) (0.310 vs 0.312 但姓氏格 0.523) | [LongBanana 图结构原子判据](./categories/t2i/papers/2611.06856_longbanana_multi_reference_bench.md) (4,670 判据 / 条目级 +15.82 vs 输出级 +2.9) | [Number Words 同噪声对照](./categories/t2i/papers/2611.06840_number_words_past_ten_t2i.md) (exact-match 分不出松跟随 / 常数 16 反而优) | [UUBench 跨通路六格](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (SF≤TF / SR≤NR) | [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
