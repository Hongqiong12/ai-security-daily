# 自动化执行记忆：T2I/T+I2I 工业安全每日调研

> 自动化标识: ai-readme | 依据: `WORKFLOW.md` v2.3 | 首次记录: 2026-10-22

---

## 执行历史

### 2026-10-26 ✅ 成功

- **检索**: 全程 **HTML 搜索页通道**（API 未尝试，沿用 10-23 结论）。两轮各 16 路查询，窗口 2026-10-19→10-26，去重 114 篇、排除已收录剩 110 篇。**q1（`text-to-image safety`）与 q2（`prompt rewriting safety`）首轮 429，第二轮退避 12s+10s 递增后成功** → 结论：单轮 2.5s 间隔不够，重要查询要留二轮重跑预算。
- **收录**: 6 篇（T2I 直接相关 4 / 工业审核方法论迁移 1 / T2T 迁移 1，T2I 占比 66.7%）。
  - T2I: Yuvion VL(2606.25034, **阿里安全 AGI Lab**)、Omni-UBench(2610.31713, **浙大+阿里**)、SELECT(2510.16342 v2, 北邮)、Attractive Faces(2610.28195)
  - 迁移: AVLM Failure Taxonomy(2606.30059, **TikTok/字节 + 悉尼大学, NeurIPS'26**)、Faithful Harm Monitors(2610.30727)
- **本周主题判断**: T2I 输入侧改写**连续第三周空窗**（110 篇候选里无新改写方法）。主线转为「**分数不可信**」——图审配方（C2FT）/ 评测新尺子（掩码消融 + 匹配误报率）/ 锚点距离曲线 / 奖励语义≠奖励行为。
- **交付**: 主日报 + 6 篇六模块精读 + README/t2i-survey(4.13–4.16)/t2t-survey(5.w)/Landscape v3.5/benchmark README(30→32)/_meta.json/selected_papers.json(18→24) 全量同步；commit `cf8be66` 双推成功（github 589b2f4..cf8be66 / 工蜂 d2cb401..bc3021f）。
- **计数**: T2T 103 / T2I 102 / Agentic 39 / Total 244（文件系统精确扫描，README 徽章 + 两份 Survey + Landscape 头部/脚注/分布 + _meta 七处交叉校验一致）。6 篇 arXiv 链接全部 HTTP 200。

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
1. **检索脚本**: 本轮新增 `scripts/search_1026_html.py`（16 路）+ `scripts/search_1026_round2.py`（16 路补充），均可直接改 `FROM_DATE/TO_DATE` 复用。**建议固定为"两轮 16+16 路"结构**：首轮 2.5s 间隔拿量，次轮 4s 间隔 + 12s 起退避抢救 429 的查询。
2. **工业界线索识别**: arXiv API 不返回 affiliation，必须抓 `https://arxiv.org/html/<id>` 从正文作者块提取机构。本轮三处均靠此法确认：`Yuvion Team / Alibaba Security AGI Lab`、`State Key Lab of Blockchain and Data Security, Zhejiang University / Alibaba Group`、`Affiliation: TikTok / The University of Sydney`。**HTML 里搜 "Alibaba"/"Tencent"/"TikTok" 等关键词并打印上下文**是最快的定位方式（`<span class="ltx_role_affiliation">` 正则常失效）。
3. **会议信息**: HTML 通道拿不到 `comment` 字段时，直接从 `/html/<id>` 正文或 abs 页补（HealBench 的 AAAI'27 即如此）。
4. **去重**: 先 `grep -rl <arxiv_id> categories/` 再决定是否建档。
5. **一致性校验**: 必跑脚本核对 papers 文件数 == _meta == README 徽章 == 两份 Survey == Landscape；六模块标题必须逐篇校验。
6. **数字纪律**: 摘要未给的量化结果，精读里明确标注"论文口径，不做数字外推"，禁止编造。

---

## 待跟进

- **2026-10-26 提出的实验（优先级从高到低）**：
  - **A（图审线，最先做，成本最低）**：图审 AB 改**匹配误报率**协议 + **掩码消融**自查。判据：掩码后 FPR > 0.3 ⇒ 图审在读 prompt 不在读图。
  - **B（tag-weighted 线）**：**S_retain 保留率审计**（清洗前池 vs 清洗后集，按一级类/层级/文本长度/reject_tag 回流/暗示语境/标注一致性 6 维）。判据：VULG-HINT-EDGE 与 PORN 边界档保留率显著低于 PORN 明确类 ⇒ 先改过滤规则，别做标签复判。
  - **C（RL 改写线）**：① 锚点五分类消融取代"有/无锚点"二分（SELECT 证明距离是连续的）；② **奖励属性敏感性审计**（100 组单属性变化图对，测语义一致性 vs 美观/饱和/人脸占比/锐度）。判据：非目标属性相关性 ≥ 语义一致性 ⇒ 奖励不可用。
  - **D（标签审计线）**：双生成器仲裁分判「标注错 vs 样本难」+ 构造 **harmless-made-alarming** 子集专测过度预测（PORN 误报根源，目前完全没测）。
  - **E（C2FT-lite）**：若 10-23 的"复述意图 + 豁免条款"实验收益有限，说明单样本监督到头了，应改多图对比（每锚点配 1 同类真值 + 1 混淆类真值，ρ=0.3，加 PAT 抗捷径）。
- **2026-10-23 提出的 4 个实验待回看**（A 已升级为 E，B 已升级为 C，C 已升级为 D，D 已升级为 A）：
  - A（tag-weighted 线）：`<tag>` 前强制复述意图 + PORN/VULG 各补 4 条豁免条款 → 看 VULG-HINT-EDGE 召回。
  - B（RL 改写线）：锚点条件消融，联合分 $S=100·\text{mean}[\mathbb{1}(\text{保真}≥τ)·(1-\text{risk})]$。
  - C（标签审计线）：不确定性筛样本复判，**同时记录意图与标签**；若"意图对但标签错"占比 > 30% → 是绑定问题不是数据问题。
  - D（图审线）：500 张已知 NSFW 图过 3 个异构 checker，放行率差异 > 20 点 → 必须异构集成。
- 2026-10-22 提出的 4 个实验建议（constraint-first 排序 / span 级输出格式 / PORN-VULG 口径审计 / CSTI 式 gate 探针）若后续有结果，应在下一轮日报的业务板块回看。
- **候选观察待补读**：Concept Acupuncturist(2610.32059, SAE 概念擦除, SDXL-Turbo 遗忘 +36.34pt)、CheckDistill(2610.26740, checklist 蒸馏奖励)。若擦除线或改写保真评审重启，优先补这两篇。
- 仓库在 2026-05 至 2026-10 中旬存在较长断档（上一份日报为 2026-06-24），`daily_reports.missing_dates` 已如实登记 2026-10 的 23 个缺失日期。
