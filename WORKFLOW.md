# AI 安全每日情报调研与推送 - T2T & T2I 专项

> **版本**: v1.0 | **创建日期**: 2026-03-24 | **最后更新**: 2026-03-24
>
> **关注领域**: Text-to-Text (T2T) 大语言模型安全 + Text-to-Image (T2I) 文生图安全
>
> **执行时间**: 每日 00:00 (北京时间)
>
> **数据来源**: ArXiv cs.CR / cs.CL / cs.LG / cs.CV

---

## 一、任务概述

本自动化任务专注于追踪和整理 **T2T** 和 **T2I** 两个核心模态的 AI 安全研究，每日自动执行以下流程：

### 1.1 任务目标

| 模态 | 英文名称 | 中文名称 | 研究重点 |
|------|----------|----------|----------|
| **T2T** | Text-to-Text | 文生文 | LLM 越狱攻击、安全对齐、提示注入、防御机制 |
| **T2I** | Text-to-Image | 文生图 | T2I 越狱攻击、概念擦除、内容安全过滤、水印保护 |

### 1.2 论文分类体系

每个模态下包含三个子类别：

- **Benchmark**: 基础评测集、基准测试论文
- **Attack**: 攻击类论文（越狱攻击、提示注入、后门攻击等）
- **Defense**: 防御类论文（安全对齐、鲁棒性防御、概念擦除等）

### 1.3 输出产物

| 产物 | 存储位置 | 说明 |
|------|----------|------|
| 每日深度情报报告 | `communications/YYYY-MM/YYYY-MM-DD_AI安全每日深度情报.md` | 综合报告 |
| T2T 专项报告 | `ai-security-daily/daily-reports/t2t/YYYY-MM-DD_t2t_每日情报.md` | T2T 专项 |
| T2I 专项报告 | `ai-security-daily/daily-reports/t2i/YYYY-MM-DD_t2i_每日情报.md` | T2I 专项 |
| 论文详情文档 | `ai-security-daily/categories/t2t/papers/` 或 `t2i/papers/` | 六大模块深度解读 |
| 企业微信推送 | 企业微信文档 | 每日推送链接 |

---

## 二、每日执行流程

### 2.1 执行时间线

```
00:00 (北京时间) ──┬── 触发自动化任务
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 1: 数据采集                                             │
│ - 搜索 ArXiv cs.CR (计算机安全) 最新论文                     │
│ - 搜索 ArXiv cs.CL (计算语言学) 最新论文                     │
│ - 搜索 ArXiv cs.LG (机器学习) 最新论文                       │
│ - 搜索 ArXiv cs.CV (计算机视觉) 最新论文                     │
│ - 检索时间窗口: 过去 7 天                                    │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 2: T2T 论文筛选                                         │
│ - 关键词: jailbreak, prompt injection, LLM security,         │
│          alignment, red teaming, defense, attack              │
│ - 分类: benchmark / attack / defense                        │
│ - 去重: 检查是否已收录 (arXiv ID 对比)                       │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 3: T2I 论文筛选                                         │
│ - 关键词: text-to-image, diffusion safety, concept erase,   │
│          prompt injection, jailbreak, content filter        │
│ - 分类: benchmark / attack / defense                        │
│ - 去重: 检查是否已收录 (arXiv ID 对比)                      │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 4: 生成深度情报报告                                     │
│ - 综合报告: 合并 T2T + T2I                                    │
│ - 专项报告: T2T 独立 + T2I 独立                              │
│ - 论文详情: 每篇论文六大模块深度解读                         │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 5: 链接验证与质量检查                                   │
│ - arXiv 链接 HTTP 验证                                       │
│ - GitHub 链接有效性检查                                      │
│ - 作者信息核对 (与原文一致)                                  │
│ - 公式格式检查 (Unicode 数学符号)                            │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 步骤 6: 推送发布                                             │
│ - GitHub: daily-reports/ + 论文文档                         │
│ - 企业微信: 新建文档并推送链接                               │
│ - 本地: communications/ 目录                                 │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
              ✅ 任务完成
```

### 2.2 论文深度解读模板 (六大模块)

每篇论文必须包含以下六大模块：

```markdown
### [论文标题]

**《[英文标题]》**

arXiv: https://arxiv.org/abs/XXXX.XXXXX | 领域: cs.XX | 作者: XXX et al. | 发布: YYYY-MM-DD | GitHub: [链接或"暂无"]

#### 一、背景与问题
- 研究动机
- 核心科学问题
- 直觉洞见

#### 二、核心方法
- 主要技术贡献
- 方法框架图（文字描述）
- 关键设计理念

#### 三、技术细节
- 数学公式（Unicode 格式）
- 算法流程
- 关键参数设置

#### 四、实验设置与结果
- 数据集描述
- 评价指标
- 主要结果表格
- 消融实验
- 关键发现

#### 五、局限性分析
- 方法局限性
- 评估局限性
- 潜在改进方向

#### 六、复现指南
- 环境依赖
- 关键代码片段（伪代码）
- 复现步骤
- 预期结果
```

### 2.3 报告格式要求

| 项目 | 要求 |
|------|------|
| arXiv 链接 | 必须 HTTP 验证有效 |
| GitHub 链接 | 必须存在且可访问 |
| 作者信息 | 必须与原文一致 |
| 公式格式 | 使用 Unicode 数学符号（∇, ∈, ≠, ≤ 等）|
| 链接显示 | 纯文本可见 URL，不使用 Markdown 链接语法 |
| 报告语言 | 中文为主，关键术语保留英文 |
| 论文数量 | 每日 3-8 篇（控制深度而非数量）|

---

## 三、ArXiv 检索策略

### 3.1 T2T 检索关键词

```
# 攻击类
jailbreak OR "prompt injection" OR "adversarial attack" OR "red teaming" OR "backdoor attack"

# 防御类
"safe alignment" OR "content filter" OR "output审核" OR defense OR mitigation OR robustness

# 评测类
benchmark OR evaluation OR dataset
```

### 3.2 T2I 检索关键词

```
# 攻击类
"text-to-image" AND (jailbreak OR "prompt injection" OR "adversarial" OR attack)

# 防御类
"concept erase" OR "concept ablation" OR "safety filter" OR "content moderation" OR
"diffusion" AND (security OR protect OR guard)

# 评测类
benchmark OR evaluation
```

### 3.3 目标 ArXiv 分类

| 分类 | 名称 | 重点关注 |
|------|------|----------|
| cs.CR | 计算机安全与加密 | 核心安全论文 |
| cs.CL | 计算语言学 | LLM 安全、对齐 |
| cs.LG | 机器学习 | 通用安全机制 |
| cs.CV | 计算机视觉 | T2I 安全 |

---

## 四、目录结构

```
ai-security-daily/
├── README.md
├── LICENSE
├── WORKFLOW.md                          ← 本文档
├── assets/
├── categories/
│   ├── t2t/                             ← T2T 论文详情
│   │   ├── benchmark/
│   │   ├── attack/
│   │   ├── defense/
│   │   └── papers/
│   │       └── YYYYMMDD_arxivid_title.md
│   └── t2i/                             ← T2I 论文详情
│       ├── benchmark/
│       ├── attack/
│       ├── defense/
│       └── papers/
│           └── YYYYMMDD_arxivid_title.md
├── daily-reports/
│   ├── t2t/                            ← T2T 每日报告
│   │   └── 2026-03/
│   │       └── YYYY-MM-DD_t2t_每日情报.md
│   └── t2i/                            ← T2I 每日报告
│       └── 2026-03/
│           └── YYYY-MM-DD_t2i_每日情报.md
└── scripts/
```

---

## 五、质量控制清单

### 5.1 论文收录检查

- [ ] arXiv ID 是否已存在（去重）
- [ ] arXiv 链接 HTTP 200
- [ ] GitHub 链接可访问（如果提供）
- [ ] 作者列表与原文一致

### 5.2 内容质量检查

- [ ] 包含六大模块（背景/方法/细节/实验/局限/复现）
- [ ] 数学公式使用 Unicode 格式
- [ ] 无 Markdown 链接语法（纯文本 URL）
- [ ] 表格格式正确

### 5.3 发布检查

- [ ] GitHub commit 成功
- [ ] 企业微信文档创建成功
- [ ] 本地文件保存成功
- [ ] 索引文件更新

---

## 六、已知问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 报告未生成 | 自动化任务 PENDING_REVIEW | 手动触发并检查任务状态 |
| arXiv 404 | 链接格式错误 | 使用正确格式 `https://arxiv.org/abs/XXXXX` |
| 作者信息缺失 | 未读取原文 | 逐一核对 arXiv 原文 |
| 链接未验证 | 跳过验证步骤 | 必须 HTTP 验证所有链接 |

---

## 七、附录

### 7.1 Unicode 数学符号对照表

| 符号 | Unicode | 符号 | Unicode |
|------|---------|------|---------|
| ∇ | `U+2207` | ∈ | `U+2208` |
| ≠ | `U+2260` | ≤ | `U+2264` |
| ≥ | `U+2265` | × | `U+00D7` |
| ÷ | `U+00F7` | ∂ | `U+2202` |
| ∑ | `U+2211` | ∏ | `U+220F` |
| √ | `U+221A` | ∞ | `U+221E` |
| α | `U+03B1` | β | `U+03B2` |
| θ | `U+03B8` | λ | `U+03BB` |
| μ | `U+03BC` | σ | `U+03C3` |
| ⇒ | `U+21D2` | → | `U+2192` |
| ⇔ | `U+21D4` | ↔ | `U+2194` |

### 7.2 相关资源

- [ArXiv CS Rankings](https://arxiv.org/csbhtml/static/cs_ranking.html)
- [Awesome-MLLM-Safety](https://github.com/isXinLiu/Awesome-MLLM-Safety)
- [JailbreakBench](https://github.com/jailbreakbench/jailbreakbench)

---

*本文档由 AI 自动化任务维护 | 版本: v1.0 | 更新: 2026-03-24*
