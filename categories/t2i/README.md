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

## 📋 最新论文 (2025)

### 🔴 攻击类

- **Reason2Attack** (AAAI 2026) - LLM推理驱动的越狱攻击
- **JailLLM** (EACL 2026) - 微调LLM生成越狱提示
- **GenBreak** (arXiv 2025) - LLM红队测试框架
- **Modifier Unlocked** (IEEE S&P 2025) - 修饰符机制漏洞
- **JailFuzzer** (IEEE S&P 2025) - 自动化越狱测试
- **DiffZOO** (NAACL 2025) - 零阶优化黑盒攻击

### 🟢 防御类

- **SPEED** (arXiv 2025) - 高效概念擦除
- **TRCE** (ICCV 2025) - 可靠恶意概念擦除
- **Concept Pinpoint Eraser** (ICLR 2025) - 精准概念移除
- **SafeGuider** (ACM CCS 2025) - 内容安全控制
- **SAFREE** (ICLR 2025) - 无训练安全守卫

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

[← 返回主目录](../README.md)
