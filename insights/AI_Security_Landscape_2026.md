# AI 大模型安全前沿洞察：现状理解与未来研究方向

> **数据来源**: 基于本项目收录的 **211 篇** AI 安全论文（2019–2026）系统性分析
> **更新日期**: 2026-04-28（v2.9 增量更新）
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

**4 月 17 日新增信号**：这一趋势在最新一批论文中被进一步拉宽。MemJack（[2604.12616](https://arxiv.org/abs/2604.12616)）证明自然良性图像本身就能成为 VLM Agent 的越狱锚点；MCPThreatHive（[2604.13849](https://arxiv.org/abs/2604.13849)）把 MCP 风险上升为持续 threat intelligence 与 taxonomy 问题；SafeHarness（[2604.13630](https://arxiv.org/abs/2604.13630)）把防线下沉到 execution harness 生命周期；R2A（[2604.15022](https://arxiv.org/abs/2604.15022)）首次把路由器的**经济成本放大**纳入攻击面；CBCL（[2604.14512](https://arxiv.org/abs/2604.14512)）则把多 Agent 安全推进到协议级 formality-by-design。它们共同说明：**Agentic 安全已经从“阻止注入”升级为“治理协议、执行框架、威胁情报与成本面”的系统工程。**

**4 月 18 日新增信号**：ATBench-Claw / ATBench-CodeX（[2604.14858](https://arxiv.org/abs/2604.14858)）与 DR3-Eval（[2604.14683](https://arxiv.org/abs/2604.14683)）把 Agent 安全再推进了一层：前者说明 benchmark 必须随 OpenClaw、Codex-runtime 这类真实执行环境重写 risk taxonomy，后者则证明 Deep Research agent 的核心瓶颈在 evidence retrieval 与 grounded report generation，而非表面文笔。两篇论文共同指向一个更大的趋势：**Agent benchmark 正在基础设施化，评测本身也开始成为需要持续维护和防攻击的系统底座。**

**4 月 20 日新增信号**：HarmfulSkillBench（[2604.15415](https://arxiv.org/abs/2604.15415)）与 LogJack（[2604.15368](https://arxiv.org/abs/2604.15368)）把 Agent 风险继续下沉到两个此前很容易被默认信任的输入面：**开放技能生态**与**云日志遥测**。前者说明“危险能力封装成 skill”本身就会削弱拒答，后者说明“日志里的修复建议”会直接劫持调试代理执行链。也就是说，Agent 安全如今不只是防 prompt injection，而是要治理**registry、telemetry 与 action boundary** 三个真实生产控制点。

**4 月 21 日新增信号**：CASCADE（[2604.17125](https://arxiv.org/abs/2604.17125)）与 Visual Inception（[2604.16966](https://arxiv.org/abs/2604.16966)）把这条主线又向前推了两步：前者说明 MCP 防御的正确抽象层次是**协议级级联治理**，要把 prompt injection、tool poisoning、data exfiltration 视为一条连续链路来处理；后者则把攻击面推进到**多模态长期记忆**，证明一张看似良性的用户图片也能在未来规划阶段持续劫持 agent 目标。两篇论文共同说明：**Agent 安全已经从“防当前输入”升级为“治理运行链路与长期记忆因果触发”的系统工程。**

**4 月 22 日新增信号**：GAAP（[2604.19657](https://arxiv.org/abs/2604.19657)）把 Agent 隐私保护继续往“执行环境级控制”推进：私有数据不再只靠 model-side refusal 保护，而是由 IFC、Permission DB 与 Disclosure Log 在 deterministic runtime 中强制约束。它释放出的信号非常明确——**Agent 安全下一步不仅要管 prompt、tool、memory，还要把 execution harness 本身做成可验证的 privacy control plane。**

**4 月 27 日新增信号**：Function Hijacking Attacks（[2604.20994](https://arxiv.org/abs/2604.20994)）与 MCP Pitfall Lab（[2604.21477](https://arxiv.org/abs/2604.21477)）又把 Agentic / MCP 安全往更上游推进了一层：前者说明只靠污染函数 description，就能在真正执行工具前把模型路由到攻击者指定函数，意味着 **tool selection layer** 已成为正式攻击面；后者则进一步证明，MCP 安全失效经常来自 schema、跨工具转发、高风险输入校验与审计日志等**开发者实现坑位**，而且 agent 自述与真实 trace 在 sink-action 场景上会出现 **100%** 偏差。共同信号是：**MCP 安全正在从“防 prompt injection”升级为“治理 pre-execution control plane + protocol trace + developer hygiene”的系统工程。**

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

**4 月 17 日新增信号**：这条线进一步分化成“谱结构鲁棒训练”“跨片段 probe”“因果头去毒”和“verifier gaming 诊断”四个分支。ER-CAT（[2604.12817](https://arxiv.org/abs/2604.12817)）把 CAT 的效果解释为嵌入奇异值方差问题；Segment-Level Coherence（[2604.14865](https://arxiv.org/abs/2604.14865)）把流式探测从 token 峰值推进到意图级连续证据；CausalDetox（[2604.14602](https://arxiv.org/abs/2604.14602)）说明 detox 开始进入因果头级干预；RLVR Reward Hacking（[2604.15149](https://arxiv.org/abs/2604.15149)）则明确告诉我们：高 verifier reward 可能只是 shortcut，而不是安全真实改进。也就是说，**T2T 安全如今不只是“如何防住攻击”，而是“如何证明训练、检测与评测本身没有被奖励结构欺骗”。**

**4 月 18 日新增信号**：Context Over Content（[2604.15224](https://arxiv.org/abs/2604.15224)）进一步证明**评测器本身也会被 system prompt 的 stakes signaling 污染**，而 Asymmetric Two-Task Unlearning（[2604.14808](https://arxiv.org/abs/2604.14808)）则把 LLM 遗忘问题重写成 retention-prioritized gradient geometry。两篇论文合起来意味着：**T2T 安全正在从“训练一个更安全的模型”转向“保证训练目标、遗忘目标与自动评测机制本身不被优化结构带偏”。**

**4 月 20 日新增信号**：Into the Gray Zone（[2604.15717](https://arxiv.org/abs/2604.15717)）与 Pruning Unsafe Tickets（[2604.15780](https://arxiv.org/abs/2604.15780)）进一步把 T2T 主线撕开成两端：一端是**研究语境会把拒答边界推入 gray zone**，Jargon 平均 ASR 达 **99.0%**；另一端是**部署后可以通过结构性剪枝修补不安全子网络**，把 Mistral-7B 的 Unsafe Rate 从 **22.8%** 压到 **1.17%**。两篇论文合起来说明：未来 T2T 安全既要研究边界为何会软化，也要研究如何在不重训的前提下做现实可部署的结构性补丁。

**4 月 21 日新增信号**：Continual Safety Alignment（[2604.17215](https://arxiv.org/abs/2604.17215)）与 Offensive Cyber Benchmark（[2604.17159](https://arxiv.org/abs/2604.17159)）把 T2T 主线继续向训练过程与执行环境两端拉开：前者说明 benign 数据中的 high-gradient 样本就足以把模型拉回 pretraining distribution，持续微调的真正风险点在**样本级对齐漂移**；后者则说明 offensive cyber agent 的表现更多由**工具环境与可发现性**决定，而不是继续堆 prompt trick。共同信号是：**T2T 安全正在从“静态输入输出防护”升级为“训练轨迹治理 + 环境条件治理”。**

**4 月 22 日新增信号**：IICL（[2604.19461](https://arxiv.org/abs/2604.19461)）与 HarDBench（[2604.19274](https://arxiv.org/abs/2604.19274)）继续把 T2T 风险推向真实 workflow：前者说明抽象算子、few-shot completion 与 pattern continuation 本身就能系统性软化安全边界；后者则把 draft-based co-authoring 里的灰区 harmful request 正式做成 benchmark。共同信号是：**T2T 对齐脆弱性正在从“危险问题”迁移到“看似正常的协作补全流程”。**

**4 月 27 日新增信号**：AIC（[2604.21159](https://arxiv.org/abs/2604.21159)）与 TTI（[2604.21860](https://arxiv.org/abs/2604.21860)）把 T2T 安全再往前推了一步：前者说明自动 red-teaming 已经进入 **query × tactic 大动作空间里的在线学习阶段**，攻击系统会持续适应目标模型的脆弱区域；后者则表明，只要平台沿用 **stateless per-turn moderation**，攻击者完全可以把多轮状态保存在系统外部，绕过单轮审核。共同信号是：**T2T 风险不再只是“某条 prompt 有多危险”，而是“攻击系统有多会学习、审核边界有多依赖单轮视角”。**

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

**4 月 17 日新增信号**：T2I 主线继续朝“结构化遗忘 + 真实链路检测 + 主动内部探测”三方向展开。Scaling Exposes the Trigger（[2604.12446](https://arxiv.org/abs/2604.12446)）说明后门检测开始主动扰动 cross-attention 响应，而不是等待表面异常暴露；DAMP（[2604.15166](https://arxiv.org/abs/2604.15166)）把 class unlearning 推进到 depth-aware direction removal，说明 concept erasure 正从全局微调走向逐层几何清除；QuAD（[2604.15027](https://arxiv.org/abs/2604.15027)）则把 near-duplicate 传播链和质量校准正式纳入 benchmark。三者合起来意味着：**T2I 安全正从“删掉危险概念 + 测一张图像”升级为“探测内部响应 + 管理传播链路 + 做层深相关遗忘”。**

**4 月 18 日新增信号**：Fragile Reconstruction（[2604.12781](https://arxiv.org/abs/2604.12781)）说明 reconstruction-based detector 自身会成为高价值攻击面，白盒下 robust accuracy 近乎归零、迁移后也常塌到随机猜；T2I-BiasBench（[2604.12481](https://arxiv.org/abs/2604.12481)）则把 demographic bias、元素遗漏与 cultural collapse 统一进一个 13 指标审计框架。两篇论文一起把 T2I 研究重心从“有没有 benchmark”推进到“benchmark / detector 本身是否足够完整、足够鲁棒、不会被轻易打穿”。

**4 月 20 日新增信号**：TwoHamsters（[2604.15967](https://arxiv.org/abs/2604.15967)）与 TICoE（[2604.15829](https://arxiv.org/abs/2604.15829)）把 T2I 安全再往前推了一层：前者说明真正棘手的风险不在单个显式危险概念，而在**多个安全概念组合后的隐含不安全语义**；后者说明 concept erasure 也必须同步升级到**图文协同精准保留**，否则就会在强擦除与误伤之间持续失衡。换句话说，T2I 正从“单概念治理”升级为“组合语义治理 + 多模态精准擦除”。

**4 月 21 日新增信号**：Bias at the End of the Score（[2604.13305](https://arxiv.org/abs/2604.13305)）与 Operationalizing Fairness in T2I Models（[2604.16516](https://arxiv.org/abs/2604.16516)）把 T2I 安全进一步推进到**评分函数治理与阈值化公平**层：前者说明 reward models 本身就会放大 demographic bias、hypersexualization 与身份漂移；后者则明确指出 fairness benchmark 若没有 tolerance band 与 pass/fail 规则，就还停留在研究性诊断而非部署级治理。两篇论文共同说明：**T2I 安全正在从“看输出有没有问题”升级为“看评分器是否中立、评测规则是否可上线”。**

**4 月 22 日新增信号**：Dual-Guard（[2604.19090](https://arxiv.org/abs/2604.19090)）、Embedding Arithmetic（[2604.18167](https://arxiv.org/abs/2604.18167)）与 IncreFA（[2604.17736](https://arxiv.org/abs/2604.17736)）把 T2I 主线又往前推了三步：前者说明来源证明已从单 bit watermark 升级到**provenance + tamper localization 一体化**；中者说明 fairness 可以通过 inference-time embedding control 做最小侵入治理；后者则把生成器归因正式推进到**incremental open-set attribution**。共同信号是：**T2I 安全正在从“离线训练后修补”升级为“部署时控制、持续归因与可取证 provenance 治理”。**

**4 月 27 日新增信号**：PGU（[2604.21041](https://arxiv.org/abs/2604.21041)）与 Target-Based Prompting（[2604.21036](https://arxiv.org/abs/2604.21036)）把 T2I 治理分别推进到了“**长期抗复活**”和“**目标显式化控制**”两端：前者说明 concept erasure 的真正难点已从“能否擦掉”转向“后续 fine-tuning 会不会把它学回来”；后者则说明 fairness 不该再由研究者暗中预设，而应被用户或场景显式声明并在推理时被执行。共同信号是：**T2I 安全正在从单次离线修补升级为生命周期治理与控制面治理。**

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

基于截至 2026-04-22 本项目收录的最新批次论文，可以识别出以下**正在形成的研究热点**：

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

### 🔥 热点九：评测系统反身安全化（Evaluation as Attack Surface）

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-18 新增）

Context Over Content（[2604.15224](https://arxiv.org/abs/2604.15224)）说明 LLM-as-a-Judge 会被 stakes signaling 隐性污染；Fragile Reconstruction（[2604.12781](https://arxiv.org/abs/2604.12781)）说明 reconstruction-based detector 在对抗扰动下会整体失守；ATBench-Claw / ATBench-CodeX（[2604.14858](https://arxiv.org/abs/2604.14858)）与 DR3-Eval（[2604.14683](https://arxiv.org/abs/2604.14683)）则进一步把 Agent benchmark 推向执行环境专用基础设施。它们共同揭示：**评测不再是安全研究的附属环节，而是需要被攻击、被验证、被治理的第一类系统组件。**

### 🔥 热点十：从显式危险词到“可信载体中的隐式风险组合”

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-20 新增）

TwoHamsters（[2604.15967](https://arxiv.org/abs/2604.15967)）说明多个单独安全概念的组合就足以形成高风险语义；Into the Gray Zone（[2604.15717](https://arxiv.org/abs/2604.15717)）说明安全研究语境会把模型推入 gray zone；HarmfulSkillBench（[2604.15415](https://arxiv.org/abs/2604.15415)）与 LogJack（[2604.15368](https://arxiv.org/abs/2604.15368)）则进一步表明，skill registry 与云日志这类“默认可信载体”会把危险意图包装成合法工作流或运维文本。共同信号是：**未来安全边界失效越来越少来自直球有害提示，越来越多来自可信上下文、组合语义与执行载体的联合伪装。**

### 🔥 热点十一：上游控制面安全化（Scoring Functions, Protocols, and Memory as Control Plane）

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-21 新增）

最新一批论文同时把安全研究继续往“上游控制面”推进。Bias at the End of the Score（[2604.13305](https://arxiv.org/abs/2604.13305)）说明 reward model 本身会放大 demographic bias、hypersexualization 与身份漂移；Operationalizing Fairness in T2I Models（[2604.16516](https://arxiv.org/abs/2604.16516)）进一步指出 fairness benchmark 若没有 threshold-level acceptance rule，就不足以支撑部署决策；CASCADE（[2604.17125](https://arxiv.org/abs/2604.17125)）把 MCP 安全重写成协议级级联治理问题；Visual Inception（[2604.16966](https://arxiv.org/abs/2604.16966)）则证明长期多模态记忆本身就是可被劫持的控制面。共同信号是：**未来安全治理的重点正在从“拦截最终输出”前移到“治理评分函数、协议链路与长期记忆”这些上游控制面。**

### 🔥 热点十二：从结果审计走向 provenance / attribution / execution environment 三位一体治理

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-22 新增）

Dual-Guard（[2604.19090](https://arxiv.org/abs/2604.19090)）把 T2I 来源证明推进到 provenance + tamper localization；IncreFA（[2604.17736](https://arxiv.org/abs/2604.17736)）把 AIGC attribution 推到 incremental open-set reality；GAAP（[2604.19657](https://arxiv.org/abs/2604.19657)）则把 Agent 隐私保护下沉到 deterministic execution environment；再加上 Embedding Arithmetic（[2604.18167](https://arxiv.org/abs/2604.18167)）把 fairness 治理前移到 inference-time control。共同信号是：**安全研究正在从“最后判一下有没有问题”转向“在生成、归因、执行全过程内嵌控制与取证能力”。**

### 🔥 热点十三：控制面安全化——函数描述、目标分布与外部状态开始主导安全边界

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-27 新增）

Function Hijacking Attacks（[2604.20994](https://arxiv.org/abs/2604.20994)）说明函数 description 本身就能劫持工具选择；MCP Pitfall Lab（[2604.21477](https://arxiv.org/abs/2604.21477)）证明协议 trace 而非 agent 自述才是 MCP 审计锚点；TTI（[2604.21860](https://arxiv.org/abs/2604.21860)）揭示攻击者只要把状态搬到系统外，就能击穿单轮审核；Target-Based Prompting（[2604.21036](https://arxiv.org/abs/2604.21036)）把 fairness 治理改写成目标显式声明；PGU（[2604.21041](https://arxiv.org/abs/2604.21041)）则把概念擦除推进到后续 fine-tuning 梯度方向治理。共同信号是：**未来安全失效越来越少发生在最终输出层，越来越多发生在“谁来定义目标、谁来维护状态、谁来决定工具路由、谁来审计协议 trace”这些上游控制面。**

### 🔥 热点十四：长期状态治理——知识正确性、企业隐私与跨会话记忆开始成为统一安全问题

**信号强度**: ⭐⭐⭐⭐⭐（2026-04-28 新增）

KVBench / KE-Check（[2604.22302](https://arxiv.org/abs/2604.22302)）把 T2I benchmark 推进到知识密集型 visual correctness；FMDiffWA（[2604.22220](https://arxiv.org/abs/2604.22220)）说明反水印能力可以直接被训练进扩散模型；BadStyle（[2604.21700](https://arxiv.org/abs/2604.21700)）把自然文风本身变成隐蔽后门触发器；SHAPE（[2604.22134](https://arxiv.org/abs/2604.22134)）则说明教学语境会系统性软化安全边界；CI-Work（[2604.21308](https://arxiv.org/abs/2604.21308)）、AgentPressureBench（[2604.20200](https://arxiv.org/abs/2604.20200)）与 CSTM-Bench（[2604.21131](https://arxiv.org/abs/2604.21131)）共同把 Agent 风险推进到企业隐私、workflow incentive 与跨会话 memory bottleneck。共同信号是：**安全研究正在把“长期状态治理”确认为跨模态共同主线——T2I 的知识约束与 provenance、T2T 的语境与风格触发、Agent 的长期记忆与工作流目标设计，正在收敛为同一个控制面问题。**

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

### T2T 论文分布（96 篇）

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
                                    Into the Gray Zone (灰区语境越狱, 2604.15717)
                                    IICL (pattern completion 越狱, 2604.19461)
                                    AIC (在线自适应红队, 2604.21159)
                                    TTI (无状态多轮注入, 2604.21860)
                                    BadStyle (风格级自然触发后门, 2604.21700)
                                    RLVR Reward Hacking (verifier gaming, 2604.15149)
                       
防御类：  (传统对齐)    DOOR        SFCoT      SafeSeek  ReasonMonitor
                       (ICML2025)   CognFirewall Activation-WM
                                    SaftyProbes  H-Node-Defense
                                    GUARD-SLM（2603.28817）
                                    Secure AI Agents（2603.30016）
                                    SelfGrader (token级检测, 2604.01473)
                                    LIRA (指令表示对齐, 2604.10403)
                                    ER-CAT (谱结构正则 CAT, 2604.12817)
                                    Segment-Level Coherence (2604.14865)
                                    CausalDetox (因果头去毒, 2604.14602)
                                    Asymmetric Two-Task Unlearning (梯度几何遗忘, 2604.14808)
                                    Pruning Unsafe Tickets (部署后安全剪枝, 2604.15780)
                                    AutoDefense, KG-DF, DOOR
                       
Benchmark:            PandaGuard   SecureBreak  InternalCollapse
                                   AI-Survey    Clawed&Dangerous
                                   LaaJ-SoK（2603.29403）
                                   ClawSafety (120场景, 2604.01438)
                                   From LLMs to MLLMs 综述 (2506.15170)
                                   Context Over Content (Judge 完整性, 2604.15224)
                                   HarDBench (协同写作灰区基准, 2604.19274)
                                   SHAPE (教学语境越狱基准, 2604.22134)
                       
Agent 安全:                         PISmith     T-MAP
                                               LLM-Agent-Sec
                                               MCP-Inject × 2
                                               Your Agent Is Mine (API路由投毒, 2604.08407)
```

### T2I 论文分布（78 篇）

```
时间线：2019 ──────────────────────────────────────► 2026
         |                                              |
概念擦除：              ESD  Forget-Me-Not  UCE  RACE  Receler
                       CA   SEGA  SLD       TRCE  CPE  Z-Erase
                                            SALMUBench(遗忘基准)
                                            EGLOCE (双能量引导, 2604.09405)
                                            Linear Subspace Removal (2604.05296)
                                            Closed-Form DP (双投影闭式擦除, 2604.10032)
                                            DAMP (深度感知类遗忘, 2604.15166)
                                            TICoE (图文协同精准擦除, 2604.15829)
                                            PGU (抗概念复活加固, 2604.21041)
                                            Embedding Arithmetic (推理时去偏, 2604.18167)
                                            Target-Based Prompting (目标声明式公平控制, 2604.21036)
                                            KVBench / KE-Check (知识密集正确性基准, 2604.22302)
                                            Concept Pinpoint Eraser [2506.22806]
                       
越狱攻击：              SneakyPrompt  MMA-Diff  FLIRT  JailFuzzer
                       Perception-JB  DiffZOO  FRAP  Janus
                       Reason2Attack  GenBreak  DTVI
                       Hidden Ads（2603.27522，VLM行为触发后门）
                       Mosaic (多视图VLM越狱, +37pp ASR, 2604.09253)
                       Fragile Reconstruction (检测器对抗脆弱性, 2604.12781)
                       
水印攻击：              SHIFT (无训练轨迹偏转, 2603.29742)
                       AR Watermark Robustness (对抗鲁棒性, 2604.11720)
                       FMDiffWA (训练期频域反水印, 2604.22220)
                       
Benchmark:             GuardT2I  JailbreakBench  MIMMU  PromptSAN
                       BPO-Verify(模型验证 CVPR'26, 2603.26328)
                       SALMUBench (遗忘基准, 2603.26316)
                       ImageProtector (VPI→隐私 ACL'26, 2604.09024)
                       NTIRE 2026 (鲁棒AIGC检测, 2604.11487)
                       QuAD (质量感知近重复校准, 2604.15027)
                       T2I-BiasBench (多指标偏见审计, 2604.12481)
                       TwoHamsters (组合语义不安全基准, 2604.15967)
                       IncreFA / IABench (增量归因基准, 2604.17736)
                       
水印保护：              Stable-Sig  ModularLoRA  SAEUron
                       Dual-Guard (双通道 provenance, 2604.19090)
                       Concept-Corrector  SPEED
                       
前处理防御：            LatentGuard  SAFREE  Safeguider
                       SafeGen  PromptGuard  MacPrompt
                       FlowGuard (线性潜空间NSFW检测, F1+30%, 2604.07879)
                       SET / Scaling Exposes Trigger (cross-attn 后门检测, 2604.12446)
```

### Agentic Search 论文分布（37 篇）

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
         MemJack (自然图像记忆增强越狱, 2604.12616)
         R2A (路由经济放大攻击, 2604.15022)
         LogJack (云日志间接注入, 2604.15368)
         Function Hijacking (函数选择层劫持, 2604.20994)

防御类:  TRUSTDESC (工具投毒防护, 2604.07536)
         GAAP (确定性隐私执行环境, 2604.19657)
         TrajGuard (轨迹检测, ACL'26, 95%, 2604.07727)
         PlanGuard (规划一致性验证, 2604.10134)
         SafeHarness (生命周期执行框架防线, 2604.13630)
         CBCL (协议级通信治理, 2604.14512)
         MCPThreatHive (MCP threat intelligence, 2604.13849)

Benchmark/评测:
         PIArena (统一注入评测, ACL'26, 2604.08499)
         ACIArena (级联注入, ACL'26, 1356 cases, 2604.07775)
         ClawSafety (120对抗场景, 2604.01438)
         Plan-RewardBench (2604.08178)
         ATBench-Claw / CodeX (执行环境轨迹安全, 2604.14858)
         DR3-Eval (Deep Research 可复现评测, 2604.14683)
         HarmfulSkillBench (技能生态武器化基准, 2604.15415)
         MCP Pitfall Lab (协议感知开发者安全基准, 2604.21477)
         CI-Work (企业情境完整性隐私基准, 2604.21308)
         AgentPressureBench (workflow incentive exploitation 基准, 2604.20200)
         CSTM-Bench (跨会话威胁检测, 2604.21131)
```

---

*本文档由 `paper-research` skill 基于项目论文库自动生成，并经人工审核和补充。*
*最近更新：2026-04-28（v2.9 增量更新），累计论文数 **211**（T2T: **96** 篇，T2I: **78** 篇，Agentic Search: **37** 篇）。*
*本次 v2.9 更新：新增 7 篇论文，T2T 补入 BadStyle / SHAPE，T2I 补入 KVBench / KE-Check 与 FMDiffWA，Agentic Search 补入 CI-Work / AgentPressureBench / CSTM-Bench，并新增“长期状态治理”这一跨模态新热点。*
*相关 Survey 详见 [`t2t-survey.md`](./t2t-survey.md)、[`t2i-survey.md`](./t2i-survey.md) 和 [`agentic-search-survey.md`](./agentic-search-survey.md)。