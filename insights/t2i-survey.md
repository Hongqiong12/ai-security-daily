# T2I 文生图安全 Survey：攻防前沿与概念擦除技术演进

> **Survey 类型**: 基于项目论文库的系统性综述（Literature-Grounded Survey）  
> **数据基础**: 本项目收录的 **65** 篇 T2I 安全论文（2019–2026）
> **更新日期**: 2026-04-17
> **关联文档**: [前瞻总览](./AI_Security_Landscape_2026.md) · [T2T Survey](./t2t-survey.md)

---

## 摘要

文生图（Text-to-Image, T2I）安全研究以扩散模型为核心战场，形成了三个相互缠绕的研究主线：**越狱攻击**（如何绕过内容安全过滤器生成违禁图像）、**概念擦除/机器遗忘**（如何从模型参数中移除有害概念的表示）、**水印与溯源**（如何标记并追踪模型生成的内容）。本 Survey 基于本项目持续收录的 T2I 论文，完整梳理了从 GAN 时代到扩散模型时代的 T2I 安全演进，揭示了概念擦除技术从全局擦除向精准定位神经元、解析几何投影与运行时优化三路分化的演进路线，以及攻击方法从人工设计向 LLM 辅助自动化与现实场景鲁棒评测的转变。

---

## 目录

1. [研究背景：为什么 T2I 安全独特](#1-研究背景为什么-t2i-安全独特)
2. [越狱攻击：突破 T2I 内容安全过滤器](#2-越狱攻击突破-t2i-内容安全过滤器)
3. [概念擦除与机器遗忘：防御的核心范式](#3-概念擦除与机器遗忘防御的核心范式)
4. [前处理防御：过滤器与提示词检测](#4-前处理防御过滤器与提示词检测)
5. [水印保护：内容归属与版权防护](#5-水印保护内容归属与版权防护)
6. [基准评测](#6-基准评测)
7. [2026 新兴挑战：多模态与单流 Transformer](#7-2026-新兴挑战多模态与单流-transformer)
8. [关键发现与研究空白](#8-关键发现与研究空白)
9. [未来方向](#9-未来方向)
10. [论文索引](#10-论文索引)

---

## 1. 研究背景：为什么 T2I 安全独特

### 1.1 扩散模型的安全特殊性

与 LLM 安全相比，T2I 安全具有三个独特性：

**① 隐式知识存储**：LLM 的知识以 token 概率分布的形式存储，可以通过 RLHF 显式训练拒绝有害输出。而扩散模型的"知识"（概念、风格、人物等）以分散的权重模式存储，**没有直接的"拒绝"输出机制**，只能通过修改潜空间来影响生成。

**② 语义-视觉 Gap**：图像内容的有害性判断比文本更模糊——同样的图像内容在不同语境（医学教育 vs. 色情内容）下有害性完全不同。这使得基于规则的内容安全过滤在视觉领域更难泛化。

**③ 开放生态的挑战**：Stable Diffusion 系列模型完全开源，用户可以自由下载并在本地运行，这使得基于 API 的内容安全过滤完全失效。**T2I 安全的核心战场在于模型参数本身**，而非接口层。

### 1.2 研究规模与分布

截至 2026-04-17，本 Survey 锚定本项目已收录的 **65** 篇 T2I 安全论文。当前 T2I 安全版图已经不再是“越狱 vs 过滤器”的单线叙事，而是至少分裂成三条强主线：

- **概念擦除 / 机器遗忘**：从权重微调走向 closed-form projection、depth-aware removal 与 activation-level intervention；
- **现实世界评测**：从 clean setting 转向 robustness-in-the-wild、near-duplicate 传播链、质量退化与伪造链路；
- **模型生命周期治理**：后门检测、身份验证、水印鲁棒性、开源再微调稳定性开始一起进入主战场。

从时间分布看，研究主体仍高度集中在 **2022–2026 的扩散模型时代**；而 2026 年的新论文尤其突出两个趋势：一是 concept erasure 的解析化/结构化，二是 AIGC 检测开始真正面向真实分发链路而非实验室 clean benchmark。

---

## 2. 越狱攻击：突破 T2I 内容安全过滤器

### 2.1 攻击面分析

T2I 系统的内容安全防线通常由两层构成：
1. **提示词过滤器**（Text Safety Filter）：在文本进入扩散模型前过滤有害词汇
2. **图像安全分类器**（NSFW Classifier）：在图像生成后检测违禁内容

越狱攻击的目标是同时绕过这两层过滤，或利用两层之间的"语义不一致"。

### 2.2 基于强化学习的语义绕过

**SneakyPrompt**（[2305.12082](https://arxiv.org/abs/2305.12082)）是 T2I 越狱研究的开创性工作之一。其核心思想是**用强化学习搜索能绕过安全过滤器的替代词**：

```python
# SneakyPrompt 核心逻辑（概念示意）
def search_bypass_prompt(harmful_intent, safety_filter, t2i_model):
    env = T2IEnvironment(t2i_model, safety_filter)
    
    # 奖励：绕过安全过滤器 + 图像语义与 harmful_intent 相关
    reward = bypass_reward + semantic_similarity
    
    # RL 搜索替代词（如 "explicit" → "anatomical", "naked" → "unclothed")
    policy = RLAgent(state=prompt, action=replace_word)
    return policy.optimize(env, harmful_intent)
```

**FLIRT**（[2308.04265](https://arxiv.org/abs/2308.04265)）将 In-Context Learning 应用于越狱，通过少量示例（few-shot）引导攻击模型生成有效越狱提示。

### 2.3 感知层越狱

**Perception-guided Jailbreak**（[2408.10848](https://arxiv.org/abs/2408.10848)）提出了一种独特的攻击视角——**利用人类感知与扩散模型理解之间的差异**：

- 构造对人类无害但对扩散模型触发有害生成的提示词
- 利用扩散模型对某些词汇的独特理解方式（训练数据偏见）
- 攻击效果对人类审核员不易察觉

### 2.4 纯黑盒查询攻击

随着越来越多的 T2I 服务只提供 API（不暴露梯度），**无梯度黑盒攻击**成为重要方向：

**DiffZOO**（[2408.11071](https://arxiv.org/abs/2408.11071)）基于**零阶优化（Zeroth Order Optimization）**，在仅有模型输出（图像）的情况下估计梯度方向，实现黑盒对抗样本构造：

```
优化过程：
  x_{t+1} = x_t - η · Ĝ(x_t)
  其中 Ĝ(x_t) 是通过有限差分估计的梯度：
  Ĝ(x_t) ≈ [f(x + δe_i) - f(x - δe_i)] / (2δ)  ∀i
```

### 2.5 LLM 辅助 T2I 攻击（2024–2026 的主流）

2024 年之后，利用 LLM 自动化生成越狱提示成为 T2I 攻击的主要趋势：

**JailFuzzer**（[2408.00523](https://arxiv.org/abs/2408.00523)）：
- 将软件模糊测试与 LLM Agent 结合
- LLM 负责生成语义连贯的"变异提示"，模糊测试框架负责系统化探索

**Jailbreaking T2I via LLM**（[2503.01839](https://arxiv.org/abs/2503.01839)）：
- 直接用 LLM 的语言理解能力构造语义攻击
- LLM 分析安全过滤器的拒绝模式，自适应调整攻击策略

**Reason2Attack**（[2503.17987](https://arxiv.org/abs/2503.17987)）：
- 利用多模态 LLM 的**推理能力**来设计 T2I 攻击
- 模型通过推理"哪种描述方式能使扩散模型生成 X"来构造攻击

**GenBreak**（[2506.10047](https://arxiv.org/abs/2506.10047)）：
- 通用破解框架，针对多个主流 T2I 服务的统一黑盒攻击

**MMA-Diffusion**（[2311.17516](https://arxiv.org/abs/2311.17516)）：
- 多模态对齐攻击，同时利用文本和图像模态绕过安全过滤

### 2.6 动态注意力后门

**Dynamic Attention Backdoor**（[2504.20518](https://arxiv.org/abs/2504.20518)）代表了一类独特的攻击——**不是在推理时越狱，而是在训练时植入后门**：
- 在扩散模型的注意力机制层植入触发器
- 特定触发词（trigger token）出现时，注意力图发生特定变化，激活隐藏的有害生成行为
- 在没有触发器的情况下，模型表现完全正常，难以被安全评估发现

**PromptSAN**（[2506.18325](https://arxiv.org/abs/2506.18325)）：
- 基于提示词的自适应 T2I 攻击，根据目标模型的防御策略动态调整

### 2.7 文本渲染能力带来的新攻击面：铭文式越狱 (2026-04-08 新增)

随着 DALL·E 3、Flux 等模型在渲染清晰文本方面的巨大进步，T2I 模型出现了被称为 **"铭文式越狱" (Inscriptive Jailbreak)** 的全新攻击面。

**Etch**（[2604.05853](https://arxiv.org/abs/2604.05853)）首次系统化了这一类别：
- **攻击区别**：传统越狱生成"有害的视觉画面"（如色情、暴力），而铭文式越狱生成"视觉无害的画面，但包含有害的渲染文本"（如欺诈传单、假公文、钓鱼链接）。
- **防御盲区**：目前的内容安全分类器（如 NudeNet 或其他 NSFW 过滤器）完全无法检测渲染文本的语义。
- **攻击框架**：通过将 prompt 拆分为"语义伪装层、视觉锚定层、排版编码层"，结合 VLM（视觉语言模型）的反馈循环进行零阶优化。
- **意义**：这意味着 T2I 防御体系必须在未来集成 OCR（光学字符识别）与文本语义审查管道，但这将带来极大的延迟和计算成本挑战。

---

## 3. 概念擦除与机器遗忘：防御的核心范式

### 3.1 概念擦除的研究动机

T2I 模型的有害生成能力来源于训练数据中大量 NSFW 内容的表示被嵌入模型权重。**概念擦除（Concept Erasure）**的目标是在不重新训练模型的前提下，从参数中"遗忘"特定有害概念，同时最小化对无害生成能力的损伤。

这是一个典型的**约束优化问题**：
```
minimize  L_erase(c)     # 擦除目标概念 c 的生成能力
subject to  L_retain(C') ≤ ε  # 保留其他概念 C' 的生成质量
```

### 3.2 第一代：文本引导的权重调整（2022–2023）

**Safe Latent Diffusion (SLD)**（[2211.05105](https://arxiv.org/abs/2211.05105)，CVPR 2023）：
- 在扩散过程中引入安全引导信号，无需修改模型权重
- 通过负向 Classifier-Free Guidance 抑制 NSFW 特征方向
- **局限**：推理时增加计算成本，且不修改模型参数（攻击者可绕过引导信号）

**SEGA: Semantic Guidance**（[2301.12247](https://arxiv.org/abs/2301.12247)）：
- 通用的语义引导框架，可用于安全控制
- 允许多个引导信号叠加，实现复杂的概念控制

**ESD: Erasing Concepts from Diffusion Models**（[2303.07345](https://arxiv.org/abs/2303.07345)）：
- **直接修改模型权重**的概念擦除先驱
- 使用对比式微调：最小化目标概念的生成概率，同时保留其他概念

**Forget-Me-Not**（[2303.17591](https://arxiv.org/abs/2303.17591)）：
- 针对特定主题（如个人面孔）的遗忘学习
- 应用场景：GDPR 合规的"被遗忘权"实现

**Concept Ablation**（[2303.13516](https://arxiv.org/abs/2303.13516)）：
- 通过消融（ablation）训练移除特定概念
- 将目标概念的生成重映射到锚点概念

### 3.3 第二代：精确化与鲁棒化（2023–2024）

第二代概念擦除工作的核心问题是：**第一代方法擦除的概念可以通过对抗性提示词恢复**（即擦除后仍然可越狱）。

**UCE: Unified Concept Editing**（[2308.14761](https://arxiv.org/abs/2308.14761)）：
- 统一多个概念的同时擦除
- 引入"保留集"机制：在优化擦除目标的同时，显式保护相关无害概念

**R.A.C.E.: Robust Adversarial Concept Erasure**（[2405.16341](https://arxiv.org/abs/2405.16341)）：
- 在擦除过程中加入**对抗训练**：同时模拟攻击者的最优越狱策略
- 目标：擦除后的模型对已知越狱方法保持鲁棒

**Receler**（[2407.12383](https://arxiv.org/abs/2407.12383)）：
- "可靠且高效"的概念擦除
- 引入**知识蒸馏**保持无关概念的生成质量
- 实验显示：在概念擦除后对下游任务的性能损失最小

### 3.4 第三代：神经元精准定位（2024–2026）

第三代工作从"调整全局权重"转向"定位并修改负责有害概念的特定神经元/特征"：

**TRCE**（[2503.07389](https://arxiv.org/abs/2503.07389)）：
- 精确追踪有害概念在扩散模型中的"表示路径"
- 通过概念追踪定位关键层和注意力头

**Concept Corrector**（[2502.16368](https://arxiv.org/abs/2502.16368)）：
- 不仅"擦除"，还将有害概念"重定向"到无害替代概念
- 保持模型在相关语义空间的生成连贯性

**SPEED**（[2503.07392](https://arxiv.org/abs/2503.07392)）：
- 速度优先的概念擦除，专注于降低擦除的计算成本
- 提出高效的参数更新方案（稀疏更新，只修改最关键的参数）

**SAEUron**（[2501.18052](https://arxiv.org/abs/2501.18052)）：
- 利用**稀疏自编码器（Sparse Autoencoder, SAE）** 分析 T2I 模型中的特征表示
- 定位负责特定视觉概念的**单个神经元**（monosemantic features）
- **意义**：首次将 Anthropic 的机制可解释性技术（Toy Models of Superposition）应用于 T2I 安全

**Concept Pinpoint Eraser (CPE)**（[2506.22806](https://arxiv.org/abs/2506.22806)）：
- 以"外科手术式"精度定位并擦除概念神经元
- 理论上可实现零副作用的概念移除（仅修改与目标概念关联的少数神经元）

**Z-Erase**（[2603.25074](https://arxiv.org/abs/2603.25074)）：
- 专为**单流扩散 Transformer（如 Flux）** 设计的概念擦除方法
- 现有大多数擦除方法为 U-Net 扩散架构设计，Z-Erase 填补了新一代架构的研究空白
- 利用单流架构中的统一注意力机制实现更精确的概念定位


### 3.6 精细化区域安全控制与 DPO（2026-04-09 新增）

**SafeCtrl**（[2604.03941](https://arxiv.org/abs/2604.03941)）：
传统的全局遗忘往往造成无害上下文的保真度损失。
- 核心方法：基于“先检测后抑制（Detect-Then-Suppress）”范式的区域感知（Region-Aware）安全控制。
- 创新点：使用注意力引导检测有害区域掩码，随后在掩码区域内利用图像级直接偏好优化（DPO）专门中和有害语义，实现图像局部安全替换（如给违禁物品“打马赛克”或替换为无害物品），而不影响背景。

### 3.5 概念擦除技术的演进全图

```
精准度
  高 │              CPE    Z-Erase
     │          SAEUron
     │       TRCE  Concept-Corrector
     │    RACE  Receler  SPEED
     │  UCE
     │ ESD  Forget-Me-Not  CA
     │SEGA  SLD
  低 └────────────────────────────────► 时间
      2022    2023    2024    2025    2026
                                          
    ←─全局权重调整─→←─区域精准─→←─单神经元─→
```

### 3.9 新兴范式：推理时能量引导概念擦除 (2026-04-13 新增)

**EGLOCE**（[2604.09405](https://arxiv.org/abs/2604.09405)）提出了概念擦除的**第三条路径**：

```
擦除技术路线图:
  路线一: 权重微调 (ESD, UCE, MACE) → 需训练，改参数，泛化代价高
  路线二: 激活操纵 (ActErase, SafeCtrl, FlowGuard) → 不训练，操作中间层
  路线三: 潜空间能量优化 (EGLOCE) → 不训练，直接优化采样轨迹 ⭐ NEW
```

**核心方法**:
- **排斥能量 E_repel**: 在潜空间通过梯度下降将采样推离目标概念区域
- **保留能量 E_retain**: 用 CLIP 相似度保持与原始 prompt 的语义对齐
- **联合优化**: 每个 denoising step 内执行 K 次（3-10次）梯度更新

**关键意义**: 标志着概念擦除从"改参数时代"正式进入"优化轨迹时代"。但这也意味着：
- 攻击者可用同样的**潜空间优化思路来恢复被擦除的概念**
- 双能量框架的理论保证（收敛性、全局最优性）仍待建立
- 与 LoRA 擦除秩亏分析的关系值得深入研究（潜空间维度 vs 能量地形）

- **优势**: 即插即用、不修改权重、对抗鲁棒性强
- **局限**: 推理延迟增加 2-5x、超参数需按目标调节、依赖特征中心预计算

### 3.10 新兴范式：闭式双投影擦除（Closed-Form Double Projections） (2026-04-15 新增)

**DP / Closed-Form Concept Erasure**（[2604.10032](https://arxiv.org/abs/2604.10032)）把概念擦除再次推进了一步：

- **核心机制**：不再做 retraining 或 iterative optimization，而是把擦除重写成两个解析可解的投影步骤——先把目标概念投影到安全子空间，再在 preserved concepts 的**左零空间**中求闭式更新。
- **关键结果**：在 SD 1.5 上，DP 将 mean erased accuracy 压到 **0.7%**，同时把 preservation drop 控制在 **1.8%**；对一般 ImageNet 非目标类的平均 accuracy drop 仅 **0.43%**，显著优于 UCE 的 **4.43%**。在 FLUX 上 preservation drop 也从 UCE 的 **23.9%** 降到 **6.6%**。
- **意义**：这标志着概念擦除正式进入“**训练自由 + 显式 preservation 约束**”时代。相比早期方法只是把 preservation 当作软惩罚项，DP 把“保留无关概念”直接写成线性硬约束，更贴近你关注的最小覆盖与结构性保真目标。

### 3.8 新兴范式：线性子空间移除 (Linear Subspace Removal)

在概念擦除的演进中，**线性子空间移除 (ISP, Identity Sanitization Projection)** [2604.05296](https://arxiv.org/abs/2604.05296) 代表了一种直接针对潜空间（Latent Space）进行代数操作的防御范式。该方法的核心逻辑在于：
1. **子空间提取**：通过提取同类概念（如不同视角的同一身份）在表征空间中的协方差主成分，定义概念所占据的线性子空间。
2. **正交投影**：构建投影矩阵 $P = I - U U^T$，将潜变量强制投影到与概念子空间正交的互补空间中。
3. **理论意义**：这为研究“模型参数空间中的线性干预”提供了一个基准。我们正在推进的“概念流形的非满秩不完备性”研究，正是以上述此类基于线性映射（或 LoRA 的低秩线性扰动）的防御范式为靶标，从流形曲率的角度指出其根本性弱点。

### 3.11 新兴范式：深度感知类遗忘（Depth-Aware Class Unlearning）(2026-04-17 新增)

**DAMP**（[2604.15166](https://arxiv.org/abs/2604.15166)）把 class unlearning 从“删输出头”推进到“逐层删方向”：
- **核心机制**：先在每一层估计 forget-specific directions，再用 depth-aware projection 逐层移除，而不是只在最后几层或 logits 端做 mask；
- **关键结果**：论文报告在绝大多数设置下都能把 Forget Accuracy 压到接近 **0**，同时把保留类性能损失压在较低水平，说明 class-level forgetting 可以不再依赖大规模重训；
- **意义**：这条线本质上把 concept erasure 进一步细化成“**层深相关的方向清除**”，与 Closed-Form DP 的解析投影路线形成互补，也和你长期关注的低秩/子空间弱点问题直接相关。

---

## 4. 前处理防御：过滤器与提示词检测

### 4.1 基于文本过滤的防御

**SafeGen**（[2404.06666](https://arxiv.org/abs/2404.06666)）：
- 文本输入的安全检测，在提示词进入扩散模型前过滤有害内容
- 多标签分类器，覆盖多种有害内容类别

**PromptGuard**（[2501.03544](https://arxiv.org/abs/2501.03544)）：
- 专门针对绕过安全过滤器的对抗性提示词检测
- 基于大规模对抗样本数据集训练，对已知越狱变体具有鲁棒性

**MacPrompt**（[2601.07141](https://arxiv.org/abs/2601.07141)）：
- 利用提示词语义的多维分析检测潜在有害提示
- 特别关注语义绕过（用无害词汇描述有害内容）的检测

### 4.2 潜空间防御

**LatentGuard**（[2404.08031](https://arxiv.org/abs/2404.08031)）：
- 在扩散模型的**潜空间（Latent Space）** 中检测有害概念
- 相较于文本过滤，潜空间防御对语义绕过攻击更鲁棒（攻击者无法预测潜空间表示）

**SAFREE: Training-Free and Adaptive Guard**（[2410.12761](https://arxiv.org/abs/2410.12761)，ICLR 2025）：
- **无训练**的自适应安全守卫，适用于 T2I 和 T2V（文生视频）
- 在推理时动态调整扩散过程的去噪方向，无需修改模型参数
- **优势**：即插即用，不影响模型基础性能

**Safeguider**（[2510.05173](https://arxiv.org/abs/2510.05173)）：
- 结合文本过滤和生成过程引导的混合防御
- 可配置的安全级别，适应不同部署场景

### 4.3 多视觉检查防御

**GuardT2I**（[2403.01446](https://arxiv.org/abs/2403.01446)）：
- 专门针对 T2I 生成结果的安全检测器
- 多维度视觉分析（内容、风格、隐含语义）

**UPAM**（[2405.11336](https://arxiv.org/abs/2405.11336)）：
- 使用视觉检查器（visual checker）进行后处理安全验证
- 可集成到任意 T2I 生成流水线的末端

**ART: Automatic Red-teaming**（[2405.19360](https://arxiv.org/abs/2405.19360)）：
- 自动化红队工具，用于持续发现 T2I 过滤器的漏洞
- 兼顾对良性用户的误拒率（false positive rate）控制

**Modular LoRA**（[2412.00357](https://arxiv.org/abs/2412.00357)）：
- 模块化安全适配器，可无损地为现有扩散模型添加安全能力
- LoRA 格式，可独立更新安全模块而无需重训完整模型

### 4.4 主动响应扰动式后门检测（2026-04-17 新增）

**Scaling Exposes the Trigger / SET**（[2604.12446](https://arxiv.org/abs/2604.12446)）把 T2I 后门检测从“等异常自己暴露”改成“主动去戳交叉注意力”：
- 在 U-Net 早期 denoising steps 中，对 cross-attention score 施加受控 scaling，观察响应偏移轨迹；
- 再用单类边界学习拟合 benign response space，把后门样本看成被 scaling 放大的异常点；
- 在 5 类主流后门攻击上取得 **95.1% AUROC / 84.8% ACC**，对 IBA 这种隐式触发器仍保持 **92.9% AUROC**，明显优于依赖表面异常的旧方法。

---

## 5. 水印保护：内容归属与版权防护

### 5.1 水印研究的三种场景

T2I 水印研究围绕三个核心应用场景：

| 场景 | 问题 | 主要方法 |
|------|------|----------|
| **内容溯源** | 判断图像是否由某个特定模型生成 | 生成器端水印（模型权重中嵌入） |
| **版权追踪** | 识别生成图像中使用的受版权保护概念 | 概念级水印 |
| **内容归属** | 追踪特定图像由哪个用户请求生成 | 用户绑定水印 |

### 5.2 生成器端水印

**Stable Signature**（[2303.15435](https://arxiv.org/abs/2303.15435)，Meta FAIR）：
- 在扩散模型的**解码器（VAE Decoder）权重**中嵌入水印信息
- 所有该模型生成的图像都自动携带水印，无法通过 prompt 去除
- **强健性**：对常见图像处理操作（压缩、裁剪、滤波）保持水印可提取性

**数学形式**：
```
给定可训练解码器 D_θ：
优化目标：
  minimize  L_image(D_θ)     # 保持图像质量
  + λ · L_watermark(D_θ, m)  # 嵌入水印 m

提取：对任意生成图像 x：
  m' = Extractor(x)
  if similarity(m', m) > threshold: "confirmed generated by this model"
```

### 5.3 概念级水印

**Modular LoRA**（[2412.00357](https://arxiv.org/abs/2412.00357)）在水印方向的应用：
- 为特定版权内容（艺术家风格、IP 角色）嵌入独特的生成特征
- 可通过特征检测工具验证是否使用了受保护的概念

**SAEUron 的水印应用**（[2501.18052](https://arxiv.org/abs/2501.18052)）：
- 利用 SAE 发现的单义神经元，为特定概念嵌入激活层水印
- 相比权重水印，激活层水印对模型微调攻击更鲁棒

### 5.4 水印鲁棒性与攻击

本项目收录的论文对水印的攻击研究相对较少，但清华大学的 AI Security Survey（[2603.24857](https://arxiv.org/abs/2603.24857)）指出了两类主要水印攻击：
- **水印移除攻击**：通过图像处理或对抗扰动破坏水印信号
- **水印伪造攻击**：在非目标模型生成的图像中添加虚假水印，造成错误归属

---

### 5.5 双重鲁棒水印的崛起 (2026-04-09 新增)

**Towards Robust Content Watermarking Against Removal and Forgery Attacks**（[2604.06662](https://arxiv.org/abs/2604.06662)）：
现有水印容易被 JPEG 压缩洗掉（Removal），也容易被重放攻击利用（Forgery）。
- 机制：频域双频段分离注入冗余水印，结合密码学感知哈希绑定生成图像特征。
- 结论：在抵抗移除与防伪造的综合测试中取得了极高鲁棒性，预示水印安全将向密码学与隐写术的深度融合发展。

### 5.6 自回归图像生成水印的三难困境 (2026-04-14 新增)

**On the Robustness of Watermarking for Autoregressive Image Generation**（[2604.11720](https://arxiv.org/abs/2604.11720)）首次系统指出：AR watermark 的问题不只是“够不够鲁棒”，而是**去除、伪造、radioactive filtering 三个目标难以兼得**。

- **对 token-based watermark**：VQ-Regen 与 LatentOpt 证明其在黑盒或灰盒条件下就会出现明显退化，说明 AR token 量化边界本身就是攻击面。
- **对 BitMark**：常规 removal 很难，但一旦攻击者转向 bit-level removal 或频域伪造，系统会暴露新的脆弱性；更严重的是，若把检测阈值调低以支持 radioactive data filtering，又会明显放大 forgery 通过率。
- **意义**：这意味着 T2I 安全的来源证明体系不能只看“是否带 watermark”，而必须进一步思考 watermark 自身是否会反过来污染数据治理链路。对于开放式生成生态，这是一条非常值得持续追踪的新研究线。

## 6. 基准评测

### 6.1 T2I 安全专用 Benchmark

**JailbreakBench**（[2404.01318](https://arxiv.org/abs/2404.01318)）：
- 标准化越狱评估协议，统一 ASR（Attack Success Rate）计算方法
- 覆盖多个 T2I 模型（SD v1.5, SDXL, DALLE 系列）
- 提供标准化的违禁内容分类体系

**MIMMU（Multimodal Understanding Safety）**（[2603.00992](https://arxiv.org/abs/2603.00992)）：
- 多模态安全理解基准，测试 T2I 模型及 MLLM 对安全相关提示的理解
- 涵盖 6 大有害内容类别，20+ 语言

**Adversarial T2I Survey**（[1910.09399](https://arxiv.org/abs/1910.09399)）：
- 早期 GAN 时代的对抗攻击分类法综述，为后续扩散模型安全研究奠定分类基础

**NTIRE 2026 Challenge on Robust AI-Generated Image Detection in the Wild**（[2604.11487](https://arxiv.org/abs/2604.11487)，CVPR 2026 Workshop）：
- 首个把 **AIGC 检测的野外鲁棒性** 做成主赛题的挑战赛：108,750 张真实图像、185,750 张 AI 图像、42 个生成器、36 种图像变换。
- 以 **Robust ROC AUC** 为主指标，并采用 open / hidden test 双轨评测，推动检测研究从“clean 判别”转向“真实分发链路鲁棒识别”。

### 6.2 质量感知近重复校准检测（2026-04-17 新增）

**QuAD**（[2604.15027](https://arxiv.org/abs/2604.15027)）把 AIGC 检测进一步推进到“传播链 + 质量退化”的真实世界场景：
- **核心机制**：不再把 fake image 当作独立样本，而是显式建模 near-duplicate 传播链，并结合图像质量感知校准 logit；
- **关键结果**：在 ReWIND 基准上把平衡准确率从 **63.0** 提升到 **70.3**，把检测器从“识别生成痕迹”推进到“识别分发链路中的痕迹衰减”；
- **意义**：这说明 T2I benchmark 正在从“生成器闭集分类”转向“开放传播环境中的鲁棒鉴别”，与 NTIRE 2026 一起构成现实部署检测的新双支点。

### 6.3 评测维度与指标

基于本项目论文收录，T2I 安全评测主要使用以下指标：

| 指标 | 用途 | 计算方式 |
|------|------|----------|
| **ASR（Attack Success Rate）** | 衡量越狱攻击效果 | 成功生成违禁图像的比例 |
| **FID（Fréchet Inception Distance）** | 衡量擦除后图像质量 | 擦除前后生成图像分布差异 |
| **CLIP Score** | 衡量文-图对齐度 | 生成图像与提示词的语义相似度 |
| **Nudenet Score** | NSFW 内容检测 | 专用 NSFW 分类器的评分 |
| **Preservation Rate** | 衡量无关概念保留 | 擦除后无关概念生成质量保留比例 |

---

## 7. 2026 新兴挑战：多模态与单流 Transformer

### 7.1 单流扩散 Transformer（DiT）带来的架构安全挑战

2024–2025 年，以 **Flux** 和 **Stable Diffusion 3.0** 为代表的**单流扩散 Transformer（Single-Stream DiT）** 开始取代传统 U-Net 扩散架构。这一架构变化给 T2I 安全研究带来了根本性挑战：

**架构差异**：

| 特性 | 传统 U-Net 扩散 | 单流 DiT（Flux/SD3） |
|------|----------------|---------------------|
| 特征提取 | 分离的 encoder/decoder | 统一的 Transformer 流 |
| 概念存储 | 分层存储，有明确的语义层 | 混合存储，难以定位 |
| 注意力机制 | 空间注意力为主 | 全局 + 局部联合注意力 |
| 擦除可行性 | ESD、UCE 等方法适用 | 需要专用方法 |

**Z-Erase**（[2603.25074](https://arxiv.org/abs/2603.25074)）是目前针对单流 DiT 的**第一个专用概念擦除方法**，在架构层面做出了以下适配：
- 利用单流架构中文本和图像特征**共享同一注意力空间**的特性
- 在联合注意力空间中定位有害概念的表示向量
- 通过针对 DiT 的梯度更新策略实现概念遗忘

**DTVI**（[2603.22041](https://arxiv.org/abs/2603.22041)）：
- 专门研究新型 T2I 架构的安全漏洞
- 发现单流 Transformer 相比 U-Net 在某些越狱场景下更脆弱

### 7.2 MLLM 引入的新 T2I 攻击面

**When Understanding Becomes a Risk: MLLM Safety**（[2603.24079](https://arxiv.org/abs/2603.24079)，CVPR 2026）：

核心论断：**多模态 LLM（MLLM）的图像理解能力本身就是一个安全漏洞**。

攻击机制：
1. MLLM 能理解图像中的隐含语义（如不完整的/模糊的 NSFW 图像）
2. MLLM 将这些隐含语义转化为文字描述
3. 该描述被用作 T2I 模型的 prompt，生成完整的 NSFW 图像

```
模糊/不完整的违规图像
    → MLLM 理解并描述图像语义
    → 描述文字 → T2I 模型
    → 完整违规图像生成
```

这意味着：当 MLLM 与 T2I 模型结合使用时，MLLM 的"帮助性理解"能力可以成为 T2I 安全过滤器的旁路。

**Janus**（[2603.21208](https://arxiv.org/abs/2603.21208)）：
- 提出了多模态安全的"双面神"问题——模型的多模态理解和生成能力是同一枚硬币的两面

### 7.2 T2I 模型生命周期安全（2026-03-30 新增）

本期出现了两篇关注 T2I 安全**全生命周期管理**的重要工作（均被 CVPR 2026 接收），标志着 T2I 安全研究从单纯的内容过滤走向更广泛的模型治理：

**Verify Claimed T2I Models via Boundary-Aware Prompt Optimization**（[2603.26328](https://arxiv.org/abs/2603.26328)，CVPR 2026 Findings）：

解决"T2I API 身份验证"问题——第三方平台可能谎称使用某知名 T2I 模型。BPO（边界感知提示优化）通过挖掘目标模型在**语义决策边界**处的独特行为，生成模型特异性验证提示，无需多参考模型即可完成高精度验证。

```
核心洞察：不同 T2I 模型在"语义边界区域"（概念过渡区）行为差异最大
→ 利用此差异生成"仅目标模型会不稳定响应"的验证提示
→ 验证准确率显著优于 4 种基线方法（5 个主流模型测试）
```

**SALMUBench: A Benchmark for Sensitive Association-Level Multimodal Unlearning**（[2603.26316](https://arxiv.org/abs/2603.26316)，CVPR 2026）：

首个针对多模态对比学习模型（CLIP 类）的**关联级遗忘**评测基准：
- 6 万条合成"人物-属性"敏感关联数据集
- 受损模型 vs 干净模型的双模型对照设置（精确隔离遗忘效果）
- 关键发现：现有遗忘方法均陷入"遗忘不足 vs 过度泛化"的二元困境

两篇论文共同指向 T2I 安全的新前沿方向：**模型可信度验证 + 知识可控遗忘**。



### 8.1 五大关键发现

**发现一：概念擦除方法均面临"擦除-保留 trade-off"且尚无最优解**

从 ESD 到 Z-Erase 的七年演进，核心张力始终未得到根本性解决：**擦除目标概念必然影响邻近无害概念**。SAEUron 和 CPE 代表了"精准手术"方向的最高成就，但其计算成本和对新架构的适配性仍是瓶颈。

**发现二：对抗鲁棒的概念擦除仍是开放问题**

RACE 和 Receler 等工作在已知攻击上获得了鲁棒性，但面对 DiffZOO、Reason2Attack 等新型攻击，擦除效果仍会退化。概念擦除和越狱攻击之间存在持续的军备竞赛。

**发现三：开源生态使所有服务端防御失效**

Stable Diffusion 完全开源意味着用户可以：(a) 使用未擦除的旧版本模型，(b) 对擦除后的模型进行再微调恢复有害能力。**模型参数级别的安全才是唯一根本性的解决方案**。

**发现四：单流 Transformer 架构的安全研究严重滞后**

Flux 和 SD3 已经成为 2025–2026 年的主流 T2I 架构，但截至本 Survey 写作时，针对该架构的安全研究论文仍极少（Z-Erase 和 DTVI 是先驱）。现有安全基准几乎全部基于 SD v1.5 和 SDXL，评估结果在新架构上的泛化性存疑。

**发现五：MLLM 理解能力带来的 T2I 旁路攻击是 2026 年最重要的新威胁**

论文 [2603.24079]（CVPR 2026）揭示的 MLLM-assisted T2I 旁路攻击，打破了"只需保护 T2I 模型本身"的假设。当 MLLM 和 T2I 模型在同一系统中协作时，安全边界需要重新划定。

### 8.2 三大研究空白

**空白一：单流 DiT 架构的系统性安全评估**

需要建立专门针对 Flux/SD3 架构的安全基准、越狱数据集和概念擦除方法，不能直接套用现有 U-Net 方法。

**空白二：开源模型再微调的安全稳定性**

类似于 T2T 的 Internal Safety Collapse，T2I 概念擦除后的模型在用户微调（LoRA fine-tuning）后安全性如何变化，目前研究几乎空白。

**空白三：视频生成（T2V）的安全研究**

本项目收录的 SAFREE 覆盖了 T2V，但整体而言，T2V 的越狱攻击和概念擦除研究远少于 T2I，而 Sora/Gen-3 等视频生成模型的普及使这一方向的重要性快速上升。

---

## 9. 未来方向

### 9.1 近期（1–2 年）

**A. Flux/SD3 安全专项研究**：建立针对单流 DiT 架构的完整安全评测体系，包括攻击方法、概念擦除技术和防御过滤器。

**B. 多模态安全边界重定义**：在 MLLM + T2I 协作系统中，建立跨模态的安全评估框架，解决 MLLM 理解能力带来的 T2I 旁路问题。

**C. LoRA 微调后的安全保持**：研究如何在允许用户 LoRA 微调的同时，保证安全对齐特性不被破坏（可参考 T2T 的双目标优化对齐思路）。

### 9.2 中期（3–5 年）

**D. 生成内容的可验证归属体系**：建立从水印嵌入到法律认可的完整内容归属技术链，与版权法规对接（Stable Signature 是技术先驱，但法律框架尚不成熟）。

**E. 统一多模态安全框架**：覆盖 T2I、T2V、I2I、MLLM 的统一安全评估框架，支持跨模态攻击的一体化检测和防御。

### 9.3 长期（5+ 年）

**F. 生成式 AI 伦理合规的技术保障**：随着生成式 AI 进入广泛的社会应用场景，技术安全研究需要与法律、伦理、监管框架紧密结合，构建"技术合规即服务（Compliance as a Service）"的基础设施。

---

## 10. 论文索引

### 越狱/攻击类（代表性选摘）

| 论文名称 | ArXiv ID | 年份 | 攻击类型 | 核心方法 |
|----------|----------|------|----------|----------|
| Adversarial T2I Survey | [1910.09399](https://arxiv.org/abs/1910.09399) | 2019 | 综述 | GAN 对抗攻击分类法 |
| SneakyPrompt | [2305.12082](https://arxiv.org/abs/2305.12082) | 2023 | 越狱 | RL 搜索替代词绕过过滤器 |
| FLIRT | [2308.04265](https://arxiv.org/abs/2308.04265) | 2023 | 越狱 | In-Context Learning 越狱 |
| MMA-Diffusion | [2311.17516](https://arxiv.org/abs/2311.17516) | 2023 | 越狱 | 多模态对齐攻击 |
| Perception Jailbreak | [2408.10848](https://arxiv.org/abs/2408.10848) | 2024 | 越狱 | 感知-理解 gap 利用 |
| DiffZOO | [2408.11071](https://arxiv.org/abs/2408.11071) | 2024 | 黑盒攻击 | 零阶优化无梯度攻击 |
| JailFuzzer | [2408.00523](https://arxiv.org/abs/2408.00523) | 2024 | 越狱 | LLM Agent + 模糊测试 |
| Jailbreaking via LLM | [2503.01839](https://arxiv.org/abs/2503.01839) | 2025 | 越狱 | LLM 语义攻击构造 |
| Reason2Attack | [2503.17987](https://arxiv.org/abs/2503.17987) | 2025 | 越狱 | 推理能力辅助攻击 |
| Dynamic Attention Backdoor | [2504.20518](https://arxiv.org/abs/2504.20518) | 2025 | 后门 | 注意力机制后门植入 |
| GenBreak | [2506.10047](https://arxiv.org/abs/2506.10047) | 2025 | 越狱 | 通用黑盒越狱框架 |
| Modifier Unlocked | [11023413](https://arxiv.org/abs/11023413) | 2025 | 越狱 | 提示词修饰词越狱 |
| Hidden Ads | [2603.27522](https://arxiv.org/abs/2603.27522) | 2026 | 后门/广告注入 | 语义行为触发VLM后门，广告植入 |
| SHIFT | [2603.29742](https://arxiv.org/abs/2603.29742) | 2026 | 水印攻击 | 无训练随机轨迹偏转破除扩散水印 |

### 概念擦除/机器遗忘类（代表性选摘）

| 论文名称 | ArXiv ID | 年份/会议 | 核心贡献 |
|----------|----------|-----------|----------|
| SLD | [2211.05105](https://arxiv.org/abs/2211.05105) | CVPR 2023 | 潜空间安全引导 |
| SEGA | [2301.12247](https://arxiv.org/abs/2301.12247) | NeurIPS 2023 | 语义引导框架 |
| ESD | [2303.07345](https://arxiv.org/abs/2303.07345) | 2023 | 权重级概念擦除先驱 |
| Concept Ablation | [2303.13516](https://arxiv.org/abs/2303.13516) | 2023 | 概念消融训练 |
| Forget-Me-Not | [2303.17591](https://arxiv.org/abs/2303.17591) | 2023 | 个体主题遗忘 |
| UCE | [2308.14761](https://arxiv.org/abs/2308.14761) | 2023 | 统一多概念编辑 |
| R.A.C.E. | [2405.16341](https://arxiv.org/abs/2405.16341) | 2024 | 对抗鲁棒概念擦除 |
| Receler | [2407.12383](https://arxiv.org/abs/2407.12383) | 2024 | 可靠高效概念擦除 |
| SPEED | [2503.07392](https://arxiv.org/abs/2503.07392) | 2025 | 高效稀疏参数更新 |
| TRCE | [2503.07389](https://arxiv.org/abs/2503.07389) | 2025 | 精准概念路径追踪 |
| Concept Corrector | [2502.16368](https://arxiv.org/abs/2502.16368) | 2025 | 概念重定向 |
| CPE | [2506.22806](https://arxiv.org/abs/2506.22806) | 2025 | 精准神经元擦除 |
| Z-Erase | [2603.25074](https://arxiv.org/abs/2603.25074) | 2026 | 单流 DiT 专用擦除 |
| Closed-Form DP | [2604.10032](https://arxiv.org/abs/2604.10032) | 2026 | 双投影闭式擦除 (NEW) |
| DAMP | [2604.15166](https://arxiv.org/abs/2604.15166) | 2026 | 深度感知类遗忘：分层移除 forget-specific directions 的 one-shot class unlearning (NEW) |
| SafeCtrl | [2604.03941](https://arxiv.org/abs/2604.03941) | 2026 | 区域擦除：Detect-Then-Suppress DPO 局部替换 |

### 前处理/过滤防御类（代表性选摘）

| 论文名称 | ArXiv ID | 年份/会议 | 核心方法 |
|----------|----------|-----------|----------|
| GuardT2I | [2403.01446](https://arxiv.org/abs/2403.01446) | 2024 | 多维视觉安全检测 |
| SafeGen | [2404.06666](https://arxiv.org/abs/2404.06666) | 2024 | 文本过滤分类器 |
| LatentGuard | [2404.08031](https://arxiv.org/abs/2404.08031) | 2024 | 潜空间概念检测 |
| UPAM | [2405.11336](https://arxiv.org/abs/2405.11336) | 2024 | 视觉检查器后处理 |
| ART | [2405.19360](https://arxiv.org/abs/2405.19360) | 2024 | 自动化红队工具 |
| SAFREE | [2410.12761](https://arxiv.org/abs/2410.12761) | ICLR 2025 | 无训练自适应守卫 |
| PromptGuard | [2501.03544](https://arxiv.org/abs/2501.03544) | 2025 | 对抗提示词检测 |
| MacPrompt | [2601.07141](https://arxiv.org/abs/2601.07141) | 2026 | 多维语义分析过滤 |
| Scaling Exposes the Trigger | [2604.12446](https://arxiv.org/abs/2604.12446) | 2026 | 主动后门检测：通过 cross-attention scaling 学习 benign response boundary (NEW) |

### 水印/溯源类（代表性选摘）

| 论文名称 | ArXiv ID | 年份/机构 | 核心贡献 |
|----------|----------|-----------|----------|
| Stable Signature | [2303.15435](https://arxiv.org/abs/2303.15435) | 2023/Meta FAIR | VAE 解码器端水印 |
| Modular LoRA | [2412.00357](https://arxiv.org/abs/2412.00357) | 2024 | 模块化安全适配器 |
| SAEUron | [2501.18052](https://arxiv.org/abs/2501.18052) | 2025 | SAE 神经元水印 |
| RobustWatermark | [2604.06662](https://arxiv.org/abs/2604.06662) | 2026 | 双重鲁棒频域水印 |
| FRAP | [2408.11706](https://arxiv.org/abs/2408.11706) | 2024 | 鲁棒提示自适应水印 |

### 基准/多模态（代表性选摘）

| 论文名称 | ArXiv ID | 年份/会议 | 类型 |
|----------|----------|-----------|------|
| JailbreakBench | [2404.01318](https://arxiv.org/abs/2404.01318) | 2024 | 标准化越狱基准 |
| MIMMU | [2603.00992](https://arxiv.org/abs/2603.00992) | 2026 | 多模态安全理解 |
| PromptSAN | [2506.18325](https://arxiv.org/abs/2506.18325) | 2025 | 自适应攻击防御 |
| MLLM Safety Risk | [2603.24079](https://arxiv.org/abs/2603.24079) | CVPR 2026 | MLLM 安全风险分析 |
| Janus | [2603.21208](https://arxiv.org/abs/2603.21208) | 2026 | 多模态双面安全 |
| DTVI | [2603.22041](https://arxiv.org/abs/2603.22041) | 2026 | 新架构 T2I 漏洞 |
| BPO Verify T2I | [2603.26328](https://arxiv.org/abs/2603.26328) | CVPR 2026 | T2I 模型身份验证基准 |
| SALMUBench | [2603.26316](https://arxiv.org/abs/2603.26316) | CVPR 2026 | 多模态关联级遗忘基准 |
| NTIRE 2026 Robust AIGC Detection | [2604.11487](https://arxiv.org/abs/2604.11487) | CVPR 2026 Workshop | 现实世界鲁棒 AIGC 检测基准 (NEW) |
| QuAD | [2604.15027](https://arxiv.org/abs/2604.15027) | CVPR 2026 Workshop | near-duplicate + 质量感知校准的开放链路 AIGC 检测 (NEW) |

---

*本 Survey 由 `paper-research` skill 自动生成，基于项目截至 2026-04-17 收录的 T2I 论文（65 篇）。*  
*上次 Survey 更新：2026-04-17（新增 3 篇：2604.12446 Scaling Exposes the Trigger、2604.15027 QuAD、2604.15166 DAMP）。*  
*下次更新时间：跟随每日自动化任务实时更新。*
