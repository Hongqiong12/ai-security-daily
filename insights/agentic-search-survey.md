# Agentic Search Model 安全与能力研究 Survey

> **版本**: v0.5（增量更新：ACIArena + TRUSTDESC + PRAC）
> **更新日期**: 2026-04-12
> **覆盖论文数**: 14 篇  
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
| — | — | — | 待收录（见研究空白 Gap 1） | — |

### 3.3 可信生成与引用归因防御

| 论文 | arXiv | 年份 | 防御机制 | 详情 |
|------|-------|------|----------|------|
| — | — | — | 待收录 | — |

### 3.4 评测基准

| 论文 | arXiv | 年份 | 评测维度 | 详情 |
|------|-------|------|----------|------|
| Near-Miss | [2603.29665](https://arxiv.org/abs/2603.29665) | 2026 | Agent 策略合规性（过程维度） | [详情](../categories/agentic-search/papers/2603.29665_near_miss_latent_policy_failure.md) |
| ACIArena | [2604.07775](https://arxiv.org/abs/2604.07775) | 2026 | Agent 级联注入统一评估（1356 案例，6 种 MAS） | [详情](../categories/agentic-search/papers/2604.07775_aciarena.md) |

**ACIArena 核心发现**：
首个 Agent Cascading Injection (ACI) 统一评估框架。四大反直觉发现：(1) 拓扑隔离不足以保障 MAS 安全——"连不连"不是关键；(2) 鲁棒 MAS 需要精心设计的角色 + 受控交互——安全来自身份认知；(3) 简化环境的防御无法迁移到真实场景；(4) 窄范围防御可能引入新漏洞。覆盖 6 种主流 MAS 实现、1,356 测试案例、3×3 攻击面矩阵。

**Near-Miss 核心发现**：在 τ²-verified Airlines benchmark 上，8-17% 的 Agent 执行轨迹存在"近失"（绕过策略检查但侥幸正确），这些案例在传统最终状态评估中全部"通过"，揭示当前评估方法论的系统性盲点。


### 3.5 轨迹与工具调用安全

| 论文 | arXiv | 年份 | 评测维度 | 详情 |
|------|-------|------|----------|------|
| TraceSafe | [2604.07223](https://arxiv.org/abs/2604.07223) | 2026 | 多步工具调用轨迹的中间安全性 | [详情](../categories/agentic-search/papers/2604.07223_tracesafe_agent_guardrails.md) |

| SkillTrojan | [2604.06811](https://arxiv.org/abs/2604.06811) | 2026 | 第三方工具文档描述后门注入 | [详情](../categories/agentic-search/papers/2604.06811v1_SkillTrojan.md) |
| TRUSTDESC | [2604.07536](https://arxiv.org/abs/2604.07536) | 2026 | 工具投毒防御：代码即真相的受信描述生成 | [详情](../categories/agentic-search/papers/2604.07536_trustdesc.md) |

**TRUSTDESC 核心发现**：
工具投毒攻击（TPA）分为显式（嵌入恶意指令）和隐式（误导性功能声明）两类，现有防御对隐式 TPA 完全无效。TRUSTDESC 通过"代码即真相"策略——从源代码自动生成受信工具描述——从根本上缓解了隐式 TPA。三阶段流水线（SliceMin 代码切片 → DescGen 描述生成 → DynVer 动态验证）在 52 个真实工具上验证有效。

**SkillTrojan 核心发现**：
向大模型智能体第三方“技能（Tool）”的自然语言文档描述中注入后门指令。该技术不仅能劫持当前任务，还会引发上下文持久污染（Context Poisoning），而传统代码扫描工具对此束手无策，这确立了第三方工具供应链安全的严峻挑战。

**TraceSafe 核心发现**：
随着 LLM 向 Agent 演进，攻击面转移到“中间执行轨迹”。评估 13 个基座模型与 7 种护栏后发现，模型安全性极大地受限于**处理结构化数据（如 JSON 解析）的瓶颈**，这比纯语义对齐更重要。同时，通用 LLM（架构优势）在审计中间轨迹时，效果大幅超越专注于文本的专用安全护栏。这标志着防御焦点必须转向系统状态机与结构化 API 负载。

---

### 3.6 视觉与注意力安全（NEW — 2026-04-12 新增）

| 论文 | arXiv | 年份 | 攻击类型 | 详情 |
|------|-------|------|----------|------|
| PRAC | [2604.08005](https://arxiv.org/abs/2604.08005) | 2026 | 注意力集中偏好重定向攻击（CUA 视觉模态） | [详情](../categories/agentic-search/papers/2604.08005_prac_attack.md) |

**PRAC 核心发现**：
首次揭示 CUA（计算机使用代理）视觉模态的注意力机制脆弱性。PRAC 通过在 GUI 中嵌入隐蔽对抗性补丁重定向 VLM 的内部注意力，间接操控 CUA 决策偏好。关键威胁：**一次白盒攻击可跨微调迁移至所有同源衍生 CUA**，构成供应链级风险。这标志着 Agent 安全从纯语言维度扩展到了视觉交互空间。

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

## 6. 论文完整索引

> 随每日任务自动追加，按收录日期倒序排列。

| # | arXiv ID | 标题 | 类型 | 收录日期 | 链接 |
|---|----------|------|------|----------|------|
| 7 | 2604.08005 | PRAC: Preference Redirection via Attention Concentration (CUA Attack) | 攻击/视觉注意力 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.08005) |
| 6 | 2604.07775 | ACIArena: Toward Unified Evaluation for Agent Cascading Injection | 评测/MAS 安全 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.07775) |
| 5 | 2604.07536 | TRUSTDESC: Preventing Tool Poisoning via Trusted Description Generation | 防御/工具投毒 | 2026-04-12 | [abs](https://arxiv.org/abs/2604.07536) |
| 4 | 2604.06811 | SkillTrojan: Backdoor Attacks on Skill-Based Agent Systems | 攻击/供应链后门 | 2026-04-09 | [abs](https://arxiv.org/abs/2604.06811) |
| 3 | 2604.07223 | TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories | 评测/中间轨迹安全 | 2026-04-09 | [abs](https://arxiv.org/abs/2604.07223) |
| 2 | 2603.29665 | Near-Miss: Latent Policy Failure Detection in Agentic Workflows | 评估/Benchmark | 2026-04-01 | [abs](https://arxiv.org/abs/2603.29665) |
| 1 | 2603.28488 | PROClaim: Progressive Retrieval-augmented Generation | 能力研究 | 2026-03-31 | [abs](https://arxiv.org/abs/2603.28488) |

---

*本 Survey 由 paper-research skill Phase 5 生成与维护 | 初始版本：2026-03-30 | v0.5 更新：2026-04-12*
*v0.5 更新说明：新增 ACIArena（MAS 级联注入评估）、TRUSTDESC（工具投毒防御）、PRAC（视觉注意力攻击）三篇论文，新增 3.6 视觉与注意力安全子节。*
