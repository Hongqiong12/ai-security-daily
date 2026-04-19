# AI 安全每日情报调研与推送 - 全模态自动化流水线

> **版本**: v2.1 | **创建日期**: 2026-03-24 | **最后更新**: 2026-04-17
>
> **关注领域**: Text-to-Image (T2I) · Multimodal-to-Image (T+I2I) · Text-to-Text (T2T) · Agentic Search
>
> **执行时间**: 每日 08:00 (北京时间) | 频率: FREQ=DAILY
>
> **数据来源**: ArXiv cs.CR / cs.CL / cs.LG / cs.CV（过去 7 天）
>
> **执行前置**: 强制加载 `paper-research` + `pua`；执行结束后必须回写 automation memory 与 `.workbuddy/memory/`

---

## 一、任务概述

本自动化任务重点追踪和整理 **文生图(T2I)** 与 **文图生图(T+I2I)** 领域的 AI 安全对齐与评测研究，辅以 T2T 和 Agentic Search 模态，每日自动执行以下全链路流程。

### 1.1 任务目标

| 模态 | 英文名称 | 中文名称 | 研究重点 |
|------|----------|----------|----------|
| **T2I & T+I2I** | Text-to-Image / Multimodal-to-Image | 文生图/文图生图 | **【核心重点】** 安全对齐、概念擦除/对抗、内容安全过滤(NSFW脱敏)、越狱攻击、多模态安全Benchmark |
| **T2T** | Text-to-Text | 文生文 | LLM 越狱攻击、提示注入、机制可解释性 (当前降维关注) |
| **Agentic** | Agentic Search | Agent 安全 | 技能供应链投毒、工具劫持、Agent 基准评测 (当前降维关注) |

### 1.2 论文分类体系

每个模态下包含子类别：

- **papers/** — 所有论文的 6 模块深度精读文档，也是精确计数的唯一文件源
- **attack/** — 攻击侧代表性索引与专题导航
- **defense/** — 防御侧代表性索引与专题导航
- **benchmark/** — 基础评测集、基准测试论文索引（**动态回填，每次新增 Benchmark 类论文时追加**）
- `attack/defense/benchmark/` 主要承担导航与专题归档；真正的论文正文统一存放在 `papers/`

### 1.3 输出产物

| 产物 | 存储位置 | 说明 |
|------|----------|------|
| 每日深度情报报告 | `daily-reports/YYYY-MM/YYYY-MM-DD_AI安全每日深度情报.md` | 综合报告（三模态合并） |
| T2T 精读文档 | `categories/t2t/papers/arxiv_id_slug.md` | 六大模块深度解读（如 `2604.15149_rlvr_hacking.md`） |
| T2I 精读文档 | `categories/t2i/papers/arxiv_id_slug.md` | 六大模块深度解读（如 `2604.15166_damp.md`） |
| Agentic 精读文档 | `categories/agentic-search/papers/arxiv_id_slug.md` | 六大模块深度解读（如 `2604.15022_r2a.md`） |
| T2T Survey | `insights/t2t-survey.md` | T2T 攻防全景（增量更新） |
| T2I Survey | `insights/t2i-survey.md` | T2I 安全七年演进（增量更新） |
| Agentic Survey | `insights/agentic-search-survey.md` | Agent 攻防全景（增量更新） |
| 总览洞察 | `insights/AI_Security_Landscape_2026.md` | 宏观格局分析（条件触发） |
| 元数据锚点 | `_meta.json` | 统一数据源（每次执行必更） |

---

## 二、每日执行流程（8 步闭环）

### 2.1 执行时间线

```
08:00 (北京时间) ──┬── 触发自动化任务
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: 情报搜索                                             │
│ - 加载 paper-research + pua 获取标准 SOP 与防摆烂闭环         │
│ - 搜索 ArXiv 近 7 天 T2T/T2I/Agentic 安全论文                │
│ - 筛选 4-8 篇高价值目标（排除已收录）                          │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: 深度解析 (6-模块精读)                                 │
│ - 对每篇论文强制执行 6 模块精读：                              │
│   ① 背景与动机 ② 核心方法 ③ 技术细节                        │
│   ④ 实验与结果 ⑤ 局限性 ⑥ 复现指南                          │
│ - 存入 categories/{modality}/papers/                         │
│ - 严禁仅搬运摘要                                              │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 每日报告生成                                         │
│ - 生成 daily-reports/YYYY-MM/YYYY-MM-DD_*.md                │
│ - 包含：今日概览 + 每篇精读摘要 + 趋势信号                    │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Survey 沉淀                                          │
│ - 判断是否存在"新型攻击/防御范式"                             │
│ - 若存在 → 增量更新 insights/{modality}-survey.md            │
│   → 追加条目至对应分类表格                                    │
│   → 刷新文档顶部的修改日期和版本号                            │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: 门面闭环 & 一致性校验 ⭐                              │
│                                                              │
│ 5.1 README.md 同步                                           │
│   [ ] 论文总数 = search_file 精确扫描各 papers/*.md 的文件数    │
│   [ ] Last Update = 今日日期                                  │
│   [ ] 今日报告链接 = 最新 daily-report                        │
│   [ ] Featured Papers = 今日最高价值论文                      │
│                                                              │
│ 5.2 数据一致性交叉验证（必须全部通过才可提交）                 │
│   [ ] README 徽章数字 === T2T数 + T2I数 + Agentic数           │
│   [ ] Survey 数据基础行 === 对应 papers/ 文件数               │
│   [ ] Landscape 数据源 === 全部 papers/ 文件数之和             │
│   [ ] _meta.json.paper_counts === 文件系统实际值               │
│   [ ] 如不一致 → 以 search_file 扫描结果为准，统一修正          │
│                                                              │
│ 5.3 Landscape 更新触发检查                                   │
│   满足以下任一条件 → 必须增量更新 Landscape_2026：             │
│   [ ] 发现"新型攻击/防御范式"                                 │
│   [ ] 单日收录 ≥ 5 篇                                        │
│   [ ] 距上次 Landscape 更新超过 7 天                          │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 6: 总结性文档同步 ⭐ 新增                                │
│                                                              │
│ 6.1 Benchmark 索引回填                                       │
│   对每篇新收录论文，判断是否属于 Benchmark/评测类：            │
│   若是 → 追加至 categories/{modality}/benchmark/README.md    │
│   格式遵循已有表格列规范                                      │
│                                                              │
│ 6.2 总览洞察增量更新（同 5.3 触发条件）                       │
│   [ ] 刷新「数据来源」中的论文总数                            │
│   [ ] 在对应模态章节追加最新趋势段落                          │
│   [ ] 更新「前沿趋势」章节的最新信号                          │
│   [ ] 刷新文档底部统计行                                      │
│                                                              │
│ 6.3 _meta.json 更新                                          │
│   [ ] last_updated = 今天                                    │
│   [ ] paper_counts = 各模态精确文件计数                      │
│   [ ] survey_versions = 各 Survey 当前状态                   │
│   [ ] daily_reports.latest = 今日日期                        │
│   [ ] missing_dates = 检测断档                               │
│                                                              │
│ 6.4 WORKFLOW.md 月初自同步                                   │
│   [ ] 若今天是每月 1 日：核对路径结构、模态列表与当前 Prompt   │
│   [ ] 若目录或流程已变化：同步更新本文档头部版本与目录结构     │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 7: 交付校验 & Git 推送 ⭐                                │
│                                                              │
│ 7.1 质量门禁                                                 │
│   [ ] 所有新论文精读包含完整 6 模块                           │
│   [ ] 所有 arXiv 链接有效                                     │
│   [ ] 数据一致性校验通过（Step 5.2 全部打勾）                │
│                                                              │
│ 7.2 Git 操作                                                 │
│   git add -A && git commit -m "YYYY-MM-DD: N papers ..."     │
│   git push origin main                                       │
│   [ ] 必须读取 push 结果确认成功                              │
│   [ ] 如果 push 失败 → 不结束任务 → 重试最多 3 次             │
│                                                              │
│ 7.3 失败兜底                                                 │
│   如果发现输出未遵守 6 模块格式或数据不一致：                  │
│   → 触发自我反思 → 补救重试 → 直到通过校验                    │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 8: 记忆回写 & 月度自校准 ⭐                               │
│ - 追加 `.codebuddy/automations/.../memory.md` 执行摘要       │
│ - 追加 `.workbuddy/memory/YYYY-MM-DD.md` 持久化结果           │
│ - 如为每月 1 日：同步检查并更新 WORKFLOW.md 与目录结构说明     │
│ - 回传主日报 / Survey / _meta.json 等核心交付物               │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
              ✅ 任务完成
```

---

## 三、ArXiv 检索策略

### 3.1 T2T 检索关键词

```
# 攻击类
jailbreak OR "prompt injection" OR "adversarial prompt" OR "red teaming"
OR "backdoor" OR "chain-of-thought attack" OR "CoT hijack"
OR "alignment attack" OR "ablation" OR "uncensor"

# 防御类
"safe alignment" OR "content filter" OR "defense" OR "mitigation"
OR "robustness" OR "safety monitor" OR "circuit analysis"
OR "mechanistic interpretability"

# 评测类
benchmark OR evaluation OR dataset OR "red team benchmark"
```

### 3.2 T2I & T+I2I 检索关键词 (核心优先)

```
# 攻击类
("text-to-image" OR "multimodal-to-image" OR "vision-language" OR "image generation") 
AND (jailbreak OR "adversarial" OR "prompt injection" OR backdoor OR "concept erasure attack" OR "bypassing")

# 防御与对齐类 (重点)
("text-to-image" OR "multimodal-to-image" OR "diffusion") 
AND ("safety alignment" OR "concept erase" OR "concept ablation" OR "safety filter" OR "content moderation" OR "NSFW" OR "safe generation" OR "red teaming")

# 评测类 (重点)
("text-to-image" OR "multimodal-to-image" OR "diffusion")
AND (benchmark OR evaluation OR "safety benchmark" OR "image safety dataset" OR "red team benchmark")
```

### 3.3 Agentic Search 检索关键词

```
# 攻击类
"agentic" AND (attack OR "prompt injection" OR poisoning OR "tool hijack"
OR "supply chain" OR "skill injection" OR "indirect injection")

# 防御类
"agent" AND (security OR defense OR "guard" OR "sandbox" OR "permission")
OR "tool use" AND (safety OR verification)

# 评测类
"agent" AND (benchmark OR evaluation OR "red team" OR "security eval")
```

### 3.4 目标 ArXiv 分类

| 分类 | 名称 | 重点关注 |
|------|------|----------|
| cs.CR | 计算机安全与加密 | 核心安全论文 |
| cs.CL | 计算语言学 | LLM 安全、对齐 |
| cs.LG | 机器学习 | 通用安全机制 |
| cs.CV | 计算机视觉 | T2I / VLM 安全 |

---

## 四、目录结构（当前实际结构）

```
ai-security-daily/
├── README.md                          ← 项目主页（自动更新徽章+链接）
├── WORKFLOW.md                        ← 本文档（自动化 SOP）
├── _meta.json                         ← 元数据锚点（统一数据源）
├── LICENSE
├── assets/                            ← 静态资源目录（当前为空）
├── fetch_arxiv.py                     ← ArXiv 搜索脚本
├── generate_papers.py                 ← 论文生成脚本
├── process_papers.py                  ← 论文处理脚本
├── update_surveys.py                  ← Survey 更新脚本
├── selected_papers.json               ← 已筛选论文记录
├── categories/
│   ├── t2t/
│   │   ├── attack/
│   │   ├── defense/
│   │   ├── benchmark/
│   │   ├── papers/                    ← 84 篇 6 模块精读
│   │   └── README.md
│   ├── t2i/
│   │   ├── attack/
│   │   ├── defense/
│   │   ├── benchmark/
│   │   ├── papers/                    ← 65 篇 6 模块精读
│   │   └── README.md
│   ├── agentic-search/
│   │   ├── attack/
│   │   ├── defense/
│   │   ├── benchmark/
│   │   ├── papers/                    ← 25 篇 6 模块精读
│   │   └── README.md
│   ├── i2i/                           ← 早期扩展模态
│   ├── i2t/                           ← 早期扩展模态
│   ├── i2v/                           ← 早期扩展模态
│   └── t2v/                           ← 早期扩展模态
├── daily-reports/
│   └── 2026-04/                       ← 本月日报
│       └── *_AI安全每日深度情报.md
├── insights/                          ← Survey & 洞察
│   ├── t2t-survey.md
│   ├── t2i-survey.md
│   ├── agentic-search-survey.md
│   ├── AI_Security_Landscape_2026.md  ← 总览洞察（条件触发更新）
│   └── alignment-paradigm-shift-abliteration.md
└── scripts/
```

---

## 五、质量控制清单

### 5.1 论文收录检查

- [ ] arXiv ID 是否已存在（去重，对比 selected_papers.json）
- [ ] arXiv 链接 HTTP 200
- [ ] GitHub 链接可访问（如果提供）
- [ ] 作者列表与原文一致

### 5.2 内容质量检查

- [ ] 包含六大模块（背景/方法/细节/实验/局限/复现）
- [ ] 数学公式使用 Unicode 格式
- [ ] 无 Markdown 链接语法（纯文本 URL）
- [ ] 表格格式正确
- [ ] **严禁搬运摘要**——必须有自己的分析解读

### 5.3 数据一致性校验（Step 5.2 核心）

这是 **v2.0 新增的关键防线**：

```python
# 伪代码：自动化必须执行的精确计数
counts = {
    "t2t": count_files("categories/t2t/papers/*.md"),
    "t2i": count_files("categories/t2i/papers/*.md"),
    "agentic": count_files("categories/agentic-search/papers/*.md"),
}
total = counts["t2t"] + counts["t2i"] + counts["agentic"]

# 必须确保以下位置一致：
assert README_badge == total
assert t2t_survey_count == counts["t2t"]
assert t2i_survey_count == counts["t2i"]
assert agentic_survey_count == counts["agentic"]
assert landscape_total == total
assert _meta_json_total == total
```

### 5.4 发布后检查

- [ ] GitHub commit 成功（含 hash）
- [ ] Push to origin main 成功（读取控制台输出确认）
- [ ] _meta.json 已更新
- [ ] 所有总结性文档已同步

---

## 六、已知问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 总结性文档不更新 | 自动化 Prompt 缺少同步指令 | v2.0 增加 Step 6（Benchmark 回填 + Landscape 更新） |
| 论文计数漂移 | 无统一数据源，靠 Agent 估计 | v2.0 引入 `_meta.json` 锚点 + Step 5.2 强制精确扫描 |
| Benchmark 目录僵死 | 只初始化从未回填 | v2.0 Step 6.1：新收录 Benchmark 类论文自动追加 |
| WORKFLOW 与实际脱节 | 未随架构变更同步更新 | v2.1 增加月初自同步规则，并按真实目录/命名规范刷新本文档 |
| Landscape 过期 | 缺乏触发机制 | v2.0 设定 3 条自动触发规则（新范式 / ≥5篇 / 超7天） |
| Push 失败无兜底 | 未捕获错误即结束 | v2.0 Step 7.2/7.3：必读 push 结果，失败重试 3 次 |

---

## 七、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v2.1** | 2026-04-17 | 修复 README/WORKFLOW 对齐问题：刷新真实目录结构与论文计数、改正 `arxiv_id_slug.md` 命名规范、补入 Step 8（记忆回写与月度自校准）、增加 `paper-research` + `pua` 执行前置 |
| v2.0 | 2026-04-14 | **重大重构**: 新增 Step 6(总结性文档同步) + Step 5.2(精确计数校验) + _meta.json + Agentic 模态 + Benchmark 动态回填 + Landscape 自动触发 |
| v1.0 | 2026-03-24 | 初始版：T2T+T2I 双轨，6 步流程，基础 QC 清单 |

---

*本文档由自动化任务维护 | 版本: v2.1 | 最后更新: 2026-04-17*
