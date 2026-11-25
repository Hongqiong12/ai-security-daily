# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-346-green.svg">
    <img src="https://img.shields.io/badge/Papers-346-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--26-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--26-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-26)

> **今天六篇把「判安全」这件事从「一个总数」拆成按部件、按栏、按仪器。最扎的一刀来自快手可灵：单 slot 的「外科式替换风险锚点」会被文本编码器扩散到全句，59%–74% 的改写还擅自加了场景和光照。**
>
> **✅ 供给侧**：网页端十分类 `/list/<cat>/recent?show=2000` 串行全批扫描，公告批次 **11-19→11-25**（740/718/563/1442/**845**）；全批池 **4308 篇**（1982 篇带摘要），复用昨日 1871 条摘要缓存回填 1566、仅新抓 **416** 篇，主题词 **26 路** + 形态 **12 路**全部本地正则复现、零第二次检索请求。`t2_prompt_rewrite` 严格词表 3 命中**全为误命中**（空窗第 **19** 周），但 ② 全批扫描 + ④ 厂商兜底「捡」出本轮头条 HinT —— **零命中不等于供给为零**最有力的一次验证。
>
> **🎯 头部公司首次命中 2 篇**：**KlingAI Research（快手可灵）** 的 HinT、**Adobe Inc.** 的 TIDE；另有阿里 Qwen-Image-2512 / Qwen-Image-2.1 / Qwen-Image-Edit-2511 作为被测主干出现在 3 篇里。**T2I 占比 83.3%，历史最高。**
>
> **⚠️ 仍零供给**：I2I 安全改写方法 / 统一生成-编辑改写面 / GRPO 安全改写 / 跨语言安全改写 / 风险知识召回护栏（`t14_policy_guard` 5 命中全 RAG、0 可迁移，「有量不等于有供给」**第六次**）/ i2v-t2v 生成安全（主线⑥不给建议）。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **外科式替换在表示层不成立** | [HinT：蒸馏修正而非改写](./categories/t2i/papers/2611.31048_hint_distill_correction_not_rewrite.md) | **KlingAI Research 快手可灵 + 复旦 + 华南师大 + 浙大**（主干 Qwen-Image-2512 / SD3.5-M / FLUX.2-klein）。critic 把 **10 词 → 22–25 词**，**59%–74%** 修订加了未要求的场景/光照；**单 slot 编辑经文本编码器传播到全句**；改写习惯 **2.2%→98–100%（2 轮内）**而 HinT **<4%**；twin 速度差使 GenEval2 EMA **+11.4/+11.1/+1.9**，比标量奖励 RL 高 **21.6 点**，训练 **+<4%**、推理零开销。⇒ 输入改写有效性上界补第五栏「表示层漂移」，但**修法是换监督单位，不是加严改写**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **防护成功率几乎全是假的** | [BODYBENCH](./categories/t2i/papers/2611.31774_bodybench_nudification_defense_audit.md) | **密歇根 + 普林斯顿**（11-25 新批次）。648 合成主体 × 11 掩码；三种 harm-aligned 判据（性化/自然度/可辨认性）替代 PSNR。四种防护仅 **AdvPaint 一个配置**达 DefenseScore **0.951** 且要求掩码**精确对齐**；dilation d=7 掉 **0.739**，d=15/31 全崩；**PSNR/SSIM 与裸体化防护基本不相关**。⇒ 「掩码精确对齐」在结构上等价于评测集重叠；图审 AB 必须补三栏判据 + 扰动格。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **一个阈值先杀掉最细的编辑** | [TIDE：每部件自己的预算](./categories/t2i/papers/2611.32407_tide_per_instruction_token_budget.md) | **IIT Delhi + Adobe Inc.**（主干 Qwen-Image-Edit-2511）。**Theorem 2 证明 part-agnostic 规则无法保证异构预算**；单一全局阈值在 **89%** 的 MICE-Bench 图上破坏至少一个编辑；per-part 少丢 **48%/最高 77%** 且 **2.09×→2.20× 更快**。⇒ 「改写强度分级下沉」第一次有可证伪定理与「分档不牺牲延迟」实测；I2I 0/0% 的**第八种**归因。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **完整成功率 0.0% 是判据坏了** | [CRIE-Agent / CRIE-S](./categories/t2i/papers/2611.27388_crie_redundant_instruction_final_intent.md) | **中山大学**（主干 Qwen-Image-2.1 / FLUX.2-klein-4B）。10,000 条冗余/撤销编辑指令；五个后端直接编辑 O. 54–58 / A. 69–84 / R. 57–70 而**完整成功全部 0.0%**；CRIE-Agent 折叠成最终编辑目标 + 从源图重执行，抬到 **27.5–50.0%**。⇒ 0/0% 的**第九种**归因：验收判据没有可判的正例；报「方向覆盖数」而非 0/1。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **编辑后水印存活率有基线了** | [VeriOrigin](./categories/t2i/papers/2611.30523_veriorigin_watermark_edit_survival.md) | **北理工 + 澳门理工 + 深北理莫斯科 + 宁大 + 深大 + 中关村实验室**（兑现 11-25 优先精读）。XOnet 可逆 CNN + 两阶段训练；clean 定位 F1 **0.995**、JPEG70 payload **0.949**、Gaussian σ23 **0.998**、resize 0.35 **0.999**，载荷代价 ≤**2.3 F1 点**，无损通道 **bit-exact 恢复**。⇒ 判定 / 信息 / 事件三栏做进同一框架；属**输出凭证层**，不阻止风险内容生成。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **安全率下降有一半是尺子写的** | [Measurement Artifacts](./categories/t2t/papers/2611.32848_quantized_eval_instrument_artifacts.md) | **COMSATS + Middlesex**（迁移）。$\Delta_{measured}=\Delta_{true}+\Delta_{inst}$：与量化交互的仪器误差能**造出或反转**效应。基线拒答检测器只召回 **33.3%** 的拒答（corrected **80.0%**）；人工校准后 4-bit harmful compliance **+2.6 点**而检测器记的 refusal 降 **4.7 点**；同一模型四种评分给 **+9.8/+0.8/−13.6/−7.3**；**LLM.int8() 非 batch-invariant**（重排 batch 改变答案数达量化本身的 **57–119%**）。⇒ 与 overlap 下界、评测集重叠并列的**第三种读数污染**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |

⏱ **今日一句话**：**别再调那个总数了**。先把「五栏归因（含改写表示层漂移）、三栏图审判据、按部件/方向覆盖数的分流输出、检测器人工校准、生成侧+判定侧 serving setup 指纹」补进验收；输入改写优化预算继续冻结，重心留在出图侧生成过程干预与验收单位重构。

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **346** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **判定的单位错了（热点三十三）**（NEW） · **按部件/按栏/按仪器拆开一个总数**（NEW） · **头部公司首次命中 2 篇：快手可灵 + Adobe**（NEW） | 2026-11-26 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **量化后安全率下降有一半是尺子写的**（NEW） · **拒答检测器只召回 33.3% 的拒答**（NEW） · **第三种读数污染：测量仪器交互可造出/反转效应**（NEW） | 2026-11-26 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **HinT：单 slot 外科替换扩散到全句、改写 59–74% 加未要求场景**（NEW） · **BODYBENCH：掩码精确对齐才 0.951**（NEW） · **TIDE Theorem 2 分级是数学必要**（NEW） · **CRIE-S 完整成功 0.0%**（NEW） | 2026-11-26 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [Risk-certified 约束式策略选点](./categories/t2t/papers/2611.20156_risk_certified_prompt_optimization.md) (max 放行率 s.t. 漏过 ≤ α / LTT+Clopper–Pearson) | [词级风险锚点表](./categories/t2t/papers/2611.02348_which_words_a_model_fears.md) (保义替换降 3–28 点) | [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Measurement Artifacts 量化评测仪器项](./categories/t2t/papers/2611.32848_quantized_eval_instrument_artifacts.md) (检测器召回 33.3%→80.0% / +2.6 vs 4.7 点 / 8-bit 非 batch-invariant) | [Latent Safety Filter Conservatism](./categories/t2t/papers/2611.23685_latent_safety_filter_conservatism.md) (overlap 0.96→0.44 / 误杀 0.302→0.161) | [Operating-Point Contamination](./categories/t2t/papers/2611.29629_operating_point_contamination.md) (FNMR 虚高 3.6×→13.9× / N_eff 下限) | [The Vulnerability Window](./categories/t2t/papers/2611.27155_vulnerability_window_quantized_judges.md) (1.1–12.3% 成对翻转 / 聚合准确率只动 0.03 点) | [Your Judge Inherits Your Prompt](./categories/t2t/papers/2611.26881_judge_inherits_prompt_directional_bias.md) (接受偏置虚高 +29.5 点，拒绝侧不对称) | [Operating-Point Failure 冻结护栏失效](./categories/t2t/papers/2611.19216_operating_point_failure_frozen_guardrail.md) (FPR 1.01%→15.12% 而 AUROC ≤0.0058 / 重设 9/9 恢复) | [Jev 分级护栏的匹配预算对照](./categories/t2t/papers/2611.08845_jev_guardrail_overrefusal.md) (同 4% 误杀：三级 3.9% vs 重调单门 4.6% / 二级精度 53.8%) | [指标教程：阈值选法决定一切](./categories/t2t/papers/2611.08048_metrics_scenario_guide.md) (代价 274→473.5 / F1 最高者最贵 / 聚合 0.691-0.700-0.857) | [StreamLTT 流式风险认证](./categories/t2t/papers/2611.04062_streamltt_risk_certification.md) (换检验 0.0300 vs 换定义 0.0090) | [Alignment Tax 分级退化](./categories/t2t/papers/2611.06476_alignment_tax_graded.md) (0.550 vs 0.981 / ≥96% 来自压制 rejected) | [Risk Control 率不承诺个体](./categories/t2t/papers/2611.05851_risk_control_rates_not_magnitudes.md) (271.3 mm 在 α=0.10 内 / 改定义便宜 47 倍) | [Failure-Boundary 两曲线评测](./categories/t2t/papers/2611.06453_failure_boundary_profiles.md) (恒停/恒闯钉 0.5 / 53.7 vs 32.2) | [Spot-Stop 三项分解](./categories/t2t/papers/2611.01125_what_does_a_safety_label_measure.md) (阈值只修 1/3–1/2) | [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [DSC 延迟语义承诺](./categories/t2i/papers/2611.25929_deferred_semantic_commitment.md) (问句+✓ 使 Endorsed 15.3%→41.3% / 语义一字未改) | [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [HinT 蒸馏修正而非改写](./categories/t2i/papers/2611.31048_hint_distill_correction_not_rewrite.md) (单 slot 扩散到全句 / 改写习惯 2.2%→98% 而 HinT <4% / KlingAI) | [TIDE 每部件预算](./categories/t2i/papers/2611.32407_tide_per_instruction_token_budget.md) (Theorem 2 / 89% 破坏预算 / 2.09×→2.20× / Adobe) | [VeriOrigin 编辑后水印](./categories/t2i/papers/2611.30523_veriorigin_watermark_edit_survival.md) (JPEG70 0.949 / 定位 F1 0.995 / bit-exact 恢复) | [GuideCache / 静默文本改写](./categories/t2i/papers/2611.25382_silent_text_rewrite_guidance_cache.md) (word acc 62%→46% 而图像级分不动 / CFG guidance 项归因) | [HOSE 层次正交擦除](./categories/t2i/papers/2611.30592_hose_hierarchical_orthogonal_erasure.md) (harmful −80% / FID 34.87 但 %HARM 非最优) | [EBSG 子概念空间引导](./categories/t2i/papers/2611.20623_ebsg_example_based_spatial_guidance.md) (SR 97.2/96.2/84.2/97.4 而 NR ≤1.4 / FID 6.31 vs 7.83) | [P2E 冗余监督](./categories/t2i/papers/2611.27229_p2e_supervision_redundancy.md) (生成增益 25× 而改写器只差 +0.14 HPS v2) | [Tripwire-WM 伪造事件报告](./categories/t2i/papers/2611.25226_tripwire_wm_forgery_evident.md) (伪造接受 0% vs 55.0% / 真图 ≥99% @10⁻⁶ FPR) | [StitchEdit 层间兼容探针](./categories/t2i/papers/2611.07922_stitchedit_per_layer_gradient_probe.md) (源深度锁死 CLIP-Dir 0.62 / oracle 也仅 0.79) | [GARM 有界奖励](./categories/t2i/papers/2611.07648_garm_tabo_bounded_reward.md) (单加硬负例泄漏 0.046→0.057) | [TailSteer 尾部校正单点有效](./categories/t2i/papers/2611.06741_tailsteer_multiturn_edit_drift.md) (49+1 步稳 / 50 步过平滑 / FreqEdit −6 编辑率换保真) | [IntrAA-SD 同架构归因](./categories/t2i/papers/2611.06000_intraa_sd_finetune_attribution.md) (99.03 ID / 88.55 OOD) | [Kling 输入侧改写配方](./categories/t2i/papers/2611.04916_kling_prompt_enhancement_reward_chain.md) (接上生成器保真 −0.07) | [UniForget 跨通路擦除](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (DF 92.7%→37.1%) | [AegisFlow 路径约束](./categories/t2i/papers/2610.39825_aegisflow_nonmyopic_path_safe_guidance.md) (MNC 贴边界) | [VEvo-Harness 三动作路由](./categories/t2i/papers/2610.39158_vevo_harness_causally_guarded_agentic_generation.md) (看图门控 2% vs 16%) | [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [BODYBENCH 裸体化防护审计](./categories/t2i/papers/2611.31774_bodybench_nudification_defense_audit.md) (0.951 仅在掩码精确对齐 / PSNR 不相关 / 三栏判据) | [CRIE-S 冗余指令编辑](./categories/t2i/papers/2611.27388_crie_redundant_instruction_final_intent.md) (完整成功 0.0%→27.5–50.0% / 10,000 条) | [SAE-Audit 擦除残留审计](./categories/t2i/papers/2611.30117_sae_audit_concept_erasure_residue.md) (nudity 0.00→注入 0.48–0.77 / 随机 ≤0.06) | [Batch-Dependent Non-Determinism](./categories/t2i/papers/2611.30545_batch_dependent_nondeterminism_t2i.md) (bit-identity 全 0.0 / SSIM 0.580, 0.229 / serving setup 指纹) | [Unimodal Shortcuts](./categories/t2i/papers/2611.27339_unimodal_shortcuts_scene_intent.md) (灰图纯文本探针 0.9645–0.9846 AUROC / 四路控制上界 0.500) | [AnimalFarm](./categories/t2i/papers/2611.27905_animalfarm_hateful_image_audit.md) (92.1% 出图 / 95.9% 仇恨 / 最强图审 recall 73.9%) | [EditSafetyBench 图文联合安全](./categories/t2i/papers/2611.26569_editsafetybench_text_aware_vision_blind.md) (UIR 87.1% vs UNR 24.2% / 5,940 配对) | [CuRSE-Bench 文化盲区](./categories/t2i/papers/2611.20821_curse_bench_cultural_blind_spots.md) (10,709+2,648 / 6 地区 × 10 harm axes) | [T2I-NSI 否定约束未绑定](./categories/t2i/papers/2611.09304_t2i_negation_suppression.md) (反向 0.00% vs 未执行 13–17% / WEAKLY_REND 占七成 / κ 0.09) | [UniMore 统一模型特异性损失](./categories/t2i/papers/2611.08996_unimore_specificity_unified.md) (WISE +3.59 而 UEval +0.70 / color binding +8.25) | [VisionValueBench 中立 prompt 的值泄漏](./categories/t2i/papers/2611.05578_visionvaluebench_value_leakage.md) (改写器使 UAI −0.357→+0.182) | [Proxy Audit 代理变量审计](./categories/t2i/papers/2611.07132_proxy_audit_t2i_disparity.md) (0.310 vs 0.312 但姓氏格 0.523) | [LongBanana 图结构原子判据](./categories/t2i/papers/2611.06856_longbanana_multi_reference_bench.md) (4,670 判据 / 条目级 +15.82 vs 输出级 +2.9) | [Number Words 同噪声对照](./categories/t2i/papers/2611.06840_number_words_past_ten_t2i.md) (exact-match 分不出松跟随 / 常数 16 反而优) | [UUBench 跨通路六格](./categories/t2i/papers/2611.04467_uniforget_cross_pathway_concept_unlearning.md) (SF≤TF / SR≤NR) | [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
