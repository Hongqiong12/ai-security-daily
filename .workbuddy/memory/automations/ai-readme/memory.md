# 自动化执行记忆：T2I/T+I2I 工业安全每日调研

> 自动化标识: ai-readme | 依据: `WORKFLOW.md` v2.3 | 首次记录: 2026-10-22

---

## 执行历史

### 2026-10-23 ✅ 成功

- **检索**: arXiv **API 全面失败**（先 429 限流，退避后转 400 Bad Request，`all:diffusion` 也 400）→ 改用 `https://arxiv.org/search/?query=...&searchtype=all&order=-announced_date_first&size=200` **HTML 搜索页通道**。关键教训：**arXiv 简单搜索不支持 AND/OR 布尔组合**（返回 0 结果），必须用纯关键词串；宽查询 + 按 announced 日期倒序 + 本地日期过滤 + 关键词打分，效果优于窄查询。
- **收录**: 6 篇（T2I 4 / T2T 迁移 2，T2I 占比 66.7%）。
  - T2I: Mirage(2610.30348)、HealBench(2610.27516, AAAI'27)、IMPLICIT-Bench(2609.24228)、LogicVal(2610.24051)
  - 迁移: DiagSafe(2610.29225, **腾讯混元**×北师大)、AIMS(2606.27210, Adobe/NVIDIA)
- **本周主题判断**: T2I 输入侧改写**空窗**（138 篇 T2I 主题论文中无新改写方法），主线转到**归因工程**（锚点/审核器架构/判定标准/意图绑定）。
- **交付**: 主日报 + 6 篇六模块精读 + README/t2i-survey/t2t-survey/Landscape v3.4/两份 benchmark README/_meta.json/selected_papers.json 全量同步；commit c194ab1 已 push 成功。
- **计数**: T2T 102 / T2I 97 / Agentic 39 / Total 238（真实扫描，六处交叉校验一致）。

### 2026-10-22 ✅ 成功

- **检索**: 10 路 arXiv 查询（含 `submittedDate:[202610150000 TO 202610222359]` 日期过滤），去重后 157 篇；注意 arXiv API 有 429 限流，查询间隔需 ≥3.5s 并做 3–4 次重试。
- **收录**: 6 篇（T2I 4 / T2T 迁移 2 / Agentic 0，T2I 占比 66.7%）。
  - T2I: CSTI(2610.26452)、DSC(2610.21569)、SCOPE(2610.22264)、PPAA(2610.27719)
  - T2T 迁移: AMEND(2610.23183)、Policy Is Not Capability(2610.25060)
  - 候选观察（未做精读）: BEM(2610.24508)、Polarity Blindness(2610.27908)、HealBench(2610.27516)、TI2I CFG(2610.21550)
- **交付**: 主日报 + 6 篇六模块精读 + README/t2i-survey/t2t-survey/Landscape v3.3/T2I·T2T benchmark README/_meta.json/selected_papers.json 全量同步。
- **计数**: T2T 100 / T2I 93 / Agentic 39 / Total 232（真实扫描，已交叉校验一致）。

### 历史基线（来自 .workbuddy/memory 日志）

- 2026-06-24: 6 篇全 T2I（PixJail/VESFlow/ForceForget/SafetyBPO/PromptEnhancer/FaithRewriter），计数 226。
- 2026-04-30: 主线切换为 T2I 工业安全 + 业务对齐研究板块（WORKFLOW v2.3）。

---

## 稳定执行要点（下次直接复用）

0. **检索通道优先级（2026-10-23 新增，重要）**: 先试 API；若 API 返回 429 **或** 400（连 `all:diffusion` 都 400 说明端点整体不可用），立刻切 HTML 通道 `scripts/search_1023_html.py` 的结构（宽关键词 + size=200 + 日期过滤 + KW 打分），不要在 API 上反复重试浪费 7 分钟。
1. **检索脚本**: `search_query + " AND submittedDate:[YYYYMMDD0000 TO YYYYMMDD2359]"`（仅 API 通道可用），`sortBy=submittedDate`。建议保留 10 路查询覆盖：prompt rewrite 核心 / T2I 安全 / 概念擦除 / T2I benchmark / 多模态安全 / 越狱 / 水印 / 输入过滤 / 语义保持 / Agent 安全。
2. **工业界线索识别**: arXiv API 不返回 affiliation，必须抓 `https://arxiv.org/html/<id>` 从正文作者块提取机构（腾讯混元、Adobe/NVIDIA 都是这样发现的；`arxiv.org/html/<id>` 在 API 限流时仍可访问）。
3. **会议信息**: HTML 通道拿不到 `comment` 字段时，直接从 `/html/<id>` 正文或 abs 页补（HealBench 的 AAAI'27 即如此）。
4. **去重**: 先 `grep -rl <arxiv_id> categories/` 再决定是否建档。
5. **一致性校验**: 必跑脚本核对 papers 文件数 == _meta == README 徽章 == 两份 Survey == Landscape；六模块标题必须逐篇校验。
6. **数字纪律**: 摘要未给的量化结果，精读里明确标注"论文口径，不做数字外推"，禁止编造。

---

## 待跟进

- **2026-10-23 提出的 4 个实验待回看**：
  - A（tag-weighted loss 线）：`<tag>` 前强制复述意图 + PORN/VULG 各补 4 条豁免条款 → 看 VULG-HINT-EDGE 召回。
  - B（RL 改写线，**最高优先**）：锚点条件消融（无锚点 / 检索锚点 / oracle），联合分 $S=100·\text{mean}[\mathbb{1}(\text{保真}≥τ)·(1-\text{risk})]$。若 oracle−检索 gap > 3 分 → 瓶颈在锚点定位，先别训 RL。
  - C（标签审计线）：不确定性筛样本复判，**同时记录意图与标签**；若"意图对但标签错"占比 > 30% → 是绑定问题不是数据问题。
  - D（图审线）：500 张已知 NSFW 图过 3 个异构 checker，放行率差异 > 20 点 → 必须异构集成。
- 2026-10-22 提出的 4 个实验建议（constraint-first 排序 / span 级输出格式 / PORN-VULG 口径审计 / CSTI 式 gate 探针）若后续有结果，应在下一轮日报的业务板块回看。
- 仓库在 2026-05 至 2026-10 中旬存在较长断档（上一份日报为 2026-06-24），`daily_reports.missing_dates` 已如实登记 2026-10-01～10-21。
