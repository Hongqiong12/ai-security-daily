# T2I 安全 Benchmark 短名单（2026 年前高引用版）

> **整理日期**: 2026-04-22
> **目的**: 给 T2I / 视觉安全研究快速定位 2026 年前最值得优先读的 benchmark 论文。
> **引用口径**: OpenAlex 于 2026-04-22 查询的 `cited_by_count` 快照，仅作相对热度参考，不等同于 Google Scholar 实时值。

---

## 1. 结论先行

如果只看 **严格意义上的 T2I 安全专项 benchmark**，2026 年前最值得优先看的核心论文是：

1. **UnsafeBench (2024)** —— 更偏生成后图像审核 / 安全分类器评测
2. **T2ISafety (2025)** —— 更偏 T2I 模型端的综合安全评测（fairness / toxicity / privacy）

如果把 **包含安全维度的广义 T2I benchmark** 也纳入，那么 2026 年前更高引用、也更常被相关工作提及的代表还包括：

3. **HRS-Bench (2023)** —— 综合 T2I benchmark，引用量最高
4. **HEIM / Holistic Evaluation (2023)** —— 综合评测框架，显式覆盖 bias / toxicity / fairness / robustness 等安全相关维度

---

## 2. 短名单表格

| 论文 | 年份 | 类型定位 | 约被引次数* | 为什么值得看 |
|------|------|----------|-------------|--------------|
| **HRS-Bench: Holistic, Reliable and Scalable Benchmark for Text-to-Image Models** | 2023 | 广义 T2I benchmark（综合评测） | **45** | 2026 年前这条线里最接近“高引 benchmark 支点”的工作，适合做综述与 benchmark 章节入口。 |
| **Holistic Evaluation of Text-to-Image Models (HEIM)** | 2023 | 广义 T2I benchmark（综合评测） | **13** | 把 quality、alignment 与 bias / toxicity / fairness / robustness 放进统一评测框架，是“能力评测+安全维度”融合的代表。 |
| **UnsafeBench: Benchmarking Image Safety Classifiers on Real-World and AI-Generated Images** | 2024 | 严格安全专项 benchmark | **4** | 直接评 image safety classifier 在真实图像与 AI 图像上的有效性，是“生成后审核”安全链路的代表基准。 |
| **T2ISafety: Benchmark for Assessing Fairness, Toxicity, and Privacy in Image Generation** | 2025 | 严格安全专项 benchmark | **4** | 直接面向 T2I safety，系统覆盖 fairness / toxicity / privacy 三条线，是目前最像“正统 T2I 安全 benchmark”的工作。 |

\* 引用次数为 OpenAlex 2026-04-22 快照，用于横向比较，不保证与其他学术平台完全一致。

---

## 3. 严格安全专项 vs 广义 benchmark：不要混写

### 3.1 严格安全专项 benchmark
这类论文的核心目标就是评安全风险本身，例如：
- unsafe image moderation 是否有效
- fairness / toxicity / privacy 是否过关
- 模型或安全分类器在对抗场景里会不会失守

对应代表：
- **UnsafeBench**
- **T2ISafety**

### 3.2 包含安全维度的广义 T2I benchmark
这类论文不是“只评安全”，而是把安全作为综合评测的一部分：
- image quality
- text-image alignment
- reasoning
- efficiency
- bias / toxicity / fairness / robustness

对应代表：
- **HRS-Bench**
- **HEIM**

在写综述或 related work 时，建议显式标注这两类 benchmark 的边界，避免把“综合评测”与“安全专项评测”混成一个桶。

---

## 4. 一个必须排除的易混淆项

### JailbreakBench 不属于 T2I benchmark
尽管它名字里有 benchmark，也常被误引到多模态/生成安全语境里，但 **JailbreakBench** 的标题和对象都很明确：

- 题目：**JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models**
- 对象：**LLM jailbreak**
- 结论：**不应计入 T2I benchmark 短名单**

如果要在 T2I 材料里提到它，最多只能作为“邻域参考”或“方法论启发”，不能写成 T2I benchmark 代表作。

---

## 5. 推荐引用话术（可直接复用）

> 截至 2026 年前，T2I 安全 benchmark 仍处于早期阶段。严格意义上的安全专项 benchmark 主要包括 UnsafeBench（2024）与 T2ISafety（2025）；若将包含 bias / toxicity / fairness / robustness 的综合评测框架纳入，则 HRS-Bench（2023）与 HEIM（2023）是更高引用、也更常被讨论的代表性工作。

---

## 6. 原始链接

- HRS-Bench: https://arxiv.org/abs/2304.05390
- HEIM: https://arxiv.org/abs/2311.04287
- UnsafeBench: https://arxiv.org/abs/2405.03486
- T2ISafety: https://arxiv.org/abs/2501.12612
