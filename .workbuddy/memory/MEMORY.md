# 全局研究策略与自动化任务偏好

## 1. 核心研究焦点 (2026-04-17 更新)
- **核心倾斜**: 当前及后续的主要工作重心完全侧重在 **文生图 (Text-to-Image, T2I)** 和 **文图生图 (Multimodal-to-Image, T+I2I)** 领域。
- **重点关注议题**: 
  - **安全对齐** (Safety Alignment)
  - **多模态安全 Benchmark** (Safety Benchmark / Evaluation)
  - NSFW概念擦除/对抗 (Concept Erasure)
  - VLM (Vision-Language Model) 与生图安全交叉领域
- **降级关注**: 文生文 (T2T) 和 Agent 安全 (Agentic Search) 现阶段作为辅助与背景参考，优先级下调。

## 2. 自动化执行规范 (WORKFLOW)
- `WORKFLOW.md` 中的检索策略与论文归档，应当始终优先检索 `("text-to-image" OR "multimodal-to-image") AND ("safety alignment" OR "benchmark" ...)`。
- 对于每日的自动化推送，T2I/T+I2I 相关论文必须位于报告首位，并占据最大权重。

## 3. 历史主线共识
- 仅保留与核心论文（尤其是 LoRA 概念擦除/低秩概念擦除、SDXL 擦除实验、MACE/ESD/UCE）等主线任务相关的长期记忆。
- 拒绝任何泛泛的 AI 话术或不专业的输出，交付物必须高度结构化（编号、表格、精美排版）。
- 任何统计必须通过真实的 `search_file` 脚本计算，禁止虚假估算。