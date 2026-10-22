# SafetyBPO: Bidirectional Preference Optimization for Safe Text-to-Image Generation

**论文主页**: https://openaccess.thecvf.com/content/CVPR2026F/html/Wu_SafetyBPO_Bidirectional_Preference_Optimization_for_Safe_Text-to-Image_Generation_CVPRF_2026_paper.html
**领域**: CVPR 2026 Findings / T2I Safety Alignment
**作者**: You Wu, Beier Zhu, Chi Zhang
**机构**: Westlake AGI Lab（以代码仓库与项目命名为准）
**发布日期**: 2026-06（CVPR 2026 Findings）
**分类**: defense
**GitHub**: https://github.com/Westlake-AGI-Lab/SafetyBPO

---

## 一、背景与问题

### 动机

T2I 安全领域里，很多 concept erasure 方法的真实问题不是“擦不掉”，而是**过拟合式遗忘**：一旦把危险概念压狠了，与之邻近但本来无害的语义也一起掉，这就是 over-forgetting。

### 核心科学问题

能否把 T2I 安全对齐重写成一种**偏好学习问题**：既偏好更安全的输出，又偏好对原始意图更保真的输出；并且把这种偏好同时放在 prompt 侧与 image 侧来学？

### 为什么这篇论文重要

SafetyBPO 是这批论文里**最直接命中你当前主线**的一篇。它明确提出：
- 用 LLM 把 unsafe prompt 重写成 **safe yet semantically consistent** 的版本；
- 再把这种 prompt-level preference 与 image-level preference 一起蒸馏进扩散模型；
- 最终目标不是简单拒绝，而是**安全地保留可用语义**。

---

## 二、核心方法

### （1）BPO-Bench：safe-unsafe preference pairs

作者先构建 **2.5K** 规模的高质量偏好对数据：
- 原始 unsafe prompt
- LLM 重写后的 safe prompt
- 对应安全 / 不安全图像偏好

这一步非常关键，因为它把“安全改写”从模糊工程经验，落成了可训练的 preference data。

### （2）双向偏好优化（Bidirectional Preference Optimization）

SafetyBPO 不只学一个“正向更安全”的目标，而是同时做两件事：
- 提升安全、语义一致输出的概率；
- 压低不安全或过度遗忘输出的概率。

### （3）双视角监督：prompt-level + image-level

这是它相对传统 concept erasure 最大的结构创新：
- **prompt-level**：unsafe prompt 如何被改写成安全但保真版本；
- **image-level**：生成结果是否真的既安全又保留多样性与 fidelity。

### （4）正负 guidance 模型协同

论文进一步把偏好信号蒸馏成：
- positive guidance model
- negative guidance model

让生成在采样时被同时“拉向安全保真区域、推离危险退化区域”。

---

## 三、技术细节

### SafetyBPO 真正解决了什么

它不是简单替代旧的概念擦除，而是把安全对齐问题拆成三层：
1. **unsafe prompt 如何被重写**；
2. **重写后哪些图像是更好的**；
3. **如何把二者统一进偏好优化过程**。

### 与当前业务的同构关系

如果翻译到你的输入侧 rewrite 任务，SafetyBPO 几乎对应：
- 原始高风险 prompt
- safe rewrite 候选
- 语义保持更好的 rewrite 作为 winner
- 过度改写或改不干净的 rewrite 作为 loser

也就是说，它已经给出了“safe rewrite dataset 应该长什么样”的近似答案。

### 训练自由版的意义

论文一个很强的信号是：
- 即便**不训练新模型**，只靠 prompt rewriting + classifier-free guided sampling，也能取得强结果；
- 这说明输入侧改写本身就不是纯辅助组件，而是可以成为第一层主控制面。

### 官方仓库给出的评测接口

代码仓库公开了三类评测：
- **InPro**：有害内容抑制
- **FID**：图像保真
- **CLIP**：文本对齐

这非常贴近你要的三维评测骨架。

---

## 四、实验设置与结果

### 论文公开的关键信号

从论文摘要、项目页和仓库可以确认的硬信息包括：
- **BPO-Bench = 2.5K** 高质量 safe-unsafe preference pairs；
- 训练自由版已经能在多项 unlearning benchmark 上达到 **SOTA**；
- 完整训练版进一步在安全、fidelity、diversity 之间取得更优平衡；
- 评测显式覆盖 InPro / FID / CLIP 三个方向。

### 论文最有价值的结果解读

虽然公开页面没有给出一张最浓缩的单表 headline number，但它释放了几个更重要的结构性结论：
1. **prompt rewriting 本身就是有效安全控制手段**；
2. **只做 rigid suppression 很容易 over-forgetting**；
3. **prompt preference 与 image preference 联合建模，比单边监督更稳**。

### 对当前业务的直接启发

对你来说，SafetyBPO 的可迁移价值主要不在“把它整套训出来”，而在三件事：
- 学它的数据格式：safe / unsafe pair 不是单句重写，而是配套图像偏好；
- 学它的监督粒度：prompt 侧和 image 侧都要看；
- 学它的评测接口：至少同时测风险抑制、文本对齐、图像保真。

---

## 五、局限性分析

1. **公开页面缺少最细实验表**：需要结合 PDF / 补充材料进一步读数。  
2. **核心仍偏模型侧安全对齐**：并非专门为在线 rewrite service 设计。  
3. **2.5K 数据规模对大模型仍不算大**：泛化上限可能受限。  
4. **目前主要针对 unsafe concept removal**：对灰区、模糊、高上下文依赖风险仍需更多验证。  
5. **工业部署还差一层在线路由**：何时 rewrite、何时拒绝、何时走生成侧控制，论文没有完整展开。

---

## 六、复现指南

### 环境依赖

```bash
pip install -r requirements.txt
bash train.sh
```

### 最小复现步骤

1. 构建 unsafe prompt 与 safe rewrite 的配对数据。  
2. 为每个 pair 准备图像级偏好结果。  
3. 分别训练 positive / negative guidance。  
4. 用 InPro、FID、CLIP 统一评测。  
5. 额外检查训练自由版与训练版的 trade-off 差异。

### 对当前业务的最小迁移版本

如果今天只能迁一件事，我建议直接迁它的**pair 数据设计**：
- 原始 prompt
- 安全重写 prompt
- winner image / loser image
- 风险下降 / 语义保持 / 指令遵循的理由标签

这会比只存“改写文本 + 人工主观评价”更有训练价值。
