# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-298-green.svg">
    <img src="https://img.shields.io/badge/Papers-298-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--06-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--06-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-06)

> **过去十一周我们反复在证明"这个数不可信"。今天换一个更基础的问法：**我们用来做决策的每一个数，都是一个"率"——而业务真正怕的是"量"。** 一个 α=0.10 的风险证书可以和一次 **271.3 mm** 的错误共存，因为率是集体性质、对个体免疫；一个把"该停"和"敢闯"混成一个标量的评分，会让**从不停车的智能体封堵段得分 52.2**、而每次都正确刹车的专家拿 37.8。**加指标没用，得加分母。**
>
> **✅ 供给侧先说清楚**：**11-04 批次到了**（cs.CV 口径 111 篇），但它是一个**纯能力型批次**——机器人、医学、3D、遥感、世界模型。本轮额外做了昨天没做的事：**把 11-04 的 cs.CV+cs.CR+cs.MM 全批 141 篇逐篇看**，T2I 安全直接相关 **0 篇**。全量 86 路查询去重 **534**（窗口 10-30 → 11-05），未收录候选 **520**。空窗第 **十二** 周，证据形态升级：不再是"多路归零"，而是**整批 141 篇里没有一篇** + 534 篇 NSFW 严格词边界扫描 **0 命中** + **18 路专项查询归零**（上轮 14 路，本轮破纪录）。
>
> **⚠️ 本轮新增一条硬教训**：这 141 篇被 86 路查询命中的是 **0 篇**，而本轮 6 篇里有 **3 篇**正是从这 141 篇人工扫出来的。⇒ **当整批供给与主线无关时，主题词检索会整批归零，"零命中"不再能作为"没有供给"的证据**；主线供给为零时，默认动作应改为"全批扫描 + 按结构匹配"。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **阈值 operating point（价码表）** | [Risk Control](./categories/t2t/papers/2611.05851_risk_control_rates_not_magnitudes.md) | **湖南农大 + 湘雅医院**。选择性预测的风险界只约束粗错的**率**，不约束**量**。精确 Clopper–Pearson 标定出的证书与人工地板值不可区分，管线仍吐出 **271.3 mm** 误差（真值 324.6，报 53.3），被接受候选的完整度 **0.94**，150 个答案里 1 个离群点，**α=0.10 的风险界完好无损**。收解剖学准入域 50→55 mm：覆盖只掉 **0.4** 点、最坏误差 271.3→**11.4**；改用阈值压制要推到 **0.94**，代价 **19.0** 点 ⇒ **改定义比调阈值便宜 47 倍**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-06_AI安全每日深度情报.md) |
| **评测口径（奖励敢闯）** | [Failure-Boundary](./categories/t2t/papers/2611.06453_failure_boundary_profiles.md) | **Social Chaos Lab + valeo.ai**。驾驶分 = 完成度 × 罚分，把"该停"和"敢闯"压成一个数：**从不停车的 SimLingo 在封堵段拿 52.2，每次都正确刹车的规则专家只有 37.8、总分垫底 59.2**。拆成 commitment × competence 两条曲线 + 两类平衡准确率（恒停/恒闯都被钉在 **0.5**）。附带：同一条字节级相同命令跑两次 **53.7 vs 32.2**；23 个候选物体 **7 个离线全过、上线全废（78%）**；"会停"≠"会等"（封堵全停的智能体人流等待 6/29）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-06_AI安全每日深度情报.md) |
| **I2I 多轮编辑（商汤）** | [TailSteer](./categories/t2i/papers/2611.06741_tailsteer_multiturn_edit_drift.md) | **商汤研究院 + 港中文 MMLab + 上海 AI Lab**。多轮漂移的修法：**49 步基座 + 1 步微调** → 20 轮视觉稳定；**50 步全用微调模型反而去饱和过平滑** ⇒ **单点干预有效、全程接管毁先验**。推理期模块的代价是它的 3–5 倍（RISE **−3.06/−4.72** vs **−0.56**）。最扎的一行：FreqEdit 把编辑成功率 **16.00→10.00（−6）** 换来 PSNR，而**内容一致性反而 +5.22** ⇒ **只看一致性，最好的是"没改"**。保真监督不用 GT：**未被请求改变的内容就在源图里**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-06_AI安全每日深度情报.md) |
| **指标可分辨性** | [Number Words](./categories/t2i/papers/2611.06840_number_words_past_ten_t2i.md) | **Colorado Boulder**。同噪声单因子对照：过十之后，**exact-match 分不出"松跟随"与"根本不跟"**，**relative-error 甚至偏好常数猜 16**。射程内（2–8）同噪声对 **80–99%** 满足"大请求给更多物体"；射程外重画细噪声能推动数量达数词效果的 **2/3**，而数词**没有方向**。数量写进 latent 能画对 **59%**，写进 prompt 只有 **4%**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-06_AI安全每日深度情报.md) |
| **条目级 vs 输出级（差 5 倍）** | [LongBanana](./categories/t2i/papers/2611.06856_longbanana_multi_reference_bench.md) | **快手可灵 AI 研究院** + 华南师大 + UBC/Vector/CMU/滑铁卢/清华/港科大/港大。90 任务 / **4,670 条原子判据** / 46,700 条人审标签 / 15% 双标（**89.4% / QWK 0.83**）。agentic checklist judge 的改进：**输出级相关只涨 2.9 点（0.8413→0.8707），条目级三元一致 +15.82 点、两端相反错误 −19.28 点** ⇒ **同一个改进，换个分母差 5 倍**。难度权重必须冻结并版本化。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-06_AI安全每日深度情报.md) |
| **平均率的两种谎** | [IntrAA-SD](./categories/t2i/papers/2611.06000_intraa_sd_finetune_attribution.md) | **IIT Kharagpur**。同架构只差微调的 SDXL 版本归因（Juggernaut / RealVis / DreamShaper…），140K 图 / 10 微调 / 15 ID 类 / 20 OOD 类 / 95% JPEG。**99.03% (ID) vs 88.55% (OOD)，同一模型同一次训练**；现有架构级方法同数据重训是 **92.21% / 74.84%** ⇒ **"错的方法"在 ID 上也能到 92%**。风险：风格捷径（学"动漫风=Animagine"而非微调痕迹）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-06_AI安全每日深度情报.md) |
---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **298** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **率证书与 271.3 mm 共存（α=0.10）**（NEW） · **改定义比调阈值便宜 47 倍**（NEW） · **53.7 vs 32.2 同一命令两次**（NEW） · **条目级 +15.82 / 输出级 +2.9**（NEW） | 2026-11-06 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **Risk Control：率不承诺个体（271.3 mm 在 α=0.10 内）**（NEW） · **准入域 0.4 vs 阈值 19.0 覆盖点**（NEW） · **Failure-Boundary：恒停/恒闯都钉 0.5**（NEW） · **SimLingo 52.2 > 专家 37.8**（NEW） | 2026-11-06 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **TailSteer：49+1 步有效、50 步全用过平滑**（NEW） · **FreqEdit 编辑成功率 −6 换保真**（NEW） · **LongBanana 4,670 原子判据 / 条目级 +15.82**（NEW） · **IntrAA-SD 99.03 (ID) vs 88.55 (OOD)**（NEW） | 2026-11-06 |
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
