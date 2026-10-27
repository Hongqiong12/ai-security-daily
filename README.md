# ⚔️ AI Security Daily Intelligence

<p align="center">
  <b>全网唯一的「日更级」AI 安全论文精读仓库</b><br>
  <i>T2I / T+I2I 工业安全对齐 · 输入侧 Prompt Rewrite · T2T/Agentic 仅作迁移参考</i>
</p>

<p align="center">
  <a href="https://img.shields.io/badge/Reports-Today-blue.svg">
    <img src="https://img.shields.io/badge/Reports-Today-blue.svg" alt="Reports Today"/>
  </a>
  <a href="https://img.shields.io/badge/Papers-256-green.svg">
    <img src="https://img.shields.io/badge/Papers-256-green.svg" alt="Total Papers"/>
  </a>
  <a href="https://img.shields.io/badge/Last-Update-2026--10--28-orange.svg">
    <img src="https://img.shields.io/badge/Last-Update-2026--10--28-orange.svg" alt="Last Update"/>
  </a>
  <a href="https://github.com/Hongqiong12/ai-security-daily/stargazers">
    <img src="https://img.shields.io/github/stars/Hongqiong12/ai-security-daily.svg?style=social&label=Star" alt="GitHub stars"/>
  </a>
</p>

---

## 🔥 今日最具业务价值论文评测 (2026-10-28)

> **为什么要关注本仓库？** 上周的关键词是"**分数装错了东西**"，今天更进一步：**机制装错了位置**。六篇工作分别指出六组"看起来等价、实际不等价"的关系——压制参考注意力≠防编辑、写 reason≠有推理、造多视图≠有增强、终局读奖励≠测保真、删参数≠控输出、工业 PE≠做安全。**共同点：所有"看起来在起作用的中间量"都在撒谎，只有下游可验证量算数。**

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **T2I（输入侧改写的工业配方）** | [Qwen-Image-PE](./categories/t2i/papers/2610.33472_qwen_image_pe.md) | **Qwen Team / 阿里 + 北大**。本期唯一公开的工业级 T2I 输入侧改写配方：**反向蒸馏造监督**（好图→稠密描述当改写目标，MAUVE **0.290** vs 正向扩写 0.032）+ **组内设计奖励**（$G$ 候选拼网格、judge 组内条件化打分）。397B **+7.81** Overall，9B 超全部基线，跨 4 主干泛化。**但 rubric 四个维度里没有"安全"。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-28_AI安全每日深度情报.md) |
| **T+I2I（0/0% 的机制解释）** | [Copying As Defense](./categories/t2i/papers/2610.35566_copying_as_defense.md) | **Adobe Research + 普林斯顿**。编辑安全的方向反了：**注意力行和为 1，压掉参考图等于把票投给文本**，于是"成功去上下文化"的编辑器照样按恶意指令凭空画图。改成**强制它抄原图**，ESR **81.4% → 24.0%**（相对降 70.6%）、成本还低 **1.8–2.0×**。**顺手给了我们"软改写 = 取消编辑"的机制解释。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-28_AI安全每日深度情报.md) |
| **分类 SFT（模板 reason 一分不值）** | [LoRA vs 全量微调](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) | **Fiddler AI + SFU + Georgia Tech**。把理由换成**固定套话（34 token）**，准确率 **78.2%**，**比只有标签的 78.7% 还低**；换成同标签别条样本的理由只保留 60%。**只有这条样本自己那句话拿满 +4.0pp。** 同一篇证明**过拒不是阈值问题**（ROC-AUC 排序就差 0.026–0.343），但 reason 能把过拒砍 **37pp** 而召回反升。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-28_AI安全每日深度情报.md) |
| **护栏/图审（多视图 + 校准）** | [UniGuard](./categories/t2t/papers/2610.30742_uniguard.md) | **Monash + 澳国防科技组**。**0.6B 逼平 GPT-5.2**（ATBench 66.40 vs 66.52），平均 **+45.12 F1、ECE −35.41**。最该记的两个数：**只造视图不加对比，F1 掉 20.50**；**F1 不掉但 ECE 崩 18–28 完全可能**——判得准和说得准是两件事。 | [📄 立即阅读](./daily-reports/2026-10/2026-10-28_AI安全每日深度情报.md) |
| **T2I（奖励在哪读）** | [VaLoP](./categories/t2i/papers/2610.35607_valop.md) | **GIST**。奖励的价值梯度误差本质是**后验协方差**，随噪声升高而变大 ⇒ **在最该判"画了什么"的高噪声阶段最不准**。DPS($s=0$) 与 StitchVM($s=t$) 是同一族的两端，中间需一项穿过生成器的修正，默认 $s=0.6t$。**对我们：一致性奖励读在终局像素，读到的可能是去噪随机性。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-28_AI安全每日深度情报.md) |
| **权重侧（验收标准错了）** | [Risk-Aware Output Control](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | **南洋理工大学**。擦除不该用"参数离重训模型多近"验收——**生成模型能在从未显式训练过的内容上复现受版权素材**，参数不可区分性证不到输出。主张改为**输出空间统计保证**，把保形预测恢复成特例。⇒ **输入侧改写不是擦除的廉价替代品，而是同一目标的更直接实现。** | [📄 立即阅读](./daily-reports/2026-10/2026-10-28_AI安全每日深度情报.md) |

## 🔭 前沿 Survey & 洞察简报 (Must-Read)

我们不仅搬运论文，更系统沉淀方法论。以下是基于 **256** 篇安全论文萃取的全局视野：

| 研究洞察精华 | 解决的核心问题 | 更新状态 |
|------|------|----------|
| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **机制错位六连**(NEW) · **软改写=取消编辑**(NEW) · **模板 reason 零收益**(NEW) · **只造视图不加对比 F1 −20.5**(NEW) | 2026-10-28 |
| 🧭 **[T2I 主线模型评测地图（2026）](./insights/t2i-mainline-model-eval-map-2026.md)** | 当前主线模型测哪些指标 · 对应 benchmark / evaluation set 有哪些 · 训练集透明度与闭源程度如何分层 | 2026-04-22 |
| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **模板 reason 零收益**(NEW) · **过拒非阈值问题**(NEW) · **多视图+对比+校准**(NEW) · 判词不判意图 51/55 · 极性盲 4.12/5 | 2026-10-28 |
| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **Qwen-PE 输入侧改写配方**(NEW) · **CaD 注意力竞争机制**(NEW) · **VaLoP 奖励读取位置**(NEW) · **擦除验收标准批判**(NEW) | 2026-10-28 |
| 🤖 **[Agentic Search 攻防全景](./insights/agentic-search-survey.md)** | SkillGuard-Robust package-level 审计 · SnapGuard 轻量截图守卫 | 2026-04-30 |
| 🔪 **[Abliteration 与概念擦除范式](./insights/alignment-paradigm-shift-abliteration.md)** | 剖析大模型对齐的脆弱性，以及定向消融攻击的底层逻辑 | 2026-04-07 |

---

## 📚 结构化论文库：分模态防御体系

摒弃杂乱无章的论文堆砌，我们按照 **模态 -> 攻防类型 (Benchmark/Attack/Defense)** 建立严谨的分类索引：

### 📝 Text-to-Text (T2T) LLM 越狱与对齐
> **核心关注:** 对抗性提示、机制可解释性、多智能体协同攻击、GRPO 对齐漏洞

- **Attack (攻击突破):** [PISmith](./categories/t2t/papers/2603.13026_pismith.md) (100% ASR) | [FlipAttack](./categories/t2t/papers/2410.02832_flipattack.md) | [Tree Teaming](./categories/t2t/papers/2603.22882_treeteaming.md) | [Paper Summary Attack](./categories/t2t/papers/2507.13474_paper_summary_attack.md)
- **Defense (安全加固):** [LoRA vs 全量对照](./categories/t2t/papers/2610.33813_lora_vs_full_ft_prompt_safety.md) (模板 reason 零收益) | [UniGuard 多视图护栏](./categories/t2t/papers/2610.30742_uniguard.md) (0.6B 平 GPT-5.2) | [AutoDefense](./categories/t2t/papers/2603.21975_securebreak.md) | [KG-DF](./categories/t2t/papers/2603.19469_llm_agent_security.md) | [DOOR](./categories/t2t/papers/2503.03710_door.md)
- **Benchmark:** [判词不判意图](./categories/t2t/papers/2610.31047_harm_behavioural_lexical.md) (51/55 不达标) | [极性盲](./categories/t2t/papers/2610.27908_polarity_blindness.md) (4.12/5) | [Matched-FAR 监控器批判](./categories/t2t/papers/2610.30727_faithful_harm_monitors.md) (38 读取器×15 模型) | [DiagSafe](./categories/t2t/papers/2610.29225_diagsafe.md) (84 标签) | [AIMS](./categories/t2t/papers/2606.27210_aims.md) | [PandaGuard](./categories/t2t/papers/2505.13862_pandaguard.md) (19攻+12防) | [越狱演进综述](./categories/t2t/papers/2506.15170_from_llms_to_mllms.md)

### 🎨 Text-to-Image (T2I) 视觉模型安全
> **核心关注:** 工业界安全对齐、输入侧 Prompt Rewrite、NSFW 语义保真改写、概念擦除对抗、自动化红队测试

- **Attack (攻击突破):** [Mirage 图审绕过](./categories/t2i/papers/2610.30348_mirage.md) | [JailFuzzer](./categories/t2i/papers/2408.00523_jailfuzzer.md) | [GenBreak](./categories/t2i/papers/2506.10047_genbreak.md) | [Janus 多模态越狱](./categories/t2i/papers/2603.21208_janus.md)
- **Defense (安全加固):** [Qwen-Image-PE 输入侧改写配方](./categories/t2i/papers/2610.33472_qwen_image_pe.md) (+7.81) | [CaD 编辑安全机制](./categories/t2i/papers/2610.35566_copying_as_defense.md) (ESR 81.4→24.0) | [VaLoP 奖励读取位置](./categories/t2i/papers/2610.35607_valop.md) | [擦除验收标准批判](./categories/t2i/papers/2610.35052_risk_aware_output_control.md) | [ConceptACP SAE 定位擦除](./categories/t2i/papers/2610.32059_concept_acp.md) (FSR 80.02) | [EditJev 编辑路由](./categories/t2i/papers/2610.32635_editjev.md) (2.55×) | [AdvFidelity 保真奖励](./categories/t2i/papers/2610.29380_advfidelity.md) (奖励审计) | [Yuvion VL 图审基座](./categories/t2i/papers/2606.25034_yuvion_vl.md) (C2FT) | [SELECT 锚点边界](./categories/t2i/papers/2510.16342_select_erasure_boundary.md) | [AVLM 失效归因](./categories/t2i/papers/2606.30059_avlm_failure_taxonomy.md) (NeurIPS'26) | [CSTI 早期拦截](./categories/t2i/papers/2610.26452_csti.md) | [DSC 解耦控制](./categories/t2i/papers/2610.21569_dsc.md) | [PPAA 概念擦除](./categories/t2i/papers/2610.27719_ppaa.md) | [SPEED 精确擦除](./categories/t2i/papers/2503.07392_speed.md)
- **Benchmark:** [ABACUS judge-free 编辑评测](./categories/t2i/papers/2610.28316_abacus.md) (σ=0.013) | [Omni-UBench](./categories/t2i/papers/2610.31713_omni_ubench.md) (三维+掩码) | [Attractive Faces 偏置审计](./categories/t2i/papers/2610.28195_attractive_faces_reward_bias.md) | [IMPLICIT-Bench](./categories/t2i/papers/2609.24228_implicit_bench.md) | [HealBench](./categories/t2i/papers/2610.27516_healbench.md) | [LogicVal](./categories/t2i/papers/2610.24051_logicval.md) | [T2I-BiasBench](./categories/t2i/papers/2604.12481_t2i_biasbench.md) | [NTIRE 2026](./categories/t2i/papers/2604.11487_ntire_2026_robust_aigc_detection.md)

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
