# AI安全T2T&T2I每日情报 - 执行记录

## 执行历史

### 2026-03-30
- **日期**: 2026-03-30
- **执行时间**: 08:00（自动化任务）
- **论文数量**: 6 篇（T2T: 4 篇, T2I: 2 篇）
- **Commit Hash**: 05e4d88
- **状态**: 成功

**新增论文**:
1. 2603.26221 - Clawed and Dangerous: Open Agentic Systems Security (Benchmark/Survey)
2. 2603.25056 - The System Prompt Is the Attack Surface (Attack)
3. 2603.25861 - Why Safety Probes Catch Liars But Miss Fanatics (Defense)
4. 2603.26045 - H-Node Attack and Defense in LLMs (Attack+Defense)
5. 2603.26328 - Verify T2I Models via BPO (Benchmark, CVPR 2026)
6. 2603.26316 - SALMUBench: Multimodal Unlearning Benchmark (Benchmark, CVPR 2026)

**Survey 更新**:
- t2t-survey.md: 31→35 篇，新增 3.3 代理安全治理章节和 4.6 探测边界章节
- t2i-survey.md: 44→46 篇，新增 7.2 T2I 模型生命周期安全章节
- AI_Security_Landscape_2026.md: 75+→81+ 篇，新增热点六（代理安全治理化）和热点七（T2I 生命周期安全）

**关键发现**:
- "狂热者效应"：RLHF 对齐可能无意间训练出对探测完全不可见的一致性错位模型
- 代理安全研究从"攻防"走向"治理"，系统提示设计是核心安全变量
- CVPR 2026 双收录论文标志 T2I 安全进入生命周期管理阶段
- H-Node 幻觉节点机制分析是 LLM 可靠性安全的重要突破

---

### 2026-03-31
- **日期**: 2026-03-31
- **执行时间**: 09:45（手动触发）
- **论文数量**: 6 篇（T2T: 5 篇, Agentic Search: 1 篇）
- **Commit Hash**: e9fa55c
- **状态**: 成功

**新增论文**:
1. 2603.28655 - Safeguarding LLMs Against Misuse and AI-Driven Malware Using Steganographic Canaries (Defense)
2. 2603.28013 - Kill-Chain Canaries: Stage-Level Tracking of Prompt Injection (Defense)
3. 2603.27148 - SafetyDrift: Predicting When AI Agents Cross the Line (Defense)
4. 2603.27918 - Adversarial Attacks on MLLMs: A Comprehensive Survey (Benchmark, TMLR)
5. 2603.27517 - A Systematic Taxonomy of Security Vulnerabilities in OpenClaw (Benchmark)
6. 2603.28488 - PROClaim: Courtroom-Style Multi-Agent Debate with Progressive RAG (Defense, Agentic Search首篇)

**关键发现**:
- "预测与追踪"成为防御技术新趋势：SafetyDrift通过吸收马尔可夫链提前3.7步预警，Kill-Chain Canaries精确定位防御失效阶段
- Claude在write_memory阶段有效剥离注入（0% ASR），而GPT-4o-mini传播金丝雀无损失（53% ASR）
- OpenClaw结构性弱点：每层独立信任执行使跨层攻击难以防范
- Agentic Search方向首篇论文收录：PROClaim展示渐进式RAG在多智能体验证中的强大能力

---

- **日期**: 2026-03-28（第二次执行）
- **执行时间**: 19:13
- **论文数量**: 3篇（全部 T2T 方向）
- **Commit Hash**: b8bf19e
- **状态**: 成功

**新增论文**:
1. 2603.23791 - The Cognitive Firewall: Browser AI Agent IPI Defense (Defense)
2. 2603.25500 - LLMSE Black-Hat SEO Resilience Evaluation, SEO-Bench (Benchmark)
3. 2603.24917 - Near-Verbatim Extraction Risk Estimation via Beam Search (Benchmark)

**备注**: 今日共两次执行，累计收录11篇（早晨8次+晚间3次）。晚间补充发现了浏览器代理防御、LLM搜索引擎安全评估、训练数据隐私风险量化三个新方向。

---

### 2026-03-28
- **日期**: 2026-03-28
- **论文数量**: 8篇（T2T: 7篇, T2I/VLM: 1篇）
- **Commit Hash**: 56b2f0448b9b6c9d4f79f6361e573a2c0bf57e22
- **状态**: 成功

**收录论文列表**:
1. 2603.25412 - Beyond Content Safety: Real-Time Monitoring for Reasoning Vulnerabilities (Defense)
2. 2603.25164 - PIDP-Attack: Combining Prompt Injection with Database Poisoning (Attack)
3. 2603.25176 - Prompt Attack Detection with LLM-as-a-Judge (Defense)
4. 2603.24203 - TIP: Tree-based Injection for MCP Protocol (Attack)
5. 2603.24857 - AI Security Survey: Unified Threat Taxonomy (Benchmark)
6. 2603.23822 - CLIQ: Edge LLM Knowledge Extraction (Attack)
7. 2603.24543 - Steering Vectors Safety Pitfalls (Attack)
8. 2603.25403 - VLM Dual-Layer Side-Channel Attack (Attack)

**生成文件**:
- daily-reports/2026-03/2026-03-28_AI安全每日深度情报.md
- daily-reports/t2t/2026-03/2026-03-28_t2t_每日情报.md
- daily-reports/t2i/2026-03/2026-03-28_t2i_每日情报.md
- categories/t2t/papers/2603.25412_reasoning_safety_monitor.md
- categories/t2t/papers/2603.25164_pidp_attack.md
- categories/t2t/papers/2603.25176_prompt_attack_detection.md
- categories/t2t/papers/2603.24203_tip_mcp_attack.md
- categories/t2t/papers/2603.24857_ai_security_survey.md
- categories/t2t/papers/2603.23822_edge_llm_vulnerability.md
- categories/t2t/papers/2603.24543_steering_vectors_safety.md
- categories/t2i/papers/2603.25403_vlm_side_channel.md

**关键发现**:
- 推理安全成为新的研究热点（推理监控器）
- MCP协议、边缘部署、动态预处理等新攻击面浮现
- 复合攻击（PIDP-Attack）和精细化攻击（TIP、CLIQ）技术持续演进
- 统一威胁分类法框架为系统性安全研究提供新视角
