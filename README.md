# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-274-green.svg">
    <img src="https://img.shields.io/badge/Papers-274-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--11--02-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--11--02-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-11-02)

> **为什么要关注本仓库？** 过去三周我们一直在"调模型"这一侧使劲（abstain 头 / 反事实训练 / 调 alpha / 调阈值 / 补数据）。这一轮六篇指出的是：**风险住在我们看不见的那一半，而修法不是把模型变强，是把观测通道补上。** 六篇里没有一篇的结论是"模型不够大"——32B 零样本在定位任务上全场最差（mIoU 4.72），235B 在编辑一致性上也过不了 65%。
>
> **✅ 供给侧先说清楚**：arXiv 最新批次从 **10-27 推进到 10-29**，**10-28 与 10-29 两个批次首次出现**，候选池从 277 扩到 **301 篇**。⇒ 自 10-27 以来第一次拿到真正的新供给，上一轮"存量深挖"的判断对本轮不适用。**但 T2I 输入侧安全改写仍是零**：七个专项查询同时归零（含三个本轮为 I2I 编辑安全新写的措辞），新批次 123 篇的 NSFW 关键词全扫描 **0 命中** ⇒ **连续第七周零供给**。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I 输出侧图审（天花板在哪）** | [FVH-Bench](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) | **香港中文大学（深圳）+ 纽约州立大学布法罗**。提出 **functional visual harm**：风险来自图**使能**了什么，不只是**描绘**了什么。11 个生图器平均拒答率 **2.45%**、平均 THR **4.46/5**；`PIC×THR` Spearman **0.96**（安全与能力**同向**）。五个专用图审召回 **1.60%–44.00%**，FPR 全在 0–5.5%。**同模型同 policy：纯图 14.60% → 图+prompt 43.00%（+28.4）**。Condition-Decomposed 用 **8B 骨干拿 80.40%**，比同骨干通用策略高 **30.60**，FPR 仍 0，成本 1.57×。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-02_AI安全每日深度情报.md) |
| **I2I 改写 0/0%（判定侧病根）** | [V-CAPE](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) | **Amazon**。40K 源—目标对，3 标注员多数表决 **Fleiss κ=0.77** ⇒ **任务良定义、人类判得动**。而所有 VLM（4B–235B）**accuracy 全部 <65%**，细粒度（纹理/光照/背景/材质）**接近随机**，auto-prompt 只 +3–5 点。零样本 accuracy **51.5% 但 F1 6.7%**（退化成全判一类）⇒ **只报 accuracy 会把"全判一类"读成"接近随机"**。**11 条样本把 F1 从 6.7 拉到 60.1**，N=5 最好、N=10 反降。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-02_AI安全每日深度情报.md) |
| **I2I 改写 0/0%（判定制度病根）** | [EditAgent](./categories/t2i/papers/2610.39664_editagent_observation_space.md) | **Adobe Research + UCSD**。编辑 Agent 被 **action space** 与 **judge 的 observation space** 同时限制。**pointwise→listwise：72.1→85.9（+13.8）**，直接超过微调+4 路集成的 EditScore-72B（76.3）。但 **listwise 单独加会把 Photometric 54.2→47.2、Enhancement 65.0→36.8（−28.2）**，加验证记录才回来（64.4 / 80.3）⇒ **成对比较不是免费的**。并行搜索赢 **78.5%** 且只用一半 judge 调用。**不过 judge 的自举数据让三个 benchmark 全降。** | [📄 立即阅读](./daily-reports/2026-11/2026-11-02_AI安全每日深度情报.md) |
| **输出侧审核（通道盲区 + 奖励作弊）** | [OCR+MLLM](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) | 华中科技大学。**50.4% 的风险事件没有文本痕迹**，分布在 63% 的视频里，各类别 **37.2%–53.8%**（均匀，不是特例）。非文本召回 **≈0 → 60.1%**（从无到有）。**32B 零样本 mIoU 只有 4.72，全场最差** ⇒ 任务特定能力不是规模买来的。**辅助奖励把训练奖励刷到 ~1.0，真实 mIoU 从 13.48 掉到 2.19**；类别缩放 **4× 最优、8× 再塌**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-02_AI安全每日深度情报.md) |
| **输入侧改写（改写模型自己拒答怎么办）** | [MSafeTemp](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) | **ETH Zurich**。核心工程洞察：**让对齐模型翻译有害 prompt 会被拒答** ⇒ 把 prompt 拆成 **中性框架 + 类型化风险槽位**，框架可安全改写、槽位受控重填。**Olmo 英语 ASR 0.0% → 翻译后 13.7%**（但 Llama 反向：13.0→5.3）。**翻译版与本地化版打穿行为的 Jaccard 只有 0.40–0.45**；**单 fill 会漏掉约一半被打穿的模板**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-02_AI安全每日深度情报.md) |
| **图审 AB（聚合指标是盲的）** | [Judged in Company](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) | **TUM**。批处理 25 条一 prompt，**新随机划分让 11–22% 的判定翻转**（比改 key/改指令多 **6.5–13.3 点**），**而 AUROC 只差 −0.033~+0.010**。**9 个排列投票后仍残留 52–60% 翻转**，15 个独立 batch 的多数与单条判仍差 **8.4–17.8%**。两个通道都起作用（换判定 7–23%、换文本 9–26%）⇒ **只遮判定不够**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-02_AI安全每日深度情报.md) |

---



## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **274** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **风险住在看不见的那一半**（NEW） · **纯图 14.60 → 图+prompt 43.00**（NEW） · **聚合指标对个体翻转是盲的**（NEW） · **235B 也过不了 65%**（NEW） | 2026-11-02 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **框架+槽位分离改写**（NEW） · **单 fill 漏一半被打穿模板**（NEW） · **批处理翻 11–22% 而 AUROC 不动**（NEW） · 梯度侧 vs 内容侧审计 · 拒答率被话术污染 45pp | 2026-11-02 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **depict 轴 vs enable 轴**（NEW） · **三条件+豁免拆解判定**（NEW） · **pointwise→listwise +13.8**（NEW） · StruPO 结构保真配方 · MoI-Bench 二维评测 | 2026-11-02 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [MSafeTemp 框架+槽位改写](./categories/t2t/papers/2610.40516_msafetemp_template_slot_rewrite.md) (单 fill 漏一半模板) | [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [Judged in Company 批处理翻转](./categories/t2t/papers/2610.40241_judged_in_company_batch_flips.md) (11–22% 翻转 / AUROC 只动 0.03) | [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [EditAgent 观测空间](./categories/t2i/papers/2610.39664_editagent_observation_space.md) (listwise +13.8 / 证据才救回 −28.2) | [OCR+MLLM 非文本通道](./categories/t2i/papers/2610.38185_ocr_mllm_moderation_grounding.md) (非文本召回 0→60.1) | [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [FVH-Bench 功能型视觉危害](./categories/t2i/papers/2610.37722_fvh_bench_functional_visual_harm.md) (纯图 14.60→图+prompt 43.00) | [V-CAPE 编辑一致性 AutoQA](./categories/t2i/papers/2610.38611_v_cape_edit_consistency_autoqa.md) (人类 κ=0.77 / VLM<65%) | [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
