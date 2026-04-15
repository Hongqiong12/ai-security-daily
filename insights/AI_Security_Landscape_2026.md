# AI 大模型安全前沿洞察：现状理解与未来研究方向

> **数据来源**: 基于本项目收录的 **162 篇** AI 安全论文（2019–2026）系统性分析
> **更新日期**: 2026-04-15（v2.1 增量更新）
> **覆盖领域**: T2T（LLM 安全）· T2I（文生图安全）· Agentic Search（检索增强安全）  

---

## 目录

1. [宏观全局：基础模型时代的安全格局](#1-宏观全局基础模型时代的安全格局)
2. [T2T 安全：从越狱到 Agent 攻击的演进路线](#2-t2t-安全从越狱到-agent-攻击的演进路线)
3. [T2I 安全：内容安全与概念擦除的攻防博弈](#3-t2i-安全内容安全与概念擦除的攻防博弈)
4. [横切关注点：多模态、推理链与 MCP](#4-横切关注点多模态推理链与-mcp)
5. [前沿趋势：2026 研究热点信号](#5-前沿趋势2026-研究热点信号)
6. [未来研究方向与开放问题](#6-未来研究方向与开放问题)
7. [论文图谱总览](#7-论文图谱总览)

---

## 1. 宏观全局：基础模型时代的安全格局

### 1.1 范式转变：从专用模型到通用基础模型

AI 安全研究正经历一次深刻的范式转变。过去，攻击与防御的目标是具体的、用途单一的模型（分类器、生成器）；而在基础模型（Foundation Model）时代，**单一模型承载了数十亿参数、跨领域的通用能力**，其安全风险也因此成倍放大。

清华大学 2026 年的综述（[2603.24857](https://arxiv.org/abs/2603.24857)）提出了一个关键论断：**数据与模型之间的风险传播是双向的、循环的**。传统安全研究将数据攻击（投毒）和模型攻击（越狱）视为独立问题，但实际上：

```
数据投毒 ──► 模型后门 ──► 成员推理 ──► 训练数据泄露 ──► 新一轮攻击
```

这种闭环风险结构意味着，**孤立地修补某一类漏洞，而不考虑整个生态系统的联动效应，往往是无效的**。

### 1.2 攻防不对称性持续扩大

本项目收录的论文中，**攻击类论文与防御类论文的比例约为 3:2**（T2T 中攻击方法的搜索或构造效率显著高于防御验证效率）。从 GCG、AutoDAN 等自动化越狱工具，到 2026 年涌现的 Claudini（自研究发现 SOTA 级别对抗算法，[2603.24511](https://arxiv.org/abs/2603.24511)），攻击自动化程度大幅提升，而防御侧仍大量依赖人工设计的安全对齐规则。

**核心矛盾**：安全对齐的泛化能力（generalization）远不及攻击的组合创新能力。每一种新的越狱方式的出现，往往只需要 1-2 周的工程工作，而对应的防御方案需要数月的研究验证。

### 1.3 多模态融合引入新攻击面

2023 年以前，T2T 和 T2I 的安全研究几乎是并行独立的两条线。但从 2024 年开始，随着多模态大模型（MLLM）成为主流，两者的攻击面开始交织：

- **视觉输入绕过文本过滤器**（[2603.24079](https://arxiv.org/abs/2603.24079)）：图像中的语义可以激活语言模型的生成能力，而现有的文本安全过滤机制对此盲点无感
- **VLM 红队测试需要联合策略**（[2603.22882](https://arxiv.org/abs/2603.22882)，CVPR 2026）：纯文本红队方法无法覆盖图像+文本联合攻击的组合空间
- **侧信道攻击扩展到本地 VLM**（[2603.25403](https://arxiv.org/abs/2603.25403)）：通过推理时间/内存访问模式，甚至可以推断模型内部处理的敏感内容

---

## 2. T2T 安全：从越狱到 Agent 攻击的演进路线

### 2.1 越狱攻击的四代演进

基于本项目收录的 T2T 论文，可以清晰地看到 LLM 越狱攻击的技术演进路线：

| 代次 | 时间段 | 代表方法 | 技术特征 | 代表论文 |
|------|--------|----------|----------|----------|
| **第一代** | 2022–2023 | 手工 jailbreak | 人工设计角色扮演、假设场景 | DeepInception |
| **第二代** | 2023–2024 | 自动化梯度攻击 | GCG、AutoDAN，基于梯度优化对抗 token | FlipAttack |
| **第三代** | 2024–2025 | 模糊测试 + LLM 代理 | TriageFuzz（token 重要性分级）、Claudini（自动研究） | [2603.23269](https://arxiv.org/abs/2603.23269) |
| **第四代** | 2025–2026 | Agent/CoT/推理链攻击 | 攻击推理步骤而非最终输出，利用 CoT 的中间语义 | SFCoT、PIDP |

**关键洞察**：第四代攻击的出现标志着安全对齐的"防线后移"——传统对齐技术主要保护输出阶段，而推理链（CoT）的出现创造了一个"受保护更弱的内部通道"，使得攻击者可以在模型"思考"阶段注入有害语义，最终输出合规但过程恶意。

### 2.2 提示注入（Prompt Injection）的系统化

提示注入在 2026 年已从"研究现象"演变为"系统化工程问题"：

**演进路径**：

```
单一 LLM 提示注入
    ↓
RAG 系统 PIDP 攻击（注入 + 数据库投毒联合）[2603.25164]
    ↓
MCP（Model Context Protocol）提示注入 [2603.21642, 2603.24203]
    ↓
浏览器端 AI Agent 间接注入 [2603.23791]
```

MCP 的出现尤为值得关注。MCP 作为 AI 辅助开发工具（如 GitHub Copilot、Cursor）的标准协议，其安全问题直接影响软件供应链安全：
- 论文 [2603.21642](https://arxiv.org/abs/2603.21642)（UBC）证明，**AI 辅助开发工具（MCP 架构）对提示注入攻击不具有免疫性**
- 论文 [2603.24203](https://arxiv.org/abs/2603.24203) 提出基于树搜索的 TIP 攻击，可自动生成隐蔽的 MCP 注入载荷

### 2.3 LLM Agent 安全：新兴但系统化不足

2026 年出现了多篇专注于 **LLM Agent 安全形式化**的论文，反映了研究社区认识到 Agent 安全的独特性：

- **T-MAP**（[2603.22341](https://arxiv.org/abs/2603.22341)，KAIST）：对 LLM Agent 执行轨迹（trajectory）进行红队测试，使用进化搜索探索攻击空间
- **A Framework for Formalizing LLM Agent Security**（[2603.19469](https://arxiv.org/abs/2603.19469)，UC Berkeley / Dawn Song）：首次尝试用形式化方法描述 Agent 安全的边界和保证条件

**当前的系统化缺口**：Agent 安全目前仍缺乏统一的威胁模型、评估基准和防御框架，大多数研究是"针对特定 Agent 框架的单点工作"。

**4 月 15 日新增信号**：PlanGuard（[2604.10134](https://arxiv.org/abs/2604.10134)）与 ADAM（[2604.09747](https://arxiv.org/abs/2604.09747)）把 Agent 安全继续往两个方向推进：前者证明真正有效的 indirect prompt injection 防御不是继续过滤输入，而是把“规划-执行一致性”做成运行时 reference check；后者则说明 memory-enabled agent 的真正高危点在于可被主动搜索的私有记忆分布，memory extraction 已从 prompt trick 升级为 entropy-guided adaptive querying。两篇论文共同表明：**Agent 安全正在从“注入防护”扩展到“执行授权 + 长期记忆治理”的系统级问题。**

### 2.4 防御侧：从规则对齐到机制可解释性

防御研究在 2025–2026 年出现了一个重要转向——从"添加规则"到"理解机制"：

| 防御思路 | 代表工作 | 核心贡献 |
|----------|----------|----------|
| 双目标优化对齐 | DOOR（ICML 2025）[2503.03710] | 同时优化帮助性和安全性的对立目标 |
| 推理链安全校准 | SFCoT [2603.15397] | 在 CoT 中间步骤实时检测不安全语义 |
| 安全电路归因 | SafeSeek [2603.23268] | 可解释性工具，定位 LLM 内部"安全电路"位置 |
| 激活水印监控 | Activation Watermark [2603.23171] | 通过激活层水印实现运行时安全监控 |
| 推理漏洞实时监控 | Reasoning Safety Monitor [2603.25412] | 超越内容安全，监控推理过程中的逻辑漏洞 |
| LLM-as-Judge 检测 | Prompt Attack Detection [2603.25176] | 用 LLM 混合模型集成检测提示攻击 |

**趋势**：防御研究正从"黑盒对齐训练"转向"白盒机制分析 + 实时监控"，这与机器学习可解释性（XAI）研究的交叉融合是未来的重要方向。

**4 月 15 日新增信号**：LIRA（[2604.10403](https://arxiv.org/abs/2604.10403)）把安全对齐的控制点前移到 instruction representation 本身，说明未来防御不再只是“让模型拒答”，而是“让模型安全理解指令”；与之相对，Backdoors in RLVR（[2604.09748](https://arxiv.org/abs/2604.09748)）证明 RLVR 奖励回路会把极少量 poison sample 放大成高泛化、低可见损伤的 jailbreak backdoor。二者一攻一防共同说明：**T2T 安全的主战场已经从 prompt 表面迁移到内部表示与优化动力学。**

---

## 3. T2I 安全：内容安全与概念擦除的攻防博弈

### 3.1 T2I 安全研究的独特结构

T2I 安全研究具有一个与 T2T 不同的独特结构：**防御方法大量集中在"知识/概念擦除"（Concept Erasure/Unlearning）这一范式**，而非简单的输出过滤。这反映了 T2I 模型的特殊性——扩散模型的生成能力来自训练时嵌入的"概念表示"，**从源头擦除有害概念比拦截输出更根本**。

概念擦除技术的演进（本项目收录）：

```
ESD（2023）[2303.07345] → Concept Ablation [2303.13516] → UCE [2308.14761]
    ↓
RACE [2405.16341] → Receler [2407.12383] → TRCE [2503.07389]
    ↓
Z-Erase [2603.25074]（单流扩散 Transformer 专用，2026）
    ↓
Concept Pinpoint Eraser [2506.22806]（精准定位概念神经元）
```

**关键挑战**（贯穿各代方法）：
- **遗忘 vs. 保留**的 trade-off：擦除有害概念时不可避免地损伤邻近的无害概念（如擦除"裸体"概念可能影响"解剖学"相关生成）
- **鲁棒性**：擦除后的模型对攻击者的精心构造 prompt 仍然脆弱（RACE 和 Receler 专门解决这一问题）

### 3.2 T2I 攻击方法的系统化

T2I 攻击研究在 2024–2025 年趋向**自动化**和**无查询黑盒化**：

| 攻击范式 | 代表方法 | 技术特征 |
|----------|----------|----------|
| 语义绕过 | SneakyPrompt（2023）[2305.12082] | 强化学习搜索绕过过滤器的替代词 |
| 感知层越狱 | Perception Jailbreak [2408.10848] | 利用人类感知与模型理解的差异 |
| 纯黑盒查询 | DiffZOO [2408.11071] | 零阶优化，无需梯度的黑盒攻击 |
| LLM 辅助攻击 | JailFuzzer [2408.00523] | LLM Agent + 模糊测试自动化 |
| 多模态推理攻击 | Reason2Attack [2503.17987] | 利用 VLM 自身推理能力生成攻击 |
| 动态注意力后门 | Dynamic Attention Backdoor [2504.20518] | 注意力机制层面的后门植入 |
| LLM 语义构造 | Jailbreaking via LLM [2503.01839] | 利用语言模型自动构造语义攻击 |

**值得重点关注的趋势**：从 2024 年起，**多篇 T2I 攻击论文开始利用 LLM 自身来生成攻击提示**。这种"用 AI 攻击 AI"的模式在 2026 年将更为普遍，并与 T2T 的 Agent 攻击研究高度融合。

### 3.3 水印保护：版权与溯源的技术路径

T2I 安全研究中，**水印**是一个相对独立但同样重要的研究方向，覆盖从内容归属到版权保护的多个场景：

- **Stable Signature**（[2303.15435](https://arxiv.org/abs/2303.15435)，Meta FAIR）：在扩散模型的潜空间（latent space）中嵌入水印，实现生成内容的可追溯性
- **SAEUron**（[2501.18052](https://arxiv.org/abs/2501.18052)）：利用稀疏自编码器（SAE）精确定位并操控视觉概念神经元，适用于内容水印和版权保护

**4 月 15 日新增信号**：Closed-Form Concept Erasure via Double Projections（[2604.10032](https://arxiv.org/abs/2604.10032)）把 concept erasure 从需要重训的工程问题重写成“safe projection + left-nullspace constraint”的闭式几何求解，说明 T2I 防御正在进入 training-free、解析可控的新阶段；与此同时，NTIRE 2026 Challenge（[2604.11487](https://arxiv.org/abs/2604.11487)）又把 AIGC 检测的评测中心从 clean classification 推向 robustness-in-the-wild。两篇论文一起表明：**T2I 安全正在同时补齐“方法论创新”和“现实部署评测协议”这两块短板。**

---

## 4. 横切关注点：多模态、推理链与 MCP

### 4.1 多模态安全的三大交汇点

随着 MLLM 成为主流，T2T 和 T2I 安全研究的交汇产生了三类新问题：

**① 跨模态越狱**：图像中的视觉内容可以绕过基于文本的安全过滤。论文 [2603.24079]（CVPR 2026）系统性地分析了 MLLM 理解能力本身带来的生成安全风险——"模型越能理解图像，攻击面就越宽"。

**② VLM 侧信道泄露**：本地运行的 VLM 暴露出推理时间和内存访问模式，攻击者可以通过这些模式推断用户正在生成的内容（[2603.25403](https://arxiv.org/abs/2603.25403)）。

**③ 自主 VLM 红队**：TreeTeaming（[2603.22882](https://arxiv.org/abs/2603.22882)，CVPR 2026）提出了分层策略探索框架，使 VLM 能够自主对自身或其他模型进行红队测试——**这是红队测试自动化的标志性进展**。

### 4.2 推理链（CoT）：安全研究的新主战场

Chain-of-Thought 推理在 2025–2026 年成为 LLM 安全研究的重要新方向，原因是：

1. **推理链显式化了中间步骤**，这些步骤比最终输出更难被安全过滤器覆盖
2. **CoT 的内部语义可以逐步偏移**，从看似合理的推导出发，最终得到有害结论
3. **推理能力增强了攻击能力**：Reason2Attack [2503.17987] 证明，具备推理能力的模型可以自行推导出更有效的攻击策略

SFCoT（[2603.15397](https://arxiv.org/abs/2603.15397)）代表了防御侧的最新应对——**在推理链每一步实时评分并干预**，是"推理安全监控"范式的先驱。

### 4.3 边缘端 LLM：被忽视的攻击面

论文 [2603.23822](https://arxiv.org/abs/2603.23822) 专门研究了**边缘设备上运行的小型 LLM 的安全漏洞**。与云端 LLM 相比，边缘 LLM 的独特弱点：
- 参数量压缩导致安全对齐能力下降
- 本地运行不经过云端内容过滤
- 设备侧攻击（硬件、OS）可直接操作模型参数

这一方向在移动 AI、IoT AI 场景下将持续重要，目前研究还严重不足。

---

## 5. 前沿趋势：2026 研究热点信号

基于 2026 年 3 月提交的论文（本项目收录的最新批次），可以识别出以下**正在形成的研究热点**：

### 🔥 热点一：MCP 与工具调用链安全

**信号强度**: ⭐⭐⭐⭐⭐

两篇独立论文同时在 2026 年 3 月关注 MCP 安全（[2603.21642](https://arxiv.org/abs/2603.21642)、[2603.24203](https://arxiv.org/abs/2603.24203)），加上 Agent 工具调用链攻击（RAG + 提示注入 [2603.25164]），指向同一个趋势：**AI 工具协议（MCP、函数调用、RAG 检索）正在成为新的主要攻击面**。随着 AI 进入生产软件工程流程，此方向将在 2026–2027 年爆发。

### 🔥 热点二：可解释性驱动的防御（Mechanistic Safety）

**信号强度**: ⭐⭐⭐⭐

SafeSeek（[2603.23268](https://arxiv.org/abs/2603.23268)）的安全电路归因、Activation Watermark（[2603.23171](https://arxiv.org/abs/2603.23171)）的激活层监控，以及 SAEUron（[2501.18052](https://arxiv.org/abs/2501.18052)）的稀疏自编码分析，共同指向一个范式：**用机制可解释性工具定位和修复安全漏洞，而非依赖黑盒对齐训练**。这与 Anthropic 在 Superposition 和 Circuit 研究方向高度吻合。

### 🔥 热点三：AI 自主红队（Self-Adversarial Testing）

**信号强度**: ⭐⭐⭐⭐

Claudini（[2603.24511](https://arxiv.org/abs/2603.24511)）通过自研究发现 SOTA 级别对抗算法，TreeTeaming（[2603.22882](https://arxiv.org/abs/2603.22882)）让 VLM 自主对目标模型进行红队，JailFuzzer 用 LLM Agent 自动化 T2I 攻击——**AI 自主红队正从概念转向实用工具**，这将彻底改变安全评估的方式。

### 🔥 热点四：数据泄露风险的精量化

**信号强度**: ⭐⭐⭐

论文 [2603.24917](https://arxiv.org/abs/2603.24917) 专门研究了**语言模型近逐字提取风险的精确估算**，反映了在监管压力下，学界开始从"是否存在泄露"转向"泄露的程度和概率有多大"的精量化评估。随着 AI 版权和隐私法规的收紧（欧盟 AI Act、美国 AI Bill of Rights），此方向将具有重大实际价值。

### 🔥 热点五：单流扩散 Transformer（DiT）的安全挑战

**信号强度**: ⭐⭐⭐

Z-Erase（[2603.25074](https://arxiv.org/abs/2603.25074)）和 DTVI（[2603.22041](https://arxiv.org/abs/2603.22041)）均针对新一代**单流扩散 Transformer**（Flux、SD3.0 的技术路线），而现有大多数概念擦除方法是为经典 U-Net 扩散架构设计的。**架构迁移带来了安全研究的重构需求**，这一方向在 2026 年将持续活跃。

### 🔥 热点六：代理安全治理化（Agentic Security Governance）

**信号强度**: ⭐⭐⭐⭐（2026-03-30 新增）

2603.26221（Clawed and Dangerous）和 2603.25056（System Prompt Attack Surface）同期发表，均指向同一结论：**LLM 代理的安全问题本质上是配置管理和运行时治理问题，而非单纯的模型鲁棒性问题**。这标志着代理安全研究正从"修补漏洞"走向"系统化治理"。

重要发现：能力撤销（Capability Revocation）和跨会话内存完整性在现有文献中几乎是空白，是下一阶段代理安全工程化的关键方向。

### 🔥 热点七：T2I 模型生命周期安全

**信号强度**: ⭐⭐⭐（2026-03-30 新增）

CVPR 2026 双收录的 BPO（[2603.26328](https://arxiv.org/abs/2603.26328)）和 SALMUBench（[2603.26316](https://arxiv.org/abs/2603.26316)）代表 T2I 安全研究的新方向：**从内容过滤走向模型身份验证和知识可控遗忘**。这两个方向与 AI 法规合规（GDPR 被遗忘权、EU AI Act）高度契合，预计将成为 2026–2027 年的研究热点。

### 🔥 热点八：从“行为审查”到“概念擦除”（Abliteration 攻击驱动）

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-07 新增）

随着 `gemma-4-E2B-it-heretic-ara` 等无审查模型的出现，**Abliteration（定向消融/正交化）** 攻击证明了传统 RLHF 的脆弱性：攻击者无需重新训练，仅通过正交投影抹除模型权重中的“拒绝向量”，几秒钟内即可彻底破除安全护栏。这引发了对齐范式的底层重构：
安全防线必须从**行为审查（教模型不说）**转向深层的**概念擦除（教模型真不懂）**。在 OpenAI 的 MLE（AI训练AI）愿景下，防止具有高级代码权限的 Agent 实施自我解除武装（Self-Uncensoring），已成为最为紧迫的生存级挑战。

---

## 6. 未来研究方向与开放问题

**① Agent 安全形式化与统一基准**

当前 LLM Agent 安全研究严重碎片化，缺乏：
- 统一的 Agent 威胁模型（PISmith、T-MAP、Cognitive Firewall 各自提出了不同框架）
- 跨框架的评估基准（类似 T2T 的 JailbreakBench [2404.01318] 那样的统一评测平台）
- 多步骤 Agent 任务中的安全-有用性权衡的量化方法

**② CoT 推理安全的系统化**

目前仅 SFCoT 一篇工作专注于推理链安全监控，未来需要：
- 大规模、多样化的 CoT 安全数据集（现有 benchmark 主要关注最终输出）
- 推理步骤安全评分的轻量级实现（避免推理开销过大）
- 对"逐步偏移"攻击的统一分类法

**③ 边缘端 LLM 安全专项研究**

当前几乎空白，需要：
- 压缩/量化对安全对齐能力的定量影响研究
- 硬件侧信道攻击对边缘 LLM 的威胁评估（[2603.25403] 是先驱）
- 针对资源受限设备的轻量级安全机制

### 6.2 中期（3–5 年）：系统性挑战

**④ 机制可解释性驱动的可验证安全**

目前可解释性研究（Circuit Analysis、SAE）与安全对齐之间的连接还很薄弱。中期目标：
- 能够**形式化验证**某个模型"不会生成 X 类内容"的机制级保证
- 基于 SAE/激活分析的自动化漏洞发现和修复流水线
- 安全相关神经元的稳定性研究：对齐后的安全表示在微调中是否保持稳定（Internal Safety Collapse [2603.23509] 已发现此问题严重）

**⑤ 多模态统一安全框架**

随着 GPT-4o、Gemini 等跨模态模型成为主流，需要：
- 覆盖文本、图像、视频、音频多模态的统一安全评估框架
- 跨模态攻击的迁移性研究（T2T 攻击如何迁移到 T2I/T2V）
- 实时多模态内容安全监控的工程化实现

**⑥ 生成内容溯源与版权归属体系**

数据提取攻击（[2603.24917](https://arxiv.org/abs/2603.24917)）和水印保护（Stable Signature）的研究指向了一个更大的问题：**如何建立大模型生成内容的可溯源、可归属、可验证的版权体系**。这既是技术问题，也是法律框架问题。

### 6.3 长期（5+ 年）：范式级挑战

**⑦ 自主 AI 系统的安全对齐问题**

随着 AI Agent 从工具演变为具有持久记忆、自主规划能力的系统，当前的"提示级安全对齐"将根本性地不足。需要探索：
- 目标级别（goal-level）的安全约束，而非行为级别（behavior-level）
- 多 Agent 协作中的安全协议（一个 Agent 是否可以信任另一个 Agent 的安全声明）
- AI 系统的安全属性的持久性（fine-tuning 后安全性是否退化 —— Internal Safety Collapse 已证明这是严重问题）

**⑧ 攻防博弈的博弈论建模**

目前安全研究大多是"攻击-防御"的顺序响应模式，缺乏对**持续博弈过程**的系统建模：
- 攻防双方的均衡状态是否存在？
- 什么条件下防御方能获得持久优势？
- 开源模型生态中的集体安全行动问题（类似公共品博弈）

---

## 7. 论文图谱总览

### T2T 论文分布（80 篇）

```
时间线：2022 ──────────────────────────────────────► 2026
         |                                              |
攻击类：  DeepInception FlipAttack  InfoFlood  T-MAP  Claudini
                       (auto)       TreeTeaming  TriageFuzz
                                    PIDP-Attack  VLM-SideChannel
                                    SysPrompt-Atk  H-Node-Atk
                                    Trojan-Speak（2603.29038）
                                    Unreal Thinking (CoT劫持后门, 2604.09235)
                                    FreakOut-LLM (情绪越狱, 2604.04992)
                                    RL Generalization Limits (复合越狱, 2604.02652)
                                    CRaFT (电路级特征选择, 2604.01604)
                                    Art of Misalignment (ORPO武器, 2604.07754)
                                    Harmful Unified Mechanism (<1%权重, 2604.09544)
                                    CRA Jailbreak (2604.07835)
                                    Defense Trilemma (形式化三难, 2604.06436)
                                    GCD Dual-Anchor (2604.05179)
                                    HyPE/HyPS (双曲几何安全, ICLR'26, 2604.06285)
                                    ThoughtStealer (推理后门, 2604.00770)
                                    PISmith, Paper Summary Attack
                                    SafeWeights (2604.08297)
                                    Backdoors in RLVR (奖励回路后门, 2604.09748)
                       
防御类：  (传统对齐)    DOOR        SFCoT      SafeSeek  ReasonMonitor
                       (ICML2025)   CognFirewall Activation-WM
                                    SaftyProbes  H-Node-Defense
                                    GUARD-SLM（2603.28817）
                                    Secure AI Agents（2603.30016）
                                    SelfGrader (token级检测, 2604.01473)
                                    LIRA (指令表示对齐, 2604.10403)
                                    AutoDefense, KG-DF, DOOR
                       
Benchmark:            PandaGuard   SecureBreak  InternalCollapse
                                   AI-Survey    Clawed&Dangerous
                                   LaaJ-SoK（2603.29403）
                                   ClawSafety (120场景, 2604.01438)
                                   From LLMs to MLLMs 综述 (2506.15170)
                       
Agent 安全:                         PISmith     T-MAP
                                               LLM-Agent-Sec
                                               MCP-Inject × 2
                                               Your Agent Is Mine (API路由投毒, 2604.08407)
```

### T2I 论文分布（62 篇）

```
时间线：2019 ──────────────────────────────────────► 2026
         |                                              |
概念擦除：              ESD  Forget-Me-Not  UCE  RACE  Receler
                       CA   SEGA  SLD       TRCE  CPE  Z-Erase
                                            SALMUBench(遗忘基准)
                                            EGLOCE (双能量引导, 2604.09405)
                                            Linear Subspace Removal (2604.05296)
                                            Closed-Form DP (双投影闭式擦除, 2604.10032)
                                            Concept Pinpoint Eraser [2506.22806]
                       
越狱攻击：              SneakyPrompt  MMA-Diff  FLIRT  JailFuzzer
                       Perception-JB  DiffZOO  FRAP  Janus
                       Reason2Attack  GenBreak  DTVI
                       Hidden Ads（2603.27522，VLM行为触发后门）
                       Mosaic (多视图VLM越狱, +37pp ASR, 2604.09253)
                       
水印攻击：              SHIFT (无训练轨迹偏转, 2603.29742)
                       AR Watermark Robustness (对抗鲁棒性, 2604.11720)
                       
Benchmark:             GuardT2I  JailbreakBench  MIMMU  PromptSAN
                       BPO-Verify(模型验证 CVPR'26, 2603.26328)
                       SALMUBench (遗忘基准, 2603.26316)
                       ImageProtector (VPI→隐私 ACL'26, 2604.09024)
                       NTIRE 2026 (鲁棒AIGC检测, 2604.11487)
                       
水印保护：              Stable-Sig  ModularLoRA  SAEUron
                       Concept-Corrector  SPEED
                       
前处理防御：            LatentGuard  SAFREE  Safeguider
                       SafeGen  PromptGuard  MacPrompt
                       FlowGuard (线性潜空间NSFW检测, F1+30%, 2604.07879)
```

### Agentic Search 论文分布（20 篇）

```
时间线：2025 ──────────────────────────────────────► 2026
         |                                              |
攻击类:  Clawed&Dangerous  SysPrompt-Atk  Near-Miss
         Your Agent Is Mine (API路由投毒, 2604.08407)
         BadSkill (Model-in-Skill后门, 99.5% ASR, 2604.09378)
         SIF 语义意图碎片化 (组合攻击, 71%违规, AAAI'26, 2604.08608)
         ADAM (记忆抽取, 2604.09747)
         PRAC Attack (注意力偏好重定向, 2604.08005)
         GUI Distraction (GUI干扰, 2604.07831)

防御类:  TRUSTDESC (工具投毒防护, 2604.07536)
         TrajGuard (轨迹检测, ACL'26, 95%, 2604.07727)
         PlanGuard (规划一致性验证, 2604.10134)

Benchmark/评测:
         PIArena (统一注入评测, ACL'26, 2604.08499)
         ACIArena (级联注入, ACL'26, 1356 cases, 2604.07775)
         ClawSafety (120对抗场景, 2604.01438)
         Plan-RewardBench (2604.08178)
```

---

*本文档由 `paper-research` skill 基于项目论文库自动生成，并经人工审核和补充。*
*最近更新：2026-04-15（v2.1 增量更新），累计论文数 **162**（T2T: **80** 篇，T2I: **62** 篇，Agentic Search: **20** 篇）。*
*本次 v2.1 更新：新增 6 篇论文，T2T 补入 Backdoors in RLVR 与 LIRA，T2I 补入 Closed-Form DP 与 NTIRE 2026，Agentic Search 补入 PlanGuard 与 ADAM，并同步刷新三模态趋势段落与图谱统计。*
*相关 Survey 详见 [`t2t-survey.md`](./t2t-survey.md)、[`t2i-survey.md`](./t2i-survey.md) 和 [`agentic-search-survey.md`](./agentic-search-survey.md）。