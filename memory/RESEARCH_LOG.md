### [2026-05-01] Leveraging Verifier-Based Reinforcement Learning in Image Editing
- **Authors**: Hanzhong Guo, Jie Wu, Jie Liu, Yu Gao, Zilyu Ye, Linxiao Yuan, Xionghui Wang, Yizhou Yu, Weilin Huang
- **Link**: https://arxiv.org/abs/2604.27505
- **Summary**: 提出 Edit-R1，把图像编辑 reward model 升级为 verifier-style reasoning reward，用 Keep / Follow / Quality 原则级核验替代黑盒整体打分。对 T2I 输入侧安全改写最直接的价值是提供三维 judge 雏形：风险下降、语义保持、指令遵循可以被拆开评测。

### [2026-05-01] Benchmarking Layout-Guided Diffusion Models through Unified Semantic-Spatial Evaluation in Closed and Open Settings
- **Authors**: Luca Parolari, Nicla Faccioli, Lamberto Ballan
- **Link**: https://arxiv.org/abs/2604.25358
- **Summary**: 提出 CoBench，统一评测 layout-guided T2I 的 text alignment、layout alignment 与 unified score。对当前业务的关键启发是不要用单一 overall score 评估 rewrite，而应先拆维度，再做统一聚合。

### [2026-05-01] TextGround4M: A Prompt-Aligned Dataset for Layout-Aware Text Rendering
- **Authors**: Dongxing Mao, Yilin Wang, Linjie Li, Zhengyuan Yang, Alex Jinpeng Wang
- **Link**: https://arxiv.org/abs/2604.24459
- **Summary**: 构建 4.1M prompt-grounded 文本渲染数据集，并引入 Prompt Coverage、Layout IoU 等指标，补齐 OCR-rich / layout-rich 终态评测。说明未来 T2I rewrite 评测需要覆盖海报、卡片、说明图等真实传播场景。

### [2026-05-01] Breaking Watermarks in the Frequency Domain: A Modulated Diffusion Attack Framework
- **Authors**: Chunpeng Wang, Binyan Qu, Xiaoyu Wang, Zhiqiu Xia, Shanshan Zhang, Yunan Liu, Qi Li
- **Link**: https://arxiv.org/abs/2604.22220
- **Summary**: 提出 FMDiffWA，用频域调制与扩散模型做高保真 watermark removal，说明 provenance / watermark 防线必须按强攻击者假设设计。对业务的迁移价值主要在评测层：安全系统不能只和弱攻击者比较。