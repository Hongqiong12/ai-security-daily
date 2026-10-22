# 自动化执行记忆：T2I/T+I2I 工业安全每日调研

> 自动化标识: ai-readme | 依据: `WORKFLOW.md` v2.3 | 首次记录: 2026-10-22

---

## 执行历史

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

1. **检索脚本**: `search_query + " AND submittedDate:[YYYYMMDD0000 TO YYYYMMDD2359]"`，`sortBy=submittedDate`。建议保留 10 路查询覆盖：prompt rewrite 核心 / T2I 安全 / 概念擦除 / T2I benchmark / 多模态安全 / 越狱 / 水印 / 输入过滤 / 语义保持 / Agent 安全。
2. **工业界线索识别**: arXiv API 不返回 affiliation，必须抓 `https://arxiv.org/html/<id>` 从正文作者块提取机构（本次腾讯署名就是这么发现的）。
3. **会议信息**: 从 arXiv API 的 `arxiv:comment` 字段提取（本次拿到 NeurIPS 2026 ×1、ECCV 2026 Spotlight ×1、NeurIPS 2026 TAE WS ×1）。
4. **去重**: 先 `grep -rl <arxiv_id> categories/` 再决定是否建档。
5. **一致性校验**: 必跑脚本核对 papers 文件数 == _meta == README 徽章 == 两份 Survey == Landscape；六模块标题必须逐篇校验。
6. **数字纪律**: 摘要未给的量化结果，精读里明确标注"论文口径，不做数字外推"，禁止编造。

---

## 待跟进

- 2026-10-22 提出的 4 个实验建议（constraint-first 排序 / span 级输出格式 / PORN-VULG 口径审计 / CSTI 式 gate 探针）若后续有结果，应在下一轮日报的业务板块回看。
- 仓库在 2026-05 至 2026-10 中旬存在较长断档（上一份日报为 2026-06-24），后续如恢复日更需补齐 `daily_reports.missing_dates`。
