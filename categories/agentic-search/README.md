# 🤖 Agentic Search Model 安全与能力研究

Agentic Search Model 是指具备自主规划（Plan）、动态检索（Search）和生成回复（Generate）能力的大模型系统。
与传统 RAG 不同，Agentic Search Model 在回复前会主动分解问题、调用工具、迭代搜索，直至收集到足够信息再合成最终答案。

典型代表：Perplexity AI、GPT Search（SearchGPT）、Gemini Deep Research、Grok Search、Kimi Search、天工 AI、
以及基于 ReAct / Self-RAG / WebGPT / Search-o1 / DeepSearch 等框架构建的系统。

| 子类别 | 说明 |
|--------|------|
| [benchmark](./benchmark/) | 评测集与评估框架：端到端检索-生成评测、幻觉率、引用准确率 |
| [attack](./attack/) | 攻击类：检索污染、对抗性 SEO 注入、工具调用劫持、规划层攻击 |
| [defense](./defense/) | 防御类：可信检索验证、引用归因、规划过程安全审计 |

---

## 📋 论文列表

<!-- 每次新增论文后在此追加，按日期倒序 -->

### 2026-04-14

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| Meerkat | [2604.11806](https://arxiv.org/abs/2604.11806) | 审计/Benchmark | 首次把跨大量 agent traces 的安全审计建模为 witness set 搜索 | [详情](./papers/2604.11806_meerkat.md) |
| ClawGuard | [2604.11790](https://arxiv.org/abs/2604.11790) | 防御 | 在 tool-call boundary 执行运行时最小权限防护，显著压制间接提示注入 | [详情](./papers/2604.11790_clawguard.md) |
| STARS | [2604.10286](https://arxiv.org/abs/2604.10286) | 审计/Benchmark | 将 skill invocation 风险建模为请求条件化的连续分数，并引入 SIA-Bench | [详情](./papers/2604.10286_stars.md) |

---

### 2026-03-31（首篇收录）

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| PROClaim | [2603.28488](https://arxiv.org/abs/2603.28488) | 防御 | 法庭风格多智能体辩论+P-RAG，Check-COVID 81.7%准确率，+10pp提升 | [详情](./papers/2603.28488_proclaim.md) |

---

### 研究方向速览

| 维度 | 核心问题 |
|------|----------|
| **Planning 安全** | Agentic 规划链是否被恶意查询或注入劫持？ |
| **Search 安全** | 检索结果中的对抗性内容能否影响最终答案？ |
| **Generation 安全** | 基于检索内容生成的答案是否产生幻觉或引用伪造？ |
| **工具调用安全** | 调用搜索 API / 代码解释器时是否存在提示注入风险？ |
| **隐私泄露** | 多轮检索-生成过程中是否泄露用户意图或个人信息？ |
