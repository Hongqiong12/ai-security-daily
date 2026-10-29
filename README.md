# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-268-green.svg">
    <img src="https://img.shields.io/badge/Papers-268-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--10--30-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--30-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-30)

> **为什么要关注本仓库？** 上一轮的主题是"**参数被当成了常数**"；这一轮更根本——**所有的判定装置，都在把一个本该保留为"分布 / 集合 / 不确定"的东西，硬压成一个标量**。softmax 和恒为 1、单标签 gold、单点判定、内容相似度、平均奖励、手工压力策略，六种压缩，每一种都能单独推翻结论。
>
> **⚠️ 供给侧先说清楚**：arXiv 最新公告批次仍停在 **2026-10-27**，10-28/29/30 **三个批次连续空缺**，本轮相对上一轮**新增供给为 0**。并且 10-29 记下的"换口语化措辞能捞到东西"这个假设**被本轮证伪**——五个全新措辞（`photo editing assistant` / `query rewrite` / `trust and safety` / `brand safety` / `visual harm taxonomy`）**全部返回 0**。⇒ **归零不是措辞问题，是供给问题。** 因此本轮定位为**存量补筛 + 邻域结构迁移**，T2I 占比 33.3% 低于 66.7% 常态，已在此如实标注。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I（输出侧图审的结构病根）** | [SafeSteer](./categories/t2i/papers/2610.35017_safesteer_steering_refusal.md) | **USC + UCSB**。一句话钉死：**patch softmax 和恒为 1，所以它必须把质量放在某处**。弃权信号 AUROC **0.517 ≈ 随机**；拆开看，confidence 能处理"对象不在"（logit **0.880**）却处理不了"人在图上但不该问"（**0.757**，CLIPSeg **0.480**）。SAM 3 / Qwen2.5-VL 的分数靠**过度拒绝**换（over-refusal **0.341 / 0.279**）。加一个 null logit + 反事实不变性，**0.997**，over-refusal **0.000**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-30_AI安全每日深度情报.md) |
| **T+I2I（I2I 改写 0/0% 的指标病根）** | [Grounded Exploration](./categories/t2i/papers/2610.33810_grounded_edit_exploration.md) | **Georgia Tech + Pinterest**，NeurIPS'26 Workshop。**最强的负结果**：`High-level exploration`（抽象语义 Stage 1）与"完全没有 Stage 1"在 DirCov / Dispersion / Valid@8 **三列全部重合**（4.16 vs 4.17、0.504 vs 0.504、5.80 vs 5.83）⇒ **语义层抽象等于零收益**。落到"可行区域+改动幅度"才有 Grounded **+0.17** / Valid **+0.22**。且 Gemini IF **3.93 全场最高**却 DirCov **2.18**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-30_AI安全每日深度情报.md) |
| **标签审计（该改定义还是改标签）** | [ANT-A / ANT-OR](./categories/t2t/papers/2610.32415_ant_a_ant_or.md) | **蚂蚁集团 + 哈工大深圳**，EMNLP'26 Findings。**2 类任务的 κ（38.77）比 31 类（83.50）低 45 点** ⇒ 推翻"类目多所以难"。七数据集 κ 跨度 **38.77–83.50**，判定型低、识别型高。3 标注员+1 验证员 + **判别维度池**（support ≥2 过滤），**不训练**，accuracy **+4.5**，κ 收进 **2 点**。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-30_AI安全每日深度情报.md) |
| **数据审计（标签对了为什么还是错）** | [SimpleLoRIF](./categories/t2t/papers/2610.37481_simplelorif_safety_gradient.md) | **DatologyAI + UIUC**。安全退化的数据**看起来是良性的**，所以内容侧筛子**结构上抓不到**。改成看梯度：扔掉曲率修正 + **只回传最后 4 block**，**939,343 条 / 8×H100 / 1 小时**，EM AUC **0.865**，删 20% 使 GCG ASR **−22%**，**胜过 LLM-as-a-judge 过滤**。被删样本画像：**工具执行失败 / 叙事算术 / 直接 coding**——一个都不像有害。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-30_AI安全每日深度情报.md) |
| **RL 改写（奖励作弊怎么找）** | [Audit Where Hacks Pay](./categories/t2t/papers/2610.35716_audit_where_hacks_pay.md) | **清华 REASONS Lab + Virginia Tech**。作弊样本的 advantage **取决于同组兄弟**。整组按**弱通过数升序**审计 + 被抓给 **$2b-a$** 反射修正 ⇒ 作弊打到近零，而**全量审计只领先 2 点、LB 只用 28% 标签**。最反直觉：两个**期望相同**的无偏估计量结果差 **6–12 点**——方差是设计的一部分。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-30_AI安全每日深度情报.md) |
| **样本合成（保真与变难的位次）** | [StressSim](./categories/agentic-search/papers/2610.35426_stressim_intent_preserving.md) | **Imperial College + Safe Intelligence**，NeurIPS'26 Workshop。**保真是罚项（硬）、失败是主项（软）**——位次反了优化器就牺牲保真。遗传 prompt 优化 + **每任务 20 条 rollout、零训练**，τ-bench pass^4 最多降 **69%**，而首次有效比例保持 **0.900–1.000**。手工策略跨模型**方向能反**（0.572 / 0.620 高于 standard 0.320）。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-30_AI安全每日深度情报.md) |

---

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **268** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **判定装置的六种降维压缩**(NEW) · **抽象语义脚手架 = 零收益**(NEW) · **softmax 归一 ⇒ 无路可退**(NEW) · **κ 38.77 vs 83.50**（NEW） | 2026-10-30 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **梯度侧 vs 内容侧审计**(NEW) · **2 类 κ 低于 31 类 45 点**(NEW) · **同期望估计量差 6–12 点**(NEW) · 因子化 +0.001 / −0.360 · 拒答率被话术污染 45pp | 2026-10-30 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **抽象语义脚手架 = 零收益**(NEW) · **softmax 归一 ⇒ 过度预测**(NEW) · **referential vs fairness 弃权**(NEW) · StruPO 结构保真配方 · MoI-Bench 二维评测 | 2026-10-30 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | **StressSim 保真/失败位次**(NEW) · 手工策略跨模型方向会反(NEW) · SkillGuard-Robust · SnapGuard | 2026-10-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [AK_QMUL 层级标签](./categories/t2t/papers/2610.36360_arguard_qlora_hier.md) (因子化 −0.360) | [VLM 拒答敏感性](./categories/t2t/papers/2610.37430_vlm_refusal_instruction_sensitivity.md) (话术翻 45pp) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [StruPO 结构保真改写](./categories/t2i/papers/2610.36146_strupo.md) (SGR 80.74 / 动作空间 −7.06) | [DICE 少步擦除](./categories/t2i/papers/2610.36665_dice_fewstep_safety.md) (方向 cos 0.30/0.07) | [LoRA 溯源签名](./categories/t2i/papers/2610.36933_lora_provenance.md) (P-II AUROC 1.000) | [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [MoI-Bench 操作×目标二维评测](./categories/t2i/papers/2610.37599_moi_bench.md) (几何聚合) | [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
