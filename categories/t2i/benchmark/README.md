# 📊 文生图 - 基础评测集

文生图扩散模型的安全评测基准、数据集与评估框架论文。

> 最后回填: 2026-11-10 | 共 **47** 条
> 延伸索引: [《T2I 安全 Benchmark 短名单（2026 年前高引用版）》](../../../insights/t2i-benchmark-shortlist-pre2026.md)

## 综述与全景

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| AI Security Landscape 2026 | — | 2026 (本项目) | 基于 220 篇论文的宏观安全格局分析（T2T/T2I/Agentic 三模态） |
| T2I Safety Seven-Year Survey | — | 2026 (本项目) | 文生图安全七年演进：从 Dual-Guard / Embedding Arithmetic / IncreFA，继续推进到 TextGround4M / CoBench / Edit-R1 的 verifier 与结构化评测信号 |
| Operationalizing Fairness in T2I Models | [2604.16516](https://arxiv.org/abs/2604.16516) | 2026 arXiv | 系统梳理 T2I 公平性审计与缓解文献，并提出 Target Fairness / Threshold Fairness 框架 |

## 安全评测基准 (Benchmark)

> 说明：**JailbreakBench** 已从本表移出，因为它本质是 LLM jailbreak benchmark，不属于 T2I benchmark。

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| **LongBanana** | [2611.06856](https://arxiv.org/abs/2611.06856) | 2026（**快手可灵 AI 研究院** + 华南师大 + UBC/Vector/CMU/清华/港科大/港大） | **图结构接地的原子判据基准**：90 任务 / 3×3 分类法 / 每任务 ~32 参考图 + ~20 约束 + ~50 评测项 ⇒ **4,670 条专家指定原子判据**；900 输出 × 清单 = **46,700 条人审标签**，双标 15%（**89.4% / QWK 0.83**）。三层图单元（节点/边/整图）→ 三维（Content Fidelity / Relational Binding / Global Constraint）。agentic checklist judge：**输出级相关 +2.9 点（0.8413→0.8707）而条目级三元一致 +15.82 点、两端相反错误 −19.28 点** ⇒ 同一个改进换分母差 5 倍 (NEW) |
| **Number Words Past Ten** | [2611.06840](https://arxiv.org/abs/2611.06840) | 2026（University of Colorado Boulder） | **同噪声单因子对照协议**：一个物体 + 一个起始噪声 = 一张图，故可固定一切只改一个因子（数字/种子/拼写/无关词/只重画细于 1/8 图幅的噪声）；3,088 张由未见 prompt 的人计数。射程内（2–8）**80–99%** 同噪声对满足"大请求给更多物体"；射程外重画细噪声推动数量达数词效果的 **2/3** 而数词**无方向**。**指标可分辨性负结果**：exact-match 分不出"松跟随"与"忽略"，relative-error **甚至偏好常数 16** (NEW) |
| HRS-Bench | [2304.05390](https://arxiv.org/abs/2304.05390) | 2023 ICCV | Holistic / Reliable / Scalable 三位一体的 T2I 综合评测框架，覆盖 50 类应用与多维能力指标 |
| HEIM (Holistic Evaluation) | [2311.04287](https://arxiv.org/abs/2311.04287) | 2023 NeurIPS Datasets & Benchmarks | 把质量、对齐与 bias / toxicity / fairness / robustness 纳入统一 T2I holistic evaluation |
| UnsafeBench | [2405.03486](https://arxiv.org/abs/2405.03486) | 2024 arXiv | 面向真实图像与 AI 生成图像的 image safety classifier 评测框架，代表生成后审核安全基准 |
| T2ISafety | [2501.12612](https://arxiv.org/abs/2501.12612) | 2025 CVPR | 系统覆盖 fairness / toxicity / privacy 的 T2I 安全专项 benchmark |
| SALMUBench | [2603.26316](https://arxiv.org/abs/2603.26316) | 2026 CVPR | Safe Unlearning 统一基准，支持概念擦除方法对比 |
| BPO-Verify | [2603.26328](https://arxiv.org/abs/2603.26328) | 2026 CVPR | 模型身份验证基准，检测生成内容是否来自目标模型 |
| AR Watermark Robustness | [2604.11720](https://arxiv.org/abs/2604.11720) | 2026 arXiv | 自回归图像生成水印在 removal / forgery / radioactive filtering 间存在结构性三难 |
| NTIRE 2026 Challenge | [2604.11487](https://arxiv.org/abs/2604.11487) | 2026 CVPR Workshop | 42 个生成器 + 36 种扰动的真实世界鲁棒 AIGC 检测挑战 |
| QuAD | [2604.15027](https://arxiv.org/abs/2604.15027) | 2026 CVPR Workshop | 首次把 near-duplicate 传播链与质量感知校准纳入 AIGI 检测，在 ReWIND 上带来约 8 个点 bAcc 提升 |
| T2I-BiasBench | [2604.12481](https://arxiv.org/abs/2604.12481) | 2026 arXiv | 用 13 指标统一审计 demographic bias、元素遗漏与 cultural collapse，补齐偏见评测维度 |
| Bias at the End of the Score | [2604.13305](https://arxiv.org/abs/2604.13305) | 2026 arXiv | 首次系统审计 reward models 的 demographic bias，揭示评分函数会放大 hypersexualization 与身份漂移 |
| TwoHamsters | [2604.15967](https://arxiv.org/abs/2604.15967) | 2026 arXiv | 首个 multi-concept compositional unsafety 基准，系统揭示组合语义风险与过滤器失效 |
| IncreFA / IABench | [2604.17736](https://arxiv.org/abs/2604.17736) | 2026 arXiv | 把生成器归因推进到 incremental open-set setting，并配套 IABench 衡量 Avg. Acc. / Auth. Acc. / Unseen Acc. |
| KVBench / KE-Check | [2604.22302](https://arxiv.org/abs/2604.22302) | 2026 arXiv | 以 1800 个双语教材级样本和 5158 条 checklist 把 T2I 正确性评测推进到知识密集 visual correctness，并用约束修正框架降低 scientific hallucination |
| TextGround4M | [2604.24459](https://arxiv.org/abs/2604.24459) | 2026 AAAI | 4.1M prompt-grounded 文本渲染数据集，用 Prompt Coverage / Layout IoU 把 OCR-rich 终态纳入结构化评测 |
| CoBench | [2604.25358](https://arxiv.org/abs/2604.25358) | 2026 CVPR Workshop | 把 layout-guided T2I 拆成 semantic alignment + spatial alignment + unified score 的双 benchmark 体系 |
| GPT-Image-2 in the Wild | [2604.25370](https://arxiv.org/abs/2604.25370) | 2026 arXiv | 首周野外部署数据集，系统揭示社交平台传播链对 provenance、文本渲染场景与真实使用分布的重塑 |
| PixJail | [2606.24081](https://arxiv.org/abs/2606.24081) | 2026 arXiv | paper-to-pipeline 统一复现 11 个 T2I jailbreak 方法，把 benchmark 从 prompt list 升级为评测基础设施 |
| HealBench | [2610.27516](https://arxiv.org/abs/2610.27516) | **2026 AAAI'27** | 30,000 图文对 / 19 类 / 92 子类的心理舒适细粒度基准，配套 HealBench-Eval（1,095 例）**系统评测 14 个生成模型与 prompt-rewriting 策略**；提出**三维分列 + 目标维度 1:2:1 加权**的 HealScore，并训专属 scorer（THS）作 Flow-GRPO 奖励 ✅ 已精读 |
| IMPLICIT-Bench | [2609.24228](https://arxiv.org/abs/2609.24228) | 2026 arXiv | 1,831 组「中性/刻板/反刻板」prompt 三元组（场景固定），配 KG unit 锚点；**三种锚点信息条件（无/检索/oracle）× 两种干预（改写/嵌入引导）**的归因实验，提出乘性联合指标 S = 100·mean[Y·(1−b/5)] ✅ 已精读 |
| LogicVal | [2610.24051](https://arxiv.org/abs/2610.24051) | 2026 arXiv | 把 T2I 评测写成**逻辑约束满足问题**：prompt→ASP 约束（9 类 C1–C9 / 71 模板），图像→场景图，clingo 判 SAT/UNSAT，**无需参考图**；含反空真条款设计 ✅ 已精读 |
| FVH-Bench | [2610.37722](https://arxiv.org/abs/2610.37722) | 2026 arXiv (CUHK-SZ + SUNY Buffalo) | 把图审从「描绘了什么」推进到「**使能了什么**」（functional visual harm）：11 生图器平均拒绝率仅 **2.45%**，专用图审召回 **1.60%–44.00%**；提出 Condition-Decomposed Detection（每类三条必要条件 + 一条良性豁免，平均 1.57 次调用）把 8B 图审拉到 **80.40**（FPR 0）✅ 已精读 |
| V-CAPE | [2610.38611](https://arxiv.org/abs/2610.38611) | 2026 arXiv (Amazon) | **I2I 指令式编辑的视觉一致性 AutoQA**：40K 编辑对 / 27K 图，人类 Fleiss κ **0.77**，而全部 VLM（含 235B）上限 **<65%**；零样本 accuracy 51.5% 但 macro-F1 仅 6.7%（全判一类）——揭示「判据良定义」与「模型判得动」是两件事 ✅ 已精读 |
| EditAgent | [2610.39664](https://arxiv.org/abs/2610.39664) | 2026 arXiv (Adobe Research + UCSD) | 把多轮编辑失败归因到**观测空间**而非动作空间：winner set 仅 42.3% 通用 / 29.2% 专用 / **13.5% 无可用候选**；判定从 pointwise→listwise 升 **+13.8 点**（72.1→85.9），但需**成对**配 verification record（证据可查）才不反向掉点 ✅ 已精读 |

## 防御范式代表

| 论文 | ArXiv | 年份/会议 | 核心创新 |
|------|-------|----------|----------|
| ImageProtector | [2604.09024](https://arxiv.org/abs/2604.09024) | 2026 ACL | VPI (Visual Prompt Injection) 攻击翻转为隐私保护工具，91% 保护率 |
| FlowGuard | [2604.07879](https://arxiv.org/abs/2604.07879) | 2026 arXiv | 线性潜空间解码实现生成中 NSFW 检测，F1 提升 30%，内存减少 97% |
| EGLOCE | [2604.09405](https://arxiv.org/abs/2604.09405) | 2026 arXiv | 训练无关双能量引导潜空间优化用于概念擦除 |
| VESFlow | [2606.23267](https://arxiv.org/abs/2606.23267) | 2026 arXiv | 面向 few-step flow matching 的速度场安全编辑，显式平衡 ASR 降低与 benign 保真 |
| ForceForget | [2606.14351](https://arxiv.org/abs/2606.14351) | 2026 ICML | 双奖励 + Safe Adapter，同步优化 unsafe concept 移除与安全语义保真，并有效迁移到 I2I |
| SafetyBPO | [CVPR 2026 Findings](https://openaccess.thecvf.com/content/CVPR2026F/html/Wu_SafetyBPO_Bidirectional_Preference_Optimization_for_Safe_Text-to-Image_Generation_CVPRF_2026_paper.html) | 2026 CVPR Findings | safe prompt rewriting + image preference 的双视角安全对齐，显式缓解 over-forgetting |
| Omni-UBench | [2610.31713](https://arxiv.org/abs/2610.31713) | 2026 arXiv (浙大+阿里) | 全模态护栏三维基准（Safety/Utility/Reliability）：183,977 样本 / 37 来源 / 4 模态；**等长掩码消融**（空白图/静音/占位文本）暴露"判定与内容无关"，配套越狱话术×良性媒体的过敏感探针 |
| Yuvion VL RiskEval (YVRE) | [2606.25034](https://arxiv.org/abs/2606.25034) | 2026 arXiv (阿里安全 AGI Lab) | 三级递进评测（58 benchmark）：Level 1 通用能力设 ≤3 点退化 gate，Level 2 公开安全 8 集 + 自建电商治理 4 集，Level 3 内部业务 20+ 集六维（含 AI 生成图检测、动态政策下的指令遵循） |
| ABACUS | [2610.28316](https://arxiv.org/abs/2610.28316) | 2026 WACV (CEA List / 巴黎萨克雷) | **指令式图像编辑的 judge-free 评测基准**：10,944 指令 / 3,845 图 / 80 类；全景真值经双检测器可删性审计，SAM3 + 匈牙利实例匹配 + 双检测器共识，`Score = CF × SC × OC` 乘积；与人类计数一致性 **0.82**（纯 VLM 0.55、单检测器 0.28），跨 7 编辑器 σ=**0.013** |

| **WeGenEditBench + WeGenEvoStudio** | [2610.41210](https://arxiv.org/abs/2610.41210) | 2026 arXiv（**腾讯微信视觉 + 中山大学**，58 页） | **"先要件后汇总"的图像编辑基准**：2,740 instance / **148** 任务类型（单图 / 文字密集 / 多参考）/ 15 配置；checklist **预生成且跨模型共享**，judge 必须先写 item 级理由与扣分再给维度分（EG/PR/VQ/DS）；不适用项排除出分母、**空 side 列表不算成功**；**每版本冻结 judge/prompt/输入处理/checklist/无效响应五项**；审计 15,214 model–task + 194,836 item 记录、10% 人工审。硬证据：**PR 全场第一（4.175）的模型 Overall 只排第五（3.841）**；定向收益是全量的 **1.07–1.85×**；RSI 环（WeGenEvoStudio）FLUX.2 Overall 1.083→3.517、Qwen +13.2%（含 −0.343 的子项跌幅）✅ 已精读 |
| MoI-Bench | [2610.37599](https://arxiv.org/abs/2610.37599) | 2026 arXiv (UCL + 南京大学 + 香港理工 + 华东师范) | **图像生成/编辑的"操作 × 目标"二维评测**：16 操作 × 8 目标稀疏矩阵 → 64 子任务 / 1150 样本；判据 IF/VQ/DP(Structure+Identity) 组成 **稀疏 rubric 立方体**（always / sample-dependent / N/A 三态），条件**先写后跑**；**加权几何平均**聚合禁止跨判据补偿，**能力缺失记 0 且不移除**；双 judge（GPT-4o 主 + Gemini-3.1-pro 独立）排名 Spearman **ρ=0.968**、人类锚 **ρ=0.904**；输出 Quality–Deployability 二维图谱（iPhone 17 Pro / Xiaomi 15 Pro 实测延迟与峰值内存） |

| **UUBench** | [2611.04467](https://arxiv.org/abs/2611.04467) | 2026 arXiv（**中科院自动化所 + 国科大 + 字节跳动 + 港中深 + 上交**） | **跨通路概念擦除的六格诊断基准**：30 目标（人物/地标/物体各 10）× 2 同类邻近概念 = 60 邻居 / 720 图。**六指标各自独立分母**：TF 目标遗忘（生成）/ SF 严格遗忘 / NR 邻居保留 / SR 严格邻居保留 / TU 目标非身份效用（理解）/ NU 邻居效用，并写死偏序 **SF ≤ TF、SR ≤ NR**。「生成侧 TF 100.0 而 DF 仅 24.0」「两通路直接组合只到 31.3」「N=1→30 时理解侧 DF 92.7%→37.1%、生成侧邻居 NR 剩 41.8%」三条硬数字把权重侧擦除的失效边界量化到不可忽略 ✅ 已精读 |

| **CompoSET** | [2610.41118](https://arxiv.org/abs/2610.41118) | 2026 arXiv（**Caltech / Pietro Perona 组**） | **受控单点编辑的组合性基准**：既有 benchmark 的 base–foil 配对图**平均 97% 像素在变**（配对间场景/布局/内容全不同）⇒ 模型只要捕捉"整图不一样"即可答对。CompoSET 把差异压到 **8%**：**1,776 instance / 80 自然场景 / 每 base ~22 个 foil / 16 种编辑类型（4 语义类别）/ 3 档 caption 长度**；评分要求 **image→text 与 text→image 双向都对**（strict bidirectional，随机线 16.67%）。硬证据：**22 个 dual-encoder VLM 全部在或低于随机**（最好 SigLIP-2 SO400M/14 = **13.9%**，95% CI [12.3,15.5]，scene-clustered bootstrap 后 22 个上界全 <**15.55%**），而同模型 BiVLC 49.5% / ColorSwap 39.7% / MMVP 31.1%；**文本侧硬负样本不迁移**（NegCLIP 7.0 < CLIP B/16 LAION 7.8）；失败集中在 Spatial / Quantity / Activity&State。⇒ **I2I 编辑评测集改造的直接范本**（一条指令配多个单点 foil，才能把"场景难"与"编辑难"分开）✅ 已精读 |

| **Coverage Hides Churn** | [2611.07502](https://arxiv.org/abs/2611.07502) | 2026 arXiv / WACV 2027（**Virginia Tech + Accenture**） | **策略更新的"判断漂移"评测协议（churn）**：把「覆盖率」与「个体决策稳定性」拆成两个必须同时报的量。协议三件套——① HPS（Homogeneous Prediction Sets）与 HPS-Refresh 逐轮刷新；② **churn / 撤销率 / 新增率**（同一图像在前后两轮的标签是否被改）；③ **PrefixCP**（每类目保留入册时注册表前缀，取前若干标签入册）。硬证据：覆盖保证有效但 HPS-Refresh 改变 **53–90%** 图像旧决策；**只动归一化项**（不改任何类目边界）时受影响图像 **60–67%**、撤销率 **8.5–34.7%**，而**旧类覆盖变化 ≤0.01**；撤销 **8.4–52.7%** vs 新增 **0.1–2.5%**（几何不对称，放开容易收回难）；PrefixCP 恢复 **40.9–58.5%** 覆盖差距、代价 **0.49–3.14** 个标签；Table 5 的排期实验让 **49.6–65.8%** 图像集合全变而 macro 覆盖 ≤0.0015。⇒ **阈值/注册表变更上线前必须报 churn，不能只报覆盖率与准确率** ✅ 已精读 |

| **StitchEditBench** | [2611.07922](https://arxiv.org/abs/2611.07922) | 2026 **NeurIPS**（**香港科技大学**） | **"编辑梯度与结构梯度"逐层对齐的编辑基准 + 逐层梯度探针**：ST 60 / OM 50 / VC 40 = **150 例**，四指标 DCS（方向一致性）/ CLIP-Dir / LPIPS / User Pref.。把编辑失败从「指令没听懂」重新归因到**梯度通路的层间冲突**——逐层计算编辑梯度与深度梯度的余弦对齐剖面，发现冲突集中在中后段。硬证据：**显式条件把原图深度锁死**，源深度 CLIP-Dir 仅 **0.62**，换成 oracle 目标深度也只有 **0.79**，而**隐式条件 0.81**（即"给出正确答案"也救不回显式条件的锁死）；冲突区一起训能把 DCS 拉到 **0.92** 但 CLIP-Dir 掉到 **0.75**；Random Schedule 0.83 ⇒ **一致性指标与指令遵循指标在冲突区互为代价，必须双列报** (NEW) |

| **VisionValueBench** | [2611.05578](https://arxiv.org/abs/2611.05578) | 2026 arXiv（**UW–Madison + 微软亚洲研究院**） | **把"文化价值"从模糊标签拆成可测维度的 T2I 基准**：以 **Hofstede 六维**（PDI/IDV/MAS/UAI/LTO/IVR）为坐标，配 **SAE（单属性提取）/ IAE（整体属性评估）双判据**，用 **TVD** 与 **homogeneity gap（群内−群间 cosine）** 量化 **visual value leakage**（连中性 prompt 也在表达价值取向）。硬证据：**EN→ZH 换语言后位移仅 0.07**（换语言改不了取向）；HiDream 的 UAI 从 **−0.357 翻到 +0.182**（ΔS=**+0.602**）；SAE **77.50% / κ 0.513** 明显弱于 IAE **82.92% / κ 0.731** ⇒ **拆维打分不如整体判**（与"越细越准"的直觉相反）。嵌入用 CLIP ViT-H-14 + InsightFace buffalo_l 双通道 ✅ 已精读 |

| **Proxy Audit for T2I Disparity** | [2611.07132](https://arxiv.org/abs/2611.07132) | 2026 arXiv（**弗吉尼亚大学**） | **代理变量（proxy variables）审计协议**：不直接测"受保护属性"，而是沿 **职业 / 地理 / 姓氏** 三条代理轴构造配对探针，把"总分"与"失败位置"分开。硬证据：**Flux 0.310 与 Imagen 0.312 的总分几乎重合，但失败格子完全不重叠**（一致率意义上的"同分不同病"）；Stable Diffusion 在**姓氏格**掉到 **0.523**；面部嵌入 cosine **0.838** 说明失败并非"人脸不像"；**Schmidt / Chen / Kim 三姓氏的 TVD < 0.1** ⇒ 群体级分布差异小到不可见，而个体级失败已很严重。⇒ **公平性/鲁棒性验收不能只看聚合分，必须报分格矩阵** (NEW) |

| **T2I-NSI（Negation Suppression）** | [2611.09304](https://arxiv.org/abs/2611.09304) | 2026 arXiv（**IIT Jodhpur + Colorado State**） | **第一个把"否定约束是否生效"做成基准级测量的工作**：759,869 配对 prompt 原子 / 5,082 物体目录 / **916,272 图** / 6 生成器（FLUX.2、Qwen-Image-2512、SD3.5、GPT-Image-1.5、Gemini-2.5-Flash、Midjourney v7）。**设计要点**：每个否定 prompt 配一条规范肯定对照，探针**只用肯定描述 query**（绕开探针自身的否定盲区）；NSI=$(C^+-C^-)/(C^++C^-)$∈[−1,1]；**六分类失败模式**（SUCCESS / ALWAYS_PRESENT / ALWAYS_ABSENT / INVERSE / PARTIAL_SUPPR / WEAKLY_REND）把"从不生成"与"无视否定"分开。硬证据：**INVERSE 0.00%**（45.6 万次原子-模型评测）而 **ALWAYS_PRESENT 13.0–16.9% + PARTIAL_SUPPR 9.2–12.5%**，**SUCCESS 仅 0.03–0.29%**；Robust NSI 开源 **0.0198–0.0378**、GPT-Image-1.5 **0.0934**、Gemini **0.0902**（匹配 prompt 下 **3.5×**，Δ=−0.067[−0.075,−0.059]）；**WEAKLY_REND 71.8–74.2% 主导聚合**（这些原子均 NSI 0.004–0.017，把总分拉到零）；句法 **0.0110–0.0267** < 形态 < 词汇 **0.0301–0.0580**；**L2 关系否定是三者一致谷底**；人工 420 原子 / 2,522 trials：残留率 **87.3% vs 度量 85.3%**、**κ=0.09（标签非人类等价）**、度量判"无从判定"的 502 原子中 **283 个(59.8%)人工判为 ALWAYS_PRESENT**；阈值网格下 **OTHER 占 10–97%** 而 NSI 变 ≤0.005 ✅ 已精读 |

[← 返回文生图目录](../README.md)
