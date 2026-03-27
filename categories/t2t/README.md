# 📝 文生文 (Text-to-Text)

文本到文本的 LLM（如 GPT、Claude、LLaMA 等）相关安全论文。

| 子类别 | 说明 |
|--------|------|
| [benchmark](./benchmark/) | 基础评测集、基准测试 |
| [attack](./attack/) | 攻击类：越狱、提示注入、对抗样本等 |
| [defense](./defense/) | 防御类：安全对齐、越狱防御等 |

## 📋 论文列表

### 2026-03-25

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| TriageFuzz | [2603.23269](https://arxiv.org/abs/2603.23269) | 攻击 | Token 感知越狱测试，25 次查询 ASR 提升 20–40% | [详情](./papers/2603.23269_triagefuzz.md) |
| T-MAP | [2603.22341](https://arxiv.org/abs/2603.22341) | 攻击 | 轨迹感知 Agent 红队，MCP 漏洞挖掘 | [详情](./papers/2603.22341_tmap.md) |
| Activation Watermarking | [2603.23171](https://arxiv.org/abs/2603.23171) | 防御 | 激活水印监控，自适应攻击检测率提升 52% | [详情](./papers/2603.23171_activation_watermark.md) |

---

### 2026-03-23

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| PISmith | [2603.13026](https://arxiv.org/abs/2603.13026) | 攻击 | GRPO + 自适应熵正则化，ASR@10 达 100% | [详情](../t2t/papers/2603.13026_pismith.md) |
| FlipAttack | [2410.02832](https://arxiv.org/abs/2410.02832) | 攻击 | 利用 LLM 自回归特性，1 次查询 ASR 约 98% | [详情](../t2t/papers/2410.02832_flipattack.md) |
| Paper Summary Attack | [2507.13474](https://arxiv.org/abs/2507.13474) | 攻击 | 利用 LLM 对权威来源的信任倾向 | [详情](../t2t/papers/2507.13474_paper_summary_attack.md) |
| InfoFlood | [2506.12274](https://arxiv.org/abs/2506.12274) | 攻击 | 通过信息过载淹没安全注意力机制 | [详情](../t2t/papers/2506.12274_infoflood.md) |
| DOOR | [2503.03710](https://arxiv.org/abs/2503.03710) | 防御 | 双重优化目标，同时提升安全性和任务效用 | [详情](../t2t/papers/2503.03710_door.md) |

---

[← 返回主目录](../../README.md)
