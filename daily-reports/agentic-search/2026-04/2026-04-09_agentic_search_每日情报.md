# 2026-04-09 Agentic Search 安全每日情报

## 本日核心洞察
Agentic Search 的安全焦点正在向**多步轨迹审计**和**第三方技能供应链漏洞**转移。
*   TraceSafe 指出传统的单轮 Prompt 护栏在面对“分片化、多步执行”的智能体工具调用链时形同虚设，必须引入状态机级别的轨迹审计。
*   SkillTrojan 揭露了通过向第三方工具文档描述中注入后门指令的新型攻击路径。这表明，自然语言描述已经成为智能体执行权限的一部分，传统代码审计工具对其失效。

## 深度解读论文列表
1. [TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories](../../../categories/agentic-search/papers/2604.07223v1_TraceSafe.md)
2. [SkillTrojan: Backdoor Attacks on Skill-Based Agent Systems](../../../categories/agentic-search/papers/2604.06811v1_SkillTrojan.md)
