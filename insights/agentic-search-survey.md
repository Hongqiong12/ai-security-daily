# Agentic Search Model 安全与能力研究 Survey

> **版本**: v1.1（增量更新：MemJack / MCPThreatHive / SafeHarness / R2A / CBCL）
> **更新日期**: 2026-04-17
> **覆盖论文数**: 25 篇  
> **维护方式**: 每次新增论文后增量追加；每月 1 日执行深度重构

---

## 1. 领域定义与范围

**Agentic Search Model** 是指具备自主规划（Plan）、动态检索（Search）与综合生成（Generate）能力的大模型系统。与传统的一次性 RAG 管道不同，Agentic Search 系统会在收到用户问题后：

1. **规划（Plan）**：将复杂问题分解为多个子查询或行动步骤
2. **检索（Search）**：通过搜索引擎、知识库或工具 API 迭代获取信息
3. **生成（Generate）**：综合检索结果，生成带有引用溯源的最终答案

### 1.1 典型代表系统

| 类型 | 代表产品 / 框架 | 核心特点 |
|------|----------------|----------|
| **商业产品** | Perplexity AI、SearchGPT（OpenAI）、Gemini Deep Research（Google）、Grok Search（xAI）、Kimi Search（月之暗面）、天工 AI | 面向终端用户，具备实时 web 检索 |
| **学术框架** | ReAct、Self-RAG、WebGPT、Search-o1、DeepSearch、IRCoT | 侧重推理与检索的协同机制 |
| **企业级框架** | LlamaIndex Agentic RAG、LangChain Agents | 工具链集成与工作流编排 |

### 1.2 与传统 RAG 的核心区别

| 维度 | 传统 RAG | Agentic Search |
|------|----------|----------------|
| 检索策略 | 一次性固定检索 | 迭代动态检索，基于中间结果调整查询 |
| 规划能力 | 无规划，直接检索 | 问题分解、子任务调度、多步推理 |
| 工具调用 | 单一检索工具 | 多工具（搜索、代码解释器、计算器等） |
| 答案可信度 | 依赖检索质量 | 引用归因 + 多源验证 |
| 安全暴露面 | 检索结果污染 | 规划劫持 + 工具调用注入 + 检索污染 |

---

## 2. 研究格局与核心问题

### 2.1 五大核心研究维度

```
┌─────────────────────────────────────────────────────────┐
│                   Agentic Search Pipeline                │
│                                                          │
│  User Query → [Plan] → [Search×N] → [Generate] → Answer │
│                  ↑          ↑            ↑               │
│             规划安全    检索安全      生成安全             │
└─────────────────────────────────────────────────────────┘
```

| 维度 | 核心问题 | 威胁来源 |
|------|----------|----------|
| **规划安全** | 问题分解链是否被恶意查询或注入劫持？ | 对抗性用户输入、多步推理欺骗 |
| **检索安全** | 检索结果中的对抗性内容能否影响最终答案？ | 检索污染（Retrieval Poisoning）、对抗性 SEO |
| **生成安全** | 基于检索内容的答案是否产生幻觉或引用伪造？ | 知识冲突、引用幻觉 |
| **工具调用安全** | 调用搜索 API / 代码解释器时是否存在间接提示注入？ | 工具链劫持（Tool Hijacking） |
| **隐私安全** | 多轮检索-生成过程中是否泄露用户意图或个人信息？ | 意图推断、会话泄露 |

### 2.2 攻击-防御博弈格局（初始判断，待论文充实）

**攻击侧的独特性**：Agentic Search 的检索结果直接构成生成上下文，意味着攻击者只需污染**一篇公开网页**，就可能影响该系统对数百万用户的回答——这种"单点污染、广播影响"的特性，远比传统 LLM 越狱攻击的威胁面更大。

**防御侧的挑战**：规划步骤本身很难进行白盒分析（规划过程通常在模型内部完成），使得检测规划层注入比检测简单的 prompt injection 更困难。

---

## 3. 核心论文（待填充）

> 本节将随每日自动化任务持续填充。每新增一篇论文，在对应子节追加一行。

### 3.1 Agentic Search 能力研究

| 论文 | arXiv | 年份 | 核心贡献 | 详情 |
|------|-------|------|----------|------|
| PROClaim | [2603.28488](https://arxiv.org/abs/2603.28488) | 2026 | 渐进式 RAG 评估基准，7步骤框架 | [详情](../categories/agentic-search/papers/2603.28488_proclaim.md) |

**PROClaim 核心发现**：渐进式检索-评估-扩展框架（7步骤）在多跳问答任务上较传统 RAG 提升 18.3%，并揭示了 Agentic Search 的关键能力瓶颈："过早收敛"（Premature Convergence）——模型倾向于在找到第一个可行答案后停止检索，导致漏掉更优解。

### 3.2 检索污染与对抗性攻击

| 论文 | arXiv | 年份 | 攻击类型 | 详情 |
|------|-------|------|----------|------|
| ADAM | [2604.09747](https://arxiv.org/abs/2604.09747) | 2026 | 自适应记忆抽取 / topic-guided probing | [详情](../categories/agentic-search/papers/2604.09747_adam_agent_memory_extraction.md) |

**ADAM 核心发现**：对 memory-enabled agent 来说，最危险的不再是单次 prompt injection，而是基于 topic distribution estimation 的主动搜索。ADAM 用 weighted k-center + entropy-guided querying 系统化探索私有记忆分布，在多种 agent / LLM 组合上把 memory extraction 推到 up to 100% ASR，说明长期记忆已经成为独立且高危的运行时攻击面。

### 3.3 可信生成与引用归因防御

| 论文 | arXiv | 年份 | 防御机制 | 详情 |
|------|-------|------|----------|------|
| — | — | — | 待收录 | — |

### 3.4 评测基准

| 论文 | arXiv | 年份 | 基准类型 | 详情 |
|------|-------|------|----------|------|
| Plan-RewardBench | [2604.08178](https://arxiv.org/abs/2604.08178) | 2026 | 长轨迹 Reward Modeling 评估 | [详情](../categories/agentic-search/papers/2604.08178_plan_rewardbench.md) |
| ACIArena | [2604.07775](https://arxiv.org/abs/2604.07775) | 2026 | 多智能体级联注入评估 | [详情](../categories/agentic-search/papers/2604.07775_aciarena.md) |

| 论文 | arXiv | 年份 | 评测维度 | 详情 |
|------|-------|------|----------|------|
| Meerkat | [2604.11806](https://arxiv.org/abs/2604.11806) | 2026 | 仓库级轨迹安全审计 / witness 搜索 | [详情](../categories/agentic-search/papers/2604.11806_meerkat.md) |
| Near-Miss | [2603.29665](https://arxiv.org/abs/2603.29665) | 2026 | Agent 策略合规性（过程维度） | [详情](../categories/agentic-search/papers/2603.29665_near_miss_latent_policy_failure.md) |
| ACIArena | [2604.07775](https://arxiv.org/abs/2604.07775) | 2026 | Agent 级联注入统一评估（1356 案例，6 种 MAS） | [详情](../categories/agentic-search/papers/2604.07775_aciarena.md) |

**ACIArena 核心发现**：
首个 Agent Cascading Injection (ACI) 统一评估框架。四大反直觉发现：(1) 拓扑隔离不足以保障 MAS 安全——"连不连"不是关键；(2) 鲁棒 MAS 需要精心设计的角色 + 受控交互——安全来自身份认知；(3) 简化环境的防御无法迁移到真实场景；(4) 窄范围防御可能引入新漏洞。覆盖 6 种主流 MAS 实现、1,356 测试案例、3×3 攻击面矩阵。

**Near-Miss 核心发现**：在 τ²-verified Airlines benchmark 上，8-17% 的 Agent 执行轨迹存在"近失"（绕过策略检查但侥幸正确），这些案例在传统最终状态评估中全部"通过"，揭示当前评估方法论的系统性盲点。

**Meerkat 核心发现**：安全审计不应只看单条 trace，而要搜索能共同构成违规证据的 witness 集。Meerkat 通过“聚类 + agentic search”在大规模轨迹仓库中定位稀疏失败，在 CyBench、Terminal-Bench、HAL USACO 等真实 benchmark 中挖出了 developer cheating 与 reward hacking 的仓库级证据，标志着 Agent 安全评估从单轨迹分类进入 repository-level auditing 阶段。

### 3.5 轨迹与工具调用安全

| 论文 | arXiv | 年份 | 评测维度 | 详情 |
|------|-------|------|----------|------|
| TraceSafe | [2604.07223](https://arxiv.org/abs/2604.07223) | 2026 | 多步工具调用轨迹的中间安全性 | [详情](../categories/agentic-search/papers/2604.07223_tracesafe_agent_guardrails.md) |
| STARS | [2604.10286](https://arxiv.org/abs/2604.10286) | 2026 | 请求条件化的 skill invocation 连续风险评分 | [详情](../categories/agentic-search/papers/2604.10286_stars.md) |
| ClawGuard | [2604.11790](https://arxiv.org/abs/2604.11790) | 2026 | tool-call boundary 运行时最小权限防护 | [详情](../categories/agentic-search/papers/2604.11790_clawguard.md) |
| PlanGuard | [2604.10134](https://arxiv.org/abs/2604.10134) | 2026 | planning-based consistency verification 抵御 IPI | [详情](../categories/agentic-search/papers/2604.10134_planguard.md) |

| SkillTrojan | [2604.06811](https://arxiv.org/abs/2604.06811) | 2026 | 第三方工具文档描述后门注入 | [详情](../categories/agentic-search/papers/2604.06811v1_SkillTrojan.md) |
| TRUSTDESC | [2604.07536](https://arxiv.org/abs/2604.07536) | 2026 | 工具投毒防御：代码即真相的受信描述生成 | [详情](../categories/agentic-search/papers/2604.07536_trustdesc.md) |

**TRUSTDESC 核心发现**：
工具投毒攻击（TPA）分为显式（嵌入恶意指令）和隐式（误导性功能声明）两类，现有防御对隐式 TPA 完全无效。TRUSTDESC 通过"代码即真相"策略——从源代码自动生成受信工具描述——从根本上缓解了隐式 TPA。三阶段流水线（SliceMin 代码切片 → DescGen 描述生成 → DynVer 动态验证）在 52 个真实工具上验证有效。

**SkillTrojan 核心发现**：
向大模型智能体第三方“技能（Tool）”的自然语言文档描述中注入后门指令。该技术不仅能劫持当前任务，还会引发上下文持久污染（Context Poisoning），而传统代码扫描工具对此束手无策，这确立了第三方工具供应链安全的严峻挑战。

**TraceSafe 核心发现**：
随着 LLM 向 Agent 演进，攻击面转移到“中间执行轨迹”。评估 13 个基座模型与 7 种护栏后发现，模型安全性极大地受限于**处理结构化数据（如 JSON 解析）的瓶颈**，这比纯语义对齐更重要。同时，通用 LLM（架构优势）在审计中间轨迹时，效果大幅超越专注于文本的专用安全护栏。这标志着防御焦点必须转向系统状态机与结构化 API 负载。

**STARS 核心发现**：
技能安全不应只做静态扫描，而应按“用户请求 + skill + 运行时上下文”计算 activation risk。STARS 通过 SIA-Bench 证明，在 held-out 的 indirect prompt injection 场景里，请求条件化的连续风险评分显著优于仅靠 capability prior 的静态方法，说明 skill 安全已进入 invocation-level auditing 阶段。

**PlanGuard 核心发现**：
相比继续在输入端补规则，PlanGuard 直接把 Agent 安全重写成“规划-执行一致性验证”：先用只读用户原始请求的 Isolated Planner 生成 reference action set，再做两阶段运行时核验。其在 InjecAgent 上把 indirect prompt injection 的 ASR 从 72.8% 压到 0%，同时把误报率压到约 1.49%，代表了 planning-aware runtime guardrail 这条新防线。

**ClawGuard 核心发现**：
与其要求模型持续识别恶意文本，不如在真正执行工具调用前做确定性授权。ClawGuard 把防御点下沉到 tool-call boundary，在 AgentDojo、SkillInject、MCPSafeBench 上都显著压低 ASR，代表了一条“运行时 reference monitor for agents”的工程化防线。

---

### 3.6 视觉与注意力安全（NEW — 2026-04-12 新增）

| 论文 | arXiv | 年份 | 攻击类型 | 详情 |
|------|-------|------|----------|------|
| GUI Distraction | [2604.07831](https://arxiv.org/abs/2604.07831) | 2026 | 语义级 UI 元素注入劫持视觉定位 | [详情](../categories/agentic-search/papers/2604.07831_gui_distraction.md) |
| PRAC | [2604.08005](https://arxiv.org/abs/2604.08005) | 2026 | 注意力集中偏好重定向攻击（CUA 视觉模态） | [详情](../categories/agentic-search/papers/2604.08005_prac_attack.md) |

**PRAC 核心发现**：
首次揭示 CUA（计算机使用代理）视觉模态的注意力机制脆弱性。PRAC 通过在 GUI 中嵌入隐蔽对抗性补丁重定向 VLM 的内部注意力，间接操控 CUA 决策偏好。关键威胁：**一次白盒攻击可跨微调迁移至所有同源衍生 CUA**，构成供应链级风险。这标志着 Agent 安全从纯语言维度扩展到了视觉交互空间。

---

### 3.7 协议治理、路由经济学与生命周期防线（NEW — 2026-04-17 新增）

| 论文 | arXiv | 年份 | 方向 | 详情 |
|------|-------|------|------|------|
| MemJack | [2604.12616](https://arxiv.org/abs/2604.12616) | 2026 | 多智能体记忆增强 VLM 越狱 | [详情](../categories/agentic-search/papers/2604.12616_memjack_vlm.md) |
| MCPThreatHive | [2604.13849](https://arxiv.org/abs/2604.13849) | 2026 | MCP 生态威胁情报 / taxonomy | [详情](../categories/agentic-search/papers/2604.13849_mcp_threat_hive.md) |
| SafeHarness | [2604.13630](https://arxiv.org/abs/2604.13630) | 2026 | 生命周期集成式 Agent 防线 | [详情](../categories/agentic-search/papers/2604.13630_safeharness.md) |
| R2A | [2604.15022](https://arxiv.org/abs/2604.15022) | 2026 | 路由经济攻击 / cost amplification | [详情](../categories/agentic-search/papers/2604.15022_r2a.md) |
| CBCL | [2604.14512](https://arxiv.org/abs/2604.14512) | 2026 | 协议级通信治理 / formality-by-design | [详情](../categories/agentic-search/papers/2604.14512_cbcl.md) |

**MemJack 核心发现**：
攻击者不再需要伪造图片或做像素扰动，只需利用**自然良性图像 + 记忆增强的多智能体协同**，就能把 VLM 越狱做成一套可迁移的视觉语义社会工程。其在 Qwen3-VL-Plus 上达到 **72% ASR**，放宽预算后可到 **90%**，说明“自然图像本身”已经成为高价值攻击锚点。

**MCPThreatHive 核心发现**：
MCP 风险不再只是零散的 prompt injection case，而开始被系统化为 **MCP-38 taxonomy + knowledge graph + composite risk scoring**。这意味着 MCP 安全正从“补洞”进入“持续威胁情报运营”阶段。

**SafeHarness 核心发现**：
相比继续把安全寄托在输入过滤器上，SafeHarness 把防线下沉到执行框架生命周期本身：输入过滤、因果验证、最小权限工具控制、状态回滚四层协同，在平均 ASR 上带来 **42% 绝对下降**。这说明 Agent 安全的正确控制点开始从 prompt 表面迁移到 **execution harness**。

**R2A 核心发现**：
Agent / Router 系统除了安全违规，还有**经济放大攻击面**。R2A 通过通用对抗后缀把原本应落到便宜模型的请求引流到昂贵模型，在 OpenRouter 上把平均成本放大到约 **2.7×–2.9×**。这标志着 Agent 安全首次明确进入“服务成本操纵”维度。

**CBCL 核心发现**：
当多 Agent 需要自扩展通信语言时，传统做法默认“可扩展”与“可验证”不可兼得。CBCL 用 DCFL + Lean/Rust tooling 证明：通信协议可以在运行时扩展，同时保留可验证语义边界。它把 Agent 安全进一步推进到**协议设计层**，而不是只做运行时拦截。

---

## 4. 与 T2T / T2I 安全的交叉关系

Agentic Search 安全并非完全独立的方向，它与本项目已追踪的其他领域存在深度交叉：

| 交叉方向 | 关联机制 | 参考论文 |
|----------|----------|----------|
| **T2T 提示注入** | Agentic Search 中的间接提示注入（通过网页内容）是 T2T 提示注入的扩展形式 | T-MAP (2603.22341)、LLM Agent Security (2603.19469) |
| **T2T Agent 安全** | Agentic Search 本质上是一类 LLM Agent，Agent 四属性安全框架（P1-P4）直接适用 | LLM Agent Security Framework (2603.19469) |
| **T2T 对抗性 SEO** | LLMSE SEO Attack (2603.25500) 已直接研究搜索引擎回答系统的 SEO 操纵 | LLMSE SEO Attack (2603.25500) |

---

## 5. 未来研究方向（初始前瞻）

基于领域分析，以下是 Agentic Search 安全与能力研究在 2026-2027 年的关键开放问题：

### 近期（1-2 年）优先问题

**Gap 1：规划层的形式化安全分析**  
当前绝大多数工作关注检索层攻击，而对规划层（问题分解、子任务调度）的安全性几乎无系统性研究。需要发展规划过程的形式化安全模型。

**Gap 2：多轮检索中的上下文污染传播**  
当首轮检索结果被污染后，如何防止污染信息通过多轮迭代在上下文中"积累增强"？目前缺乏专门的防御机制。

**Gap 3：引用幻觉的自动检测**  
商业 Agentic Search 产品普遍存在"引用存在但内容不支持结论"的问题，尚无高效的运行时检测框架。

### 中期（3-5 年）核心挑战

**Gap 4：Agentic Search 的可解释规划审计**  
借鉴 T2T 方向的机制可解释性（如 SafeSeek 安全电路归因），建立 Agentic Search 规划步骤的可审计机制。

**Gap 5：跨系统检索污染的协调防御**  
当攻击者同时在多个搜索引擎投毒时，单一 Agentic Search 系统的局部防御无效；需要跨平台的协作检测机制。

---

## 6. 增量论文索引（重点条目）

> 随每日任务自动追加，按收录日期倒序排列；这里保留重点增量条目而非全库逐篇平铺。

| # | arXiv ID | 标题 | 类型 | 收录日期 | 链接 |
|---|----------|------|------|----------|------|
| 21 | 2604.15022 | Routing to Riches: How to Make Your Router Expensive | 攻击/路由经济操纵 | 2026-04-17 | [详情](../categories/agentic-search/papers/2604.15022_r2a.md) |
| 20 | 2604.14512 | CBCL: Safe Self-Extending Agent Communication | 防御/协议级通信治理 | 2026-04-17 | [详情](../categories/agentic-search/papers/2604.14512_cbcl.md) |
| 19 | 2604.13849 | MCPThreatHive: Automated Threat Intelligence for Model Context Protocol Ecosystems | 防御/MCP 威胁情报 | 2026-04-17 | [详情](../categories/agentic-search/papers/2604.13849_mcp_threat_hive.md) |
| 18 | 2604.13630 | SafeHarness: Lifecycle-Integrated Security Architecture for LLM-based Agent Deployment | 防御/生命周期集成框架 | 2026-04-17 | [详情](../categories/agentic-search/papers/2604.13630_safeharness.md) |
| 17 | 2604.12616 | Every Picture Tells a Dangerous Story: Memory-Augmented Multi-Agent Jailbreak Attacks on VLMs | 攻击/记忆增强视觉越狱 | 2026-04-17 | [详情](../categories/agentic-search/papers/2604.12616_memjack_vlm.md) |
| 16 | 2604.10134 | PlanGuard: Defending Agents against Indirect Prompt Injection via Planning-based Consistency Verification | 防御/规划-执行一致性验证 | 2026-04-15 | [详情](../categories/agentic-search/papers/2604.10134_planguard.md) |
| 15 | 2604.09747 | ADAM: A Systematic Data Extraction Attack on Agent Memory via Adaptive Querying | 攻击/记忆抽取 | 2026-04-15 | [详情](../categories/agentic-search/papers/2604.09747_adam_agent_memory_extraction.md) |
| 12 | 2604.11806 | Detecting Safety Violations Across Many Agent Traces | 评测/仓库级轨迹审计 | 2026-04-14 | [abs](https://arxiv.org/abs/2604.11806) |
| 13 | 2604.09378 | BadSkill: Backdoor Attacks on Agent Skills via Model-in-Skill Poisoning | 攻击/技能供应链后门 | 2026-04-14 | [详情](../categories/agentic-search/papers/2604.09378_badskill.md) |
| 14 | 2604.08608 | Semantic Intent Fragmentation: Single-Shot Compositional Attack on Multi-Agent Pipelines | 攻击/SIF组合攻击 | 2026-04-14 | [详情](../categories/agentic-search/papers/2604.08608_semantic_intent_fragmentation.md) |
| 11 | 2604.11790 | ClawGuard: A Runtime Security Framework for Tool-Augmented LLM Agents Against Indirect Prompt Injection | 防御/运行时边界防护 | 2026-04-14 | [abs](https://arxiv.org/abs/2604.11790) |
| 10 | 2604.10286 | STARS: Skill-Triggered Audit for Request-Conditioned Invocation Safety in Agent Systems | 评测/调用级风险审计 | 2026-04-14 | [abs](https://arxiv.org/abs/2604.10286) |
| 9 | 2604.08178 | Aligning Agents via Planning: A Benchmark for Trajectory-Level Reward Modeling | 评测/奖励模型 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.08178) |
| 8 | 2604.07831 | Are GUI Agents Focused Enough? Automated Distraction via Semantic-level UI Element Injection | 攻击/视觉劫持 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.07831) |
| 7 | 2604.08005 | PRAC: Preference Redirection via Attention Concentration (CUA Attack) | 攻击/视觉注意力 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.08005) |
| 6 | 2604.07775 | ACIArena: Toward Unified Evaluation for Agent Cascading Injection | 评测/MAS 安全 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.07775) |
| 5 | 2604.07536 | TRUSTDESC: Preventing Tool Poisoning via Trusted Description Generation | 防御/工具投毒 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.07536) |
| 4 | 2604.06811 | SkillTrojan: Backdoor Attacks on Skill-Based Agent Systems | 攻击/供应链后门 | 2026-04-09 | [abs](https://arxiv.org/abs/2604.06811) |
| 3 | 2604.07223 | TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories | 评测/中间轨迹安全 | 2026-04-09 | [abs](https://arxiv.org/abs/2604.07223) |
| 2 | 2603.29665 | Near-Miss: Latent Policy Failure Detection in Agentic Workflows | 评估/Benchmark | 2026-04-01 | [abs](https://arxiv.org/abs/2603.29665) |
| 1 | 2603.28488 | PROClaim: Progressive Retrieval-augmented Generation | 能力研究 | 2026-03-31 | [abs](https://arxiv.org/abs/2603.28488) |

---

*本 Survey 由 paper-research skill Phase 5 生成与维护 | 初始版本：2026-03-30 | v1.1 更新：2026-04-17*
*v1.1 更新说明：新增 MemJack、MCPThreatHive、SafeHarness、R2A、CBCL 五篇重点论文，把 Agentic 安全从“注入 / 记忆抽取”进一步推进到视觉语义社工、MCP 威胁情报、execution harness、安全经济学与协议级治理。*
