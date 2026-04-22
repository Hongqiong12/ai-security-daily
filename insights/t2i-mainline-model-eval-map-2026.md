# T2I 主线模型评测地图（2026-04）

> **整理日期**: 2026-04-22
> **目的**: 回答“当前 T2I 主线模型在测哪些指标、对应哪些评测集、训练集是什么”这三个最常被混在一起的问题。
> **阅读原则**: 先分清“评什么”与“在哪评”，再分清“模型能力”与“训练数据公开程度”。

---

## 1. 先给结论

当前 T2I 主线模型的安全/治理评测，实际上已经裂成 **4 条主线**：

1. **违规生成与越狱**
   - 关心模型会不会被 prompt 绕过
   - 常用指标：ASR、过滤器 Recall / FPR、MCCU 成功率

2. **概念擦除 / 安全遗忘**
   - 关心“删没删掉危险概念、有没有误伤无害概念”
   - 常用指标：ASR、UDA、P4D、FID、CLIP、MCP、SCR / NCR

3. **AIGC 检测 / 归因 / 溯源**
   - 关心“这图是不是 AI 生成、由哪家模型生成、有没有被改”
   - 常用指标：Robust ROC AUC、bAcc、NLL、Auth. Acc.、Unseen Acc.、IoU / F1（篡改定位）

4. **公平性 / 偏见 / 评分函数治理**
   - 关心 demographic bias、cultural collapse、reward model 偏置
   - 常用指标：Entropy、CBS、CAR、KL、BA、CCS、ΔNSFW、ΔSkin Exposure

一句话说：**现在已经不是“拿一个 benchmark 测所有 T2I 安全问题”的时代了。**

---

## 2. 主线模型族谱：现在大家主要在测谁

| 模型族 | 代表模型 | 当前评测中的典型角色 | 训练集公开程度 |
|------|---------|------------------|--------------|
| **早期开源扩散基线** | SD1.4 / SD1.5 / SD2 / SD2.1 | 几乎所有 benchmark 的基础对照组 | **相对较高**：通常视为 LAION-5B 派生过滤子集路线 |
| **中期高质量扩散主线** | SDXL | fairness / jailbreak / detection / attribution 常见强基线 | **中等**：官方公开为大规模 web-scale text-image 训练路线，但精确配方不完全透明 |
| **新一代扩散主线** | SD3 / SD3.5-Large | 越来越多出现在 bias / attribution / erasure / detection 实验里 | **较低**：精确训练语料通常未完整公开 |
| **单流 Transformer 主线** | FLUX.1-dev / FLUX.1-schnell | 当前最值得重点盯的主线模型，常在 MCCU / bias / attribution 中最强也最脆 | **较低**：训练语料未完整公开 |
| **研究型开源替代路线** | PixArt-α、Playground-v2.5、LCM-SDXL 等 | 方法论文里常作为结构或效率对照组 | **不一**：部分公开，部分只给模型不完全给数据细节 |
| **闭源商业主线** | Midjourney v6、DALL·E 3、Imagen 3 / Gemini image stack | 常在 AIGC detection、fairness、holistic eval 中作为真实部署对象 | **很低**：训练集基本不公开 |
| **AR / 原生多模态新支线** | CogView4、GPT-4o 图像生成等 | attribution / benchmark 中开始出现，但仍属新支线 | **很低**：大多只公开能力，不公开训练数据 |

---

## 3. 现在主流都在测哪些指标

## 3.1 违规生成 / 越狱 / 安全过滤

| 指标 | 含义 | 越高/越低更好 | 典型用途 |
|------|------|---------------|---------|
| **ASR (Attack Success Rate)** | 成功生成违规图像的比例 | **越低越好**（对防御） | 越狱攻击、概念擦除后的红队评估 |
| **Recall / TPR** | 检测器抓住违规样本的比例 | **越高越好** | 安全过滤器、MCCU 检测器 |
| **FPR** | 误伤正常请求/图像的比例 | **越低越好** | 审核器、运行时防护 |
| **MDR (MCCU Defense Rate)** | 面对组合语义风险时的防御率 | **越高越好** | TwoHamsters 这类组合风险 benchmark |
| **NSFW rate** | 输出被判为 NSFW 的比例 | 视场景而定 | reward model 审计、越狱后果度量 |

### 代表 benchmark / 数据集
- **TwoHamsters**：测 multi-concept compositional unsafety，关键看 MCCU 成功率 / MDR
- **JailbreakBench（邻域参考）**：偏方法论，但严格说不应当算 T2I benchmark 主索引
- **UnsafeBench**：偏生成后安全分类器评测
- **T2ISafety**：更接近“综合安全专项 benchmark”

---

## 3.2 概念擦除 / 安全遗忘

| 指标 | 含义 | 越高/越低更好 | 典型用途 |
|------|------|---------------|---------|
| **ASR** | 目标危险概念是否仍能被生成 | **越低越好** | 擦除是否彻底 |
| **UDA** | 对未知/变体提示下的 residual unsafe generation | **越低越好** | 擦除鲁棒性 |
| **P4D** | prompt-level persistence / prompt-based residual risk | **越低越好** | 对 prompt 攻击残留风险评估 |
| **FID** | 擦除后图像质量分布变化 | **越低越好** | 保真度 |
| **CLIP Score** | 文图语义对齐 | **越高越好** | 语义保真 |
| **MCP** | 与目标相近的无害概念保留能力 | **越高越好** | 误伤评测 |
| **SCR / NCR** | 单概念 / 非目标概念保留率 | **越高越好** | TwoHamsters 等 benchmark 中常见 |

### 代表 benchmark / 数据集
- **SALMUBench**：安全遗忘 / 关联级遗忘评测
- **TwoHamsters**：除了越狱，也逼迫擦除方法面对组合语义误伤问题
- **TICoE / DAMP / SPEED / UCE / ESD** 这类论文常内置自己的评测协议，但指标集合已经逐步稳定下来

---

## 3.3 AIGC 检测 / 模型归因 / 篡改定位

| 指标 | 含义 | 越高/越低更好 | 典型用途 |
|------|------|---------------|---------|
| **Robust ROC AUC** | 在真实后处理扰动下的真假排序能力 | **越高越好** | NTIRE 2026 主指标 |
| **Clean ROC AUC** | 干净样本条件下的排序能力 | **越高越好** | 检测上界 |
| **bAcc** | 平衡准确率 | **越高越好** | QuAD、野外检测 |
| **NLL** | 预测置信度的负对数似然 | **越低越好** | 概率校准质量 |
| **Avg. Acc.** | 多模型归因平均准确率 | **越高越好** | IncreFA / IABench |
| **Auth. Acc.** | 真图 vs 假图区分准确率 | **越高越好** | 归因与溯源 |
| **Unseen Acc.** | 未见模型检测准确率 | **越高越好** | 开放集归因 |
| **IoU / F1 / Recall** | 篡改定位性能 | **越高越好** | Dual-Guard 这类 tamper localization |

### 代表 benchmark / 数据集
- **NTIRE 2026 Challenge**：42 个生成器 + 36 种扰动，主打真实链路鲁棒检测
- **QuAD / ReWIND / AncesTree**：近重复传播链 + 质量校准检测
- **IABench**：增量归因 benchmark，支持 family-aware attribution 与 unseen detection
- **BPO-Verify**：更偏 API 身份验证 / 模型宣称真实性验证

---

## 3.4 公平性 / 偏见 / 评分函数治理

| 指标 | 含义 | 越高/越低更好 | 典型用途 |
|------|------|---------------|---------|
| **H_g / H_r (Entropy)** | 性别 / 种族分布均匀度 | **越高越好** | Embedding Arithmetic、fairness audit |
| **CBS** | Composite Bias Score | **越低越好** | T2I-BiasBench |
| **BA** | Bias Amplification | 接近 1 或更低更好 | 看模型是否放大现实偏差 |
| **KL** | 与目标分布的距离 | **越低越好** | demographic parity / representation audit |
| **CAR** | cultural accuracy ratio | **越高越好** | 文化符号正确性 |
| **GMR / IEMR** | 显式/隐式元素遗漏率 | **越低越好** | 文化与语义完整性 |
| **CCS** | Concept Coherence Score | **越高越好** | 去偏后是否还保住职业 / 概念 |
| **ΔNSFW / ΔSkin** | reward optimization 带来的性化/裸露增量 | **越低越好** | reward model 审计 |

### 代表 benchmark / 数据集
- **T2I-BiasBench**：13 指标统一审计 demographic bias、元素遗漏、cultural collapse
- **Bias at the End of the Score**：把 reward model 也纳入评测对象
- **Operationalizing Fairness in T2I Models**：提出 Target Fairness vs Threshold Fairness 框架
- **HEIM / HRS-Bench**：更广义的 holistic evaluation，包含安全相关维度

---

## 4. “在哪测”——评测集现在怎么分层

## 4.1 安全专项 benchmark
这些是**直接围绕安全问题**建的：
- **UnsafeBench**：图像安全分类器评测
- **T2ISafety**：fairness / toxicity / privacy 综合安全 benchmark
- **TwoHamsters**：组合语义不安全 benchmark
- **SALMUBench**：安全遗忘/关联级遗忘 benchmark
- **IABench**：模型归因与增量扩展 benchmark

## 4.2 真实部署链路 benchmark
这些更强调“上平台后还行不行”：
- **NTIRE 2026**：后处理鲁棒检测
- **QuAD / ReWIND / AncesTree**：传播链、近重复、质量退化
- **Dual-Guard**：溯源 + tamper localization 一体化协议

## 4.3 广义 holistic benchmark
这些不是只测安全，但必须读，因为它们经常定义主线模型的默认比较面：
- **HRS-Bench**
- **HEIM**

---

## 5. 训练集：哪些公开，哪些其实不知道

这里必须直说：**当前 T2I 主线模型最大的结构性问题之一，就是训练集透明度远落后于评测复杂度。**

### 5.1 公开程度较高的老主线
| 模型族 | 训练集情况 |
|------|------------|
| **SD1.4 / SD1.5 / SD2 / SD2.1** | 通常被视为 **LAION-5B 派生过滤子集** 路线，训练语料来源相对清楚，是很多 benchmark 的“已知数据背景基线”。 |

### 5.2 半公开、配方不完全透明的中间主线
| 模型族 | 训练集情况 |
|------|------------|
| **SDXL** | 官方给出的方向是大规模 web-scale text-image 数据与更强过滤/分桶策略，但**精确数据组成、清洗细节、采样权重并未完全公开**。 |
| **PixArt / Playground / 其它开源替代路线** | 不同项目透明度不一，通常能知道大致数据来源，但完整配方常不全。 |

### 5.3 基本不透明的新主线 / 闭源主线
| 模型族 | 训练集情况 |
|------|------------|
| **SD3 / SD3.5** | 精确训练集与后续对齐数据通常**未完整公开**。 |
| **FLUX.1-dev / schnell** | 训练语料与数据混合策略**未完整公开**。 |
| **Midjourney / DALL·E 3 / Imagen 3 / Gemini image stack / GPT-4o 图像生成** | 基本属于**闭源 proprietary web-scale mixture**，外部研究者无法精确知道训练集组成。 |
| **CogView4 等新支线** | 多数只知道模型与能力，不知道完整训练数据。 |

### 5.4 这意味着什么
1. **公开基线更容易被系统审计**：所以很多 benchmark 依然反复测 SD1.5 / SDXL / FLUX。
2. **闭源主线更像黑箱评测对象**：大家更多只能测输出与行为，难以做“训练集→偏差→行为”的因果分析。
3. **今后的 benchmark 必须默认“训练集未知”**：因此越来越多工作转向评输出、评评分器、评传播链，而不是假设能拿到训练配方。

---

## 6. 如果你只想快速抓重点，建议这样看

### 6.1 做安全审核 / 红队
优先盯：
- **ASR / MDR / 过滤器 Recall / FPR**
- 数据集：**TwoHamsters、T2ISafety、UnsafeBench**

### 6.2 做概念擦除 / 对齐
优先盯：
- **ASR + UDA + MCP + FID + CLIP**
- 数据集：**SALMUBench + 各类概念擦除协议 + TwoHamsters**

### 6.3 做检测 / 溯源 / 归因
优先盯：
- **Robust ROC AUC、bAcc、Unseen Acc.、Auth. Acc.、IoU**
- 数据集：**NTIRE 2026、QuAD、IABench、Dual-Guard 协议**

### 6.4 做公平性 / 评分器治理
优先盯：
- **CBS / BA / KL / CAR / CCS / ΔNSFW**
- 数据集：**T2I-BiasBench、Bias at the End of the Score、Operationalizing Fairness、HEIM**

---

## 7. 一个更实用的总表

| 目标问题 | 先看指标 | 再看 benchmark | 最常被测模型 |
|---------|---------|----------------|------------|
| 能不能绕过安全过滤 | ASR / MDR / Recall / FPR | TwoHamsters / T2ISafety / UnsafeBench | SD1.5、SDXL、SD3.5、FLUX、闭源商业模型 |
| 擦除有没有删干净且不误伤 | ASR / UDA / MCP / FID / CLIP | SALMUBench + 擦除协议 | SD1.5、SD2、SDXL、SD3、FLUX |
| 图像是不是 AI 生成 / 哪家生成 / 是否被改 | Robust ROC AUC / bAcc / Unseen Acc. / IoU | NTIRE 2026 / QuAD / IABench / Dual-Guard | SD 系列、FLUX、Midjourney、DALL·E、Imagen、CogView |
| 是否存在 demographic / cultural / reward bias | Entropy / CBS / BA / CAR / CCS / ΔNSFW | T2I-BiasBench / Bias-at-Score / HEIM | SD1.5、BK-SDM、Koala、Gemini / Imagen、FLUX、SD3.5 |

---

## 8. 最后一句判断

如果你今天问“**T2I 主线模型到底在测什么**”，我的判断是：

> 现在真正的主线不再是“生成质量 + 文图对齐”两件事，而是 **违规风险、概念治理、溯源归因、偏见治理** 四线并跑；而训练集层面的可解释性，反而在新主线模型上越来越差。

这也是为什么：**评测协议越来越细，训练数据却越来越黑箱。**
