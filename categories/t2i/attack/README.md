# 🎨 文生图 - 攻击类

文生图模型的越狱攻击、提示注入、后门攻击等安全威胁研究。

## 📋 论文列表

### 🚀 2025-2026 最新研究

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **Reason2Attack** | 2026 | AAAI | 利用LLM推理能力进行越狱攻击 | [📄](./papers/2503.17987_reason2attack.md) |
| **JailLLM** | 2025 | EACL | 利用微调LLM生成T2I越狱提示 | [📄](./papers/2503.01839_jailbreaking_via_llm.md) |
| **GenBreak** | 2025 | arXiv | LLM驱动的T2I红队测试框架 | [📄](./papers/2506.10047_genbreak.md) |
| **Modifier Unlocked** | 2025 | IEEE S&P | 通过修饰符机制绕过安全过滤 | [📄](./papers/11023413_modifier_unlocked.md) |
| **JailFuzzer** | 2025 | IEEE S&P | LLM智能体驱动的自动化越狱测试 | [📄](./papers/2408.00523_jailfuzzer.md) |
| **DiffZOO** | 2025 | NAACL | 零阶优化的纯黑盒越狱攻击 | [📄](./papers/2408.11071_diffzoo.md) |

### 🔐 经典攻击论文

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **SneakyPrompt** | 2024 | IEEE S&P | 首个自动化越狱T2I模型，绕过DALL·E 2和Stable Diffusion安全过滤器 | [📄](./papers/2305.12082_sneakyprompt.md) |
| **ART** | 2024 | NeurIPS | 自动红队测试保护良性用户，VLM+LLM协同 | [📄](./papers/2405.19360_art.md) |
| **UPAM** | 2024 | ICML | 统一提示攻击同时绕过文本和视觉检查器，SPL支持黑盒 | [📄](./papers/2405.11336_upam.md) |
| **FLIRT** | 2024 | EMNLP | 反馈循环上下文红队测试，上下文学习生成对抗提示 | [📄](./papers/2308.04265_flirt.md) |
| **MMA-Diffusion** | 2024 | CVPR | 多模态攻击扩散模型，文本+图像协同绕过 | [📄](./papers/2311.17516_mma_diffusion.md) |
| **Perception-guided Jailbreak** | 2024 | AAAI | 感知引导的越狱攻击，LLM识别语义相似安全词 | [📄](./papers/2408.10848_perception_jailbreak.md) |
| **Divide-and-Conquer** | 2024 | arXiv | 利用LLM能力绕过安全过滤 | - |
| **SurrogatePrompt** | 2024 | ACM CCS | 通过替代绕过安全过滤 | - |

### 🐛 后门攻击

| 论文 | 年份 | 会议 | 核心创新 | 详情 |
|------|------|------|----------|------|
| **EvilEdit** | 2024 | ACM MM | 一秒内植入后门的T2I模型攻击 | - |
| **Backdoor Detection (DAA)** | 2025 | TPAMI | 动态注意力分析后门检测 | [📄](./papers/2504.20518_dynamic_attention_backdoor.md) |

---

## 📊 攻击类型分类

### 越狱攻击 (Jailbreak)
- 利用对抗提示绕过安全过滤器
- LLM辅助的越狱提示生成
- 自动化红队测试框架

### 后门攻击 (Backdoor)
- 在训练阶段植入隐蔽触发器
- 一旦激活生成预定义有害内容
- 检测与防御研究

### 版权攻击 (Copyright)
- 生成受版权保护的角色/内容
- 绕过版权保护机制

### 偏见放大 (Bias Amplification)
- 强化刻板印象
- 歧视性内容生成

---

[← 返回文生图目录](../README.md) | [← 返回主目录](../../README.md)
