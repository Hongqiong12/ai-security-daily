# 2026-04-02 Agentic Search 每日情报

> **生成时间**: 2026-04-02 09:42  
> **论文数量**: 2 篇  
> **方向**: Agentic Search / Agentic RAG  

---

## 执行摘要

今日 Agentic Search 方向收录 2 篇能力研究论文，分别从**故障修复**和**训练数据生成**两个维度推进了 Agentic RAG 系统的工程化可行性。Doctor-RAG 提出精准的局部修复框架，将 Agentic RAG 的可靠性从"成功/失败"的二元判断升级为"诊断-定位-修复"的全流程管理；ORBIT 则以极低成本解决了搜索Agent的训练数据瓶颈，为小参数模型在多步推理任务上的能力提升提供了可扩展的数据基础。

---

## 今日论文

### [AS-01] Doctor-RAG: Failure-Aware Repair for Agentic Retrieval-Augmented Generation

**arXiv**: 2604.00865 | **分类**: Capability | **来源**: cs.IR

**一句话摘要**: 提出统一的诊断-修复框架，通过精准定位Agentic RAG轨迹中的最早失败点并进行局部修复，以最小计算代价显著提升多跳问答准确性。

**核心创新**:

**覆盖门控分类法（Coverage-Gated Taxonomy）**  
系统化分类 Agentic RAG 的失败模式：检索覆盖失败（~60%）、推理链断裂（~30%）、证据冲突（~10%）。这一分类法首次为 Agentic RAG 失败建立了量化的故障地图。

**前缀重用局部修复**  
形式化：给定轨迹 τ = (r₁, a₁, ..., rₙ, aₙ)，识别最早失败点 k，仅修复 τ_{k:end}，保留已验证的前缀 τ_{1:k-1}。相比全流程重跑，大幅降低推理令牌消耗。

**工程价值**:
- 适用于知识密集型问答、Deep Research 类产品的自动错误恢复
- 故障分类法可作为 Agentic RAG 系统的标准日志分析框架

---

### [AS-02] ORBIT: Scalable and Verifiable Data Generation for Search Agents on a Tight Budget

**arXiv**: 2604.01195 | **分类**: Capability | **来源**: cs.CL (cross-listed cs.IR)

**一句话摘要**: 四阶段低成本数据生成框架，产出2万条4-5步推理密集型搜索查询，训练的ORBIT-4B在4B参数搜索Agent中达到领先性能。

**核心框架**:
1. **种子创建**: 从 Wikipedia/Wikidata 提取多样化主题种子
2. **问答对生成**: 生成需 4-5 步推理、答案短且可验证的查询
3. **自我验证**: 过滤逻辑不自洽的样本
4. **外部搜索验证**: 使用真实搜索引擎验证事实准确性（无需付费API）

**关键指标**:
- 数据集: 2万条查询 × 15个领域 × 4-5步推理
- 训练结果: ORBIT-4B（Qwen3-4B + GRPO）在4B参数级别达到领先性能
- 成本: 接近零数据成本（near-zero data cost）

**安全研究视角**: ORBIT 框架的外部搜索验证阶段引入了潜在的安全攻击面——若攻击者能在验证阶段注入恶意搜索结果（检索中毒），可能系统性污染训练数据，为未来的 Agentic Search 安全研究提供了重要的研究载体。

---

## Agentic Search 能力图谱更新

随着 Doctor-RAG 和 ORBIT 的加入，当前已收录的 Agentic Search 论文构建了较为完整的能力研究图谱：

```
训练阶段 ─────────────────────────── 推理阶段
    │                                     │
ORBIT (2604.01195)          PROClaim (2603.28488)
低成本训练数据生成           多智能体辩论验证答案
    │                                     │
    └──────────── Doctor-RAG (2604.00865) ─┘
                    故障定位+局部修复
                    
         Near-Miss (2603.29665) [横跨推理阶段]
         隐性策略失败检测与预警
```

四篇论文分别覆盖：训练数据→推理时验证→推理时修复→预警监控，形成完整的 Agentic RAG 可靠性保障链条。

---

## 趋势洞察

**可靠性工程化**: Agentic Search 研究正从"提升平均性能"转向"保证最差情况可控"。Doctor-RAG 的故障修复和 Near-Miss 的隐性失败检测都体现了这一转变：研究者开始像工程师处理软件可靠性问题一样处理 Agentic RAG 的失败场景。

**数据飞轮**: ORBIT 的低成本数据生成能力一旦与搜索Agent的强化学习训练循环结合，可能形成自我改进的数据飞轮，这将显著加速搜索Agent能力的提升速度。

---

## 引用索引

| ArXiv ID | 标题 | 子分类 | 关键词 |
|----------|------|--------|--------|
| 2604.00865 | Doctor-RAG | Capability | Agentic RAG, Failure Repair, Multi-hop QA |
| 2604.01195 | ORBIT | Capability | Search Agent, Data Generation, Agentic Reasoning |

*下一期预计: 2026-04-03*
