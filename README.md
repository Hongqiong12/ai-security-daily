# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-286-green.svg">
    <img src="https://img.shields.io/badge/Papers-286-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--04-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--04-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-04)

> **为什么要关注本仓库？** 前两周的结论是"被边际掉的那一维""风险住在看不见的那一半"；这周再往下一层：**不是要不要拆，而是拆到哪一层才能动手。** 六篇各自把测量单位往下压了一级——**prompt→词 / 聚合分→链路四段 / "忘了"→通路 / 终点→路径 / 布尔→根因 / 一个 label score→阈值+重叠+顺序**——然后在你第一次能干预的那一层停下来。六篇里**没有一篇的主贡献是"训一个更强的模型"**。
>
> **✅ 供给侧先说清楚**：arXiv **供给解冻**，批次从 10-30 一次推进到 **11-03**（新增 10-31 / 11-01 / 11-02 / 11-03 **四个批次、335 篇**），去重 **600** / 排除已收录后 **592 候选**。但 T2I 安全仍然为零：**全池 592 篇按 NSFW 严格词边界扫描 0 命中**、（生成∩安全∩改写）三条件交集只剩 **1 篇且其 rewrite 指 generate-verify-rewrite 循环**、**13 路专项查询归零** ⇒ **T2I 输入侧改写 + I2I 编辑改写连续第九周零供给**。这轮的空窗证据强于前八轮，因为供给已经解冻了。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **输入侧改写（工业配方）** | [Kling PE](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) | **快手可灵团队**（38 页）。**本轮唯一一篇头部公司公开的输入侧改写配方**。三层对齐（Format × **Lexicon** × **Sentence patterns**，只对格式会漂）；数据**从 caption 反向构造**并拒绝"骨架泄漏" prompt；三阶段训练里**文本级 RL 不渲染一帧**（保真 4.27→**4.45**）。最扎的一行：**接上生成器做 RL 之后保真掉回 4.38**（≥4 占比 86.67→**83.50**）⇒ **"用图像一致性奖励换语义保真"的实测价码**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-04_AI安全每日深度情报.md) |
| **权重侧擦除（失效边界）** | [UniForget / UUBench](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) | **中科院自动化所 + 字节跳动 + 港中深 + 上交**。**生成侧 TF 100.0 而 DF 只有 24.0** ⇒ 画不出来≠不知道；两通路**直接组合只到 31.3**；**N=1→30 时理解侧 DF 92.7%→37.1%、邻居 NR 剩 41.8%** ⇒ **权重侧擦除随概念数线性崩塌、且没有"只擦这个"的精度**。六格记账 + 写死 `SF≤TF`、`SR≤NR`。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-04_AI安全每日深度情报.md) |
| **约束满足（改写幅度铁律）** | [AegisFlow](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) | **清华自动化系**。**贴着约束边界走的 min-norm 控制器，约束最好、目标最差**：MNC 的 ID **0.920 最高**，但 CLIP/LPIPS 都输。⇒ **"edit rate 越小越好"在数学上就是 min-norm，会把改写后的 prompt 推到"风险刚好等于阈值"**。应改成留裕度 `τ−δ`。图像任务上比 MNC 快 **16.3%**，控制任务上慢 **10×**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-04_AI安全每日深度情报.md) |
| **I2I 0/0%（该不该改写）** | [VEvo-Harness](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) | **阿里淘天 + 清华**（ICLR'27 投稿）。直接写 *"prompt-only interventions lack fine-grained attribution and pixel-grounded feedback"*。**有害补丁入库率：不门控 33–40% / 纯文本门控 16% / 看图门控 2%** ⇒ 8 倍差距全在"验收看不看图"。**HSP 三动作路由 vs Rewrite-Only +4.0%** ⇒ 0/0% 可能是**把 resample/tune 的活派给了改写**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-04_AI安全每日深度情报.md) |
| **风险锚点（降到词级）** | [Which Words a Model Fears](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) | **美国东北大学**。单个**保义同义词替换**降拒答 **3–28 点**，惰性词对照 **≤2 点**；**71,583 词**恐惧表半集复现 **ρ=0.95**。最反直觉：**手挑的 24 个"安抚词"没有一类有效，"收纳"类反而 +0.075** ⇒ 靠人工直觉写安全同义词库会系统性失败。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-04_AI安全每日深度情报.md) |
| **阈值 operating point（该不该调）** | [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) | **Wiqonn**（44 页）。**一个 label score 混了三样东西**：`R−A = 阈值项 + 重叠项 + 对内顺序项`。**一个共享阈值只能修 1/3–1/2**，剩下 **6.9 点全是重叠**；recentering 在 **AUROC<0.70 时五个模型里三个变差**。附带：某 benchmark 的**图片尺寸单独判标签 82.3%**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-04_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **286** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **拆到能动手的那一层**（NEW） · **接上生成器后保真 4.45→4.38**（NEW） · **擦除随概念数 92.7%→37.1%**（NEW） · **共享阈值只能修 1/3–1/2**（NEW） | 2026-11-04 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **词级恐惧表：保义替换降 3–28 点**（NEW） · **手挑安抚词全部无效**（NEW） · **Spot-Stop：阈值只能修 1/3–1/2**（NEW） · **AUROC<0.70 禁止免标注校准**（NEW） | 2026-11-04 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **Kling 三层对齐与掉保真价码**（NEW） · **跨通路擦除随概念数崩塌**（NEW） · **贴边界控制器：约束最好目标最差**（NEW） · **纯改写不够：Rewrite-Only 输 4.0%**（NEW） | 2026-11-04 |
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
