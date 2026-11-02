# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-280-green.svg">
    <img src="https://img.shields.io/badge/Papers-280-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--03-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--03-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-03)

> **为什么要关注本仓库？** 上周的结论是"风险住在我们看不见的那一半"；这一周往下挖了一层：**不是没有观测通道，而是那条通道被当成常数积掉了。** 六篇各自指出一个"本该被单独记账、却被边际化"的自由度——**聚合顺序 / 这是第几次尝试 / 在输出空间还是分布空间量 / 分析单位是部件还是配置 / 用的是哪份措辞 / 用哪个指标当约束**——然后把它从假设改成测量。六篇里**没有一篇的主贡献是"训一个更强的模型"**。
>
> **✅ 供给侧先说清楚**：arXiv 最新批次只从 **10-29 推进到 10-30**（10-31/11-01 周末、11-02/11-03 未生成），**只新增 1 个批次 51 篇**，候选池 301→**319**（其中 268 篇是前几轮的补筛）。**薄供给轮**。而 T2I 输入侧改写与 I2I 编辑改写仍然为零：**12 路专项查询同时归零**（含 3 路 11-02 才新写的）、**全池 319 篇 NSFW 关键词只命中 1 篇**（且是定性威胁建模）⇒ **连续第八周零供给**。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **I2I 正例标准（同行同场景）** | [WeGenEditBench](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) | **腾讯微信视觉 + 中山大学**（58 页）。诊断 **high-score paradox**：单个显眼编辑成功 ≠ 所有耦合要求都满足。做法是**先逐条判原子要件、再汇总成维度**（EG/PR/VQ/DS）。**2,740 instance / 148 任务类型 / 15 配置 / 194,836 条 item 记录**。硬证据：某模型 **PR=4.175 全场第一，Overall 只排第五**（3.841）；定向收益是全量的 **1.07–1.85×**。**这是"可判的正例标准"的生成方式，直接解 I2I 0/0%**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-03_AI安全每日深度情报.md) |
| **I2I 分流（0/0% 的第四种归因）** | [RetryRoute](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) | **北师大 + 南洋理工**。**sticky failure**：重试成功率只有首次的 **17%–53%**（按模型 0.23–0.39×）⇒ **"失败后再试"不是重新抽一次**，单次通过率系统性错估。状态=失败计数向量，Bellman 精确解 **0.35 ms**。最扎人的是它把 **Rewrite-retry 当强基线认真实现**：盲改写 80.82/82.42 vs 同模型重试 81.74/81.74 ⇒ **改写≈盲重试**，而作为路由里一个动作最多 +2.2 点。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-03_AI安全每日深度情报.md) |
| **输入侧原位替换（同一动作）** | [ERASE](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) | 华南理工。定义**注入依赖 $I$**（两视图输出分布的对称 KL）。**ARGUS 把 ASR 打到 ≈0，但 $I$ 只从 6.26→5.15（−18%）** ⇒ **拦住≠拿掉**。ERASE 到 **0.0095**，且被攻击时仍答对 60.1%（ARGUS 33.1%）。方法：**原位擦除视图 + 在策自蒸馏**，**训练时造参考、推理时不加模块**——与"输入侧改写、不动生成模型"同构。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-03_AI安全每日深度情报.md) |
| **PORN/VULG 边界（唯一 NSFW 论文）** | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) | **NYU + 乔治敦 + ASU**。**风险不是一个部件，是一组配置**：拆成 **S（性内容）× I（身份）** 两轴。**likeness prompting** 用"作品名+角色名+属性"绕过只查名字的过滤器 ⇒ **过滤器在查符号，风险在指称**。LoRA 能把移除的概念装回去 ⇒ **擦除的治理止于权重发布**。**全池唯一一篇讨论 NSFW 的工作。** | [📄 立即阅读](./daily-reports/2026-11/2026-11-03_AI安全每日深度情报.md) |
| **评测仪器校准（尺子先自检）** | [Prompt Lottery](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) | **Upwork**（55 页）。释义改写（只动表面不动判据）让 **κ 从 0.89 掉到 0.24**，是人类的 **6–9 倍**。**反直觉核心：越"客观"越不稳**——SQuAD v2（二元客观）Top-1 翻转 **43.3%**、τ=0.17；MTBench（主观对话）翻转 **0%**。且**语义相似度高≠判定一致**（Pearson 0.157 / Spearman −0.022）⇒ **embedding 保真度量对稳定性零信息量**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-03_AI安全每日深度情报.md) |
| **类目阈值（指标选错会反噬）** | [FYC 分组阈值](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) | **FSU + UCF**。同一方法只换约束指标：**DP → 2 改善 / 1 不变 / 1 恶化**（且事前不可预测）；**FPR 条件化 → 4/4 全改善**。零成本阶段：per-group Youden-J + logit 平移、无梯度。**Xception FPR 12.96%→1.50%、AUC 98.58→99.85**，打赢需全量重训的专用公平架构（投入差 11 倍）。**eq-TPR 是退化的**：只压漏过率，最优解是全拦。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-03_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **280** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **被边际掉的那一维**（NEW） · **ARGUS：ASR≈0 但依赖只降 18%**（NEW） · **二元客观判定排序翻转 43.3%**（NEW） · **DP 反噬 / FPR 全改善**（NEW） | 2026-11-03 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **释义让 κ 从 0.89 掉到 0.24**（NEW） · **越客观越不稳：SQuAD 翻转 43.3% / MTBench 0%**（NEW） · **DP 反噬而 FPR 条件化全改善**（NEW） · **eq-TPR 退化：只压漏过=全拦**（NEW） | 2026-11-03 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **先要件后汇总：PR 第一而 Overall 第五**（NEW） · **重试成功率只有首次的 17–53%**（NEW） · **注入依赖 6.26→0.0095**（NEW） · **风险是 S×I 的配置**（NEW） | 2026-11-03 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [FYC 分组阈值校准](./categories/t2t/papers/2610.37882_fyc_fpr_disparity_threshold.md) (FPR 12.96→1.50 / DP 会反噬) | [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Prompt Lottery 释义让 κ 掉到 0.24](./categories/t2t/papers/2610.38076_prompt_lottery_paraphrase_judge.md) (SQuAD 翻转 43.3% / MTBench 0%) | [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [ERASE 原位擦除+在策自蒸馏](./categories/t2i/papers/2610.41307_erase_injected_region_onpolicy_distill.md) (注入依赖 6.26→0.0095) | [RetryRoute 粘性失败路由](./categories/t2i/papers/2610.41460_retryroute_sticky_failure_routing.md) (重试只有首次 17–53%) | [AIG-NCII 配置论](./categories/t2i/papers/2610.37949_aig_ncii_configured_not_built.md) (S×I 两轴 / likeness prompting) | [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [WeGenEditBench 先要件后汇总](./categories/t2i/papers/2610.41210_wengenedit_bench_checklist_aggregation.md) (腾讯微信视觉 / PR 第一而 Overall 第五) | [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
