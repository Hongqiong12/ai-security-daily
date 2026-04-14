# 📝 文生文 (Text-to-Text)

文本到文本的 LLM（如 GPT、Claude、LLaMA 等）相关安全论文。

| 子类别 | 说明 |
|--------|------|
| [benchmark](./benchmark/) | 基础评测集、基准测试 |
| [attack](./attack/) | 攻击类：越狱、提示注入、对抗样本等 |
| [defense](./defense/) | 防御类：安全对齐、越狱防御等 |

## 📋 论文列表

### 2026-04-14

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| Critical-CoT | [2604.10681](https://arxiv.org/abs/2604.10681) | 防御 | 用 CTCoT + SFT + DPO 同时防 ICL/FT 型推理层后门，ASRr 压到 1% 以下 | [详情](./papers/2604.10681_critical_cot.md) |
| Nullspace Steering | [2604.10326](https://arxiv.org/abs/2604.10326) | 攻击 | KL 归因 + 写路径静音 + 零空间注入的白盒机制级越狱，ACQ≈2 | [详情](./papers/2604.10326_nullspace_steering.md) |

---

### 2026-03-28（补充）

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| Cognitive Firewall | [2603.23791](https://arxiv.org/abs/2603.23791) | 防御 | 边缘-云分割计算三层防御，浏览器代理 ASR < 1%，延迟优势~17000× | [详情](./papers/2603.23791_cognitive_firewall.md) |
| LLMSE SEO Attack | [2603.25500](https://arxiv.org/abs/2603.25500) | 基准 | SEO-Bench 首次评估 LLMSE 安全性，LLMSEO 攻击将操纵率提升~2× | [详情](./papers/2603.25500_llmse_seo_attack.md) |
| Near-Verbatim Extraction | [2603.24917](https://arxiv.org/abs/2603.24917) | 基准 | 解码约束束搜索以~20采样当量估计近逐字提取风险确定性下界 | [详情](./papers/2603.24917_near_verbatim_extraction.md) |

---

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

### 2026-03-31

| 论文 | ArXiv | 类别 | 核心创新 | 详情 |
|------|-------|------|----------|------|
| Steganographic Canaries | [2603.28655](https://arxiv.org/abs/2603.28655) | 防御 | 隐写标记文件框架，混合模式Tier 3对抗下97%恢复率，拦截LLM勒索软件 | [详情](./papers/2603.28655_steganographic_canaries_llm.md) |
| Kill-Chain Canaries | [2603.28013](https://arxiv.org/abs/2603.28013) | 防御 | 四阶段攻击链追踪，Claude 0% ASR vs GPT-4o-mini 53% ASR | [详情](./papers/2603.28013_kill_chain_canaries.md) |
| SafetyDrift | [2603.27148](https://arxiv.org/abs/2603.27148) | 防御 | 吸收马尔可夫链预测代理违规，94.7%检测率，提前3.7步预警 | [详情](./papers/2603.27148_safetydrift.md) |
| MLLM Adversarial Survey | [2603.27918](https://arxiv.org/abs/2603.27918) | 基准 | 37页综合综述，TMLR接收，统一攻击分类法和漏洞中心分析 | [详情](./papers/2603.27918_mllm_adversarial_survey.md) |
| OpenClaw Taxonomy | [2603.27517](https://arxiv.org/abs/2603.27517) | 基准 | 190个漏洞双轴分类，发现完整RCE链和结构性弱点 | [详情](./papers/2603.27517_openclaw_taxonomy.md) |

---

[← 返回主目录](../../README.md)
