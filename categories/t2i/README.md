# 🎨 Text-to-Image (文生图) 安全研究

文本到图像生成模型（如 DALL-E、Stable Diffusion、Midjourney 等）的安全论文汇总。

## 📁 目录结构

| 子类别 | 说明 | 论文数 |
|--------|------|--------|
| [benchmark](./benchmark/) | 基础综述、安全评测基准 | 10+ 篇 |
| [attack](./attack/) | 越狱攻击、后门攻击、版权攻击等 | 20+ 篇 |
| [defense](./defense/) | 概念擦除、安全过滤、水印保护等 | 25+ 篇 |
| [papers](./papers/) | 详细论文分析 | 15+ 篇 |

## 🎯 研究方向概览

### 攻击类型

| 攻击类型 | 描述 | 代表论文 |
|----------|------|----------|
| **越狱攻击** | 绕过安全过滤器生成有害内容 | SneakyPrompt, JailLLM, GenBreak |
| **后门攻击** | 在模型中植入隐蔽触发器 | EvilEdit, Backdoor Detection |
| **版权攻击** | 生成受版权保护的角色/内容 | - |
| **偏见攻击** | 放大刻板印象和歧视 | Asymmetric Bias |

### 防御类型

| 防御类型 | 描述 | 代表论文 |
|----------|------|----------|
| **概念擦除** | 移除模型中的不良概念 | ESD, SPEED, TRCE |
| **安全过滤** | 输入输出层的安全检查 | Latent Guard, GuardT2I |
| **水印保护** | 保护生成内容版权 | Watermarking Diffusion |
| **后门检测** | 识别模型中的后门 | DAA |

## 📋 最新论文 (2026-03)

### 🔴 2026-03-25 新增

| 论文 | ArXiv ID | 会议 | 核心贡献 | 详情 |
|------|----------|------|----------|------|
| **MacPrompt** | [2601.07141](https://arxiv.org/abs/2601.07141) | AAAI 2026 | 跨语言字符越狱，SD Safety Checker 绕过率 100% | [详情](./papers/2601.07141_macprompt.md) |

---

## 📋 已收录论文 (2025)

### 🔴 攻击类

| 论文 | ArXiv ID | 会议 | 核心贡献 | 详情 |
|------|----------|------|----------|------|
| **Reason2Attack** | [2503.17987](https://arxiv.org/abs/2503.17987) | AAAI 2026 | LLM推理驱动的越狱攻击 | [详情](./papers/2503.17987_reason2attack.md) |
| **JailLLM** | [2503.01839](https://arxiv.org/abs/2503.01839) | EACL 2026 | 微调LLM生成越狱提示 | [详情](./papers/2503.01839_jailbreaking_via_llm.md) |
| **GenBreak** | [2506.10047](https://arxiv.org/abs/2506.10047) | arXiv | LLM红队测试框架 | [详情](./papers/2506.10047_genbreak.md) |
| **Modifier Unlocked** | [1102.3413](https://arxiv.org/abs/1102.3413) | IEEE S&P | 修饰符机制漏洞 | [详情](./papers/11023413_modifier_unlocked.md) |
| **JailFuzzer** | [2408.00523](https://arxiv.org/abs/2408.00523) | IEEE S&P | 自动化越狱测试 | [详情](./papers/2408.00523_jailfuzzer.md) |
| **DiffZOO** | [2408.11071](https://arxiv.org/abs/2408.11071) | NAACL | 零阶优化黑盒攻击 | [详情](./papers/2408.11071_diffzoo.md) |
| **SneakyPrompt** | [2305.12082](https://arxiv.org/abs/2305.12082) | IEEE S&P | 强化学习越狱攻击 | [详情](./papers/2305.12082_sneakyprompt.md) |
| **Perception Jailbreak** | [2408.10848](https://arxiv.org/abs/2408.10848) | arXiv | 感知层越狱攻击 | [详情](./papers/2408.10848_perception_jailbreak.md) |
| **When Understanding Becomes a Risk** | [2603.24079](https://arxiv.org/abs/2603.24079) | CVPR 2026 | MLLM 图像生成安全风险评估 | [详情](./papers/2603.24079_mllm_safety_risk.md) |

### 🟢 防御类

| 论文 | ArXiv ID | 会议 | 核心贡献 | 详情 |
|------|----------|------|----------|------|
| **SPEED** | [2503.07392](https://arxiv.org/abs/2503.07392) | arXiv | 高效概念擦除 | [详情](./papers/2503.07392_speed.md) |
| **TRCE** | [2503.07389](https://arxiv.org/abs/2503.07389) | ICCV | 可靠恶意概念擦除 | [详情](./papers/2503.07389_trce.md) |
| **Concept Pinpoint Eraser** | [2506.22806](https://arxiv.org/abs/2506.22806) | ICLR | 精准概念移除 | [详情](./papers/2506.22806_concept_pinpoint_eraser.md) |
| **SafeGuider** | [2510.05173](https://arxiv.org/abs/2510.05173) | ACM CCS | 内容安全控制 | [详情](./papers/2510.05173_safeguider.md) |
| **SAFREE** | [2410.12761](https://arxiv.org/abs/2410.12761) | arXiv | 无训练安全守卫 | [详情](./papers/2410.12761_safree.md) |
| **Z-Erase** | [2603.25074](https://arxiv.org/abs/2603.25074) | arXiv | 单流扩散 Transformer 概念擦除 | [详情](./papers/2603.25074_z_erase.md) |

## 📊 数据统计

```
t2i 类目论文统计 (截至 2026-03)
├── benchmark:  10+ 篇
├── attack:     20+ 篇
├── defense:    25+ 篇
└── 总计:       55+ 篇
```

## 🔗 外部资源

- [Awesome-AD-on-T2IDM](https://github.com/datar001/Awesome-AD-on-T2IDM) - T2I对抗攻防资源汇总
- [Awesome-MLLM-Safety](https://github.com/isXinLiu/Awesome-MLLM-Safety) - 多模态LLM安全资源

---

[← 返回主目录](../../README.md)
