#!/usr/bin/env python3
"""2026-11-23 门面同步（幂等）：修复 11-12 补录漂移 + 写入本轮 6 篇。

覆盖：_meta.json / selected_papers.json / README 数字 / 两份 Survey /
Landscape 数字与热点三十 / 两份 benchmark README。
重复执行不会产生重复行（每处都按 ID 或唯一串做存在性检查）。
"""
import json, re, os, subprocess, html as H

ROOT = "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
os.chdir(ROOT)

TODAY = "2026-11-23"
COUNTS = {"t2t": 132, "t2i": 156, "agentic": 40, "total": 328}
MISSING = ["2026-11-%02d" % d for d in range(11, 23)]

NEW_T2I = [
    ("2611.26569", "EditSafetyBench", "CISPA + 港科广 + 港科大", "I2I 图文联合审核 / 系统级安全评测"),
    ("2611.20821", "CuRSE-Bench", "KAIST", "T2I 文化盲区评测 / 跨语言与地区层级"),
    ("2611.25929", "DSC", "夏威夷大学 + 独立研究者", "输入侧语义承诺与拒答错配"),
    ("2611.25226", "Tripwire-WM", "滑铁卢 + Vector + KTH", "输出侧水印 / 伪造事件报告"),
]
NEW_T2T = [
    ("2611.19216", "Operating-Point Failure", "Kookmin University", "冻结护栏阈值 / 多版本回归"),
    ("2611.20156", "Risk-certified Prompt Opt", "Capgemini + 埃夫里大学等", "约束式策略选点 / 风险认证"),
]
BACKFILL = ["2611.10106", "2611.10858", "2611.11980", "2611.12524",
            "2611.11067", "2611.12662"]


def rd(p):
    return open(p, encoding="utf-8").read()


def wr(p, s):
    open(p, "w", encoding="utf-8").write(s)


def curl(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", "Mozilla/5.0", url],
                       capture_output=True, text=True)
    return r.stdout


def clean(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def abs_meta(aid):
    txt = curl("https://arxiv.org/abs/%s" % aid)
    tm = re.search(r'<h1 class="title[^>]*>(.*?)</h1>', txt, re.S)
    am = re.search(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>', txt, re.S)
    title = clean(tm.group(1)).replace("Title:", "").strip() if tm else ""
    abstract = clean(am.group(1)).replace("Abstract:", "").strip() if am else ""
    return title, abstract


# ---------- 1. selected_papers.json ----------
sel = json.load(open("selected_papers.json", encoding="utf-8"))
have = {x["id"].split("v")[0] for x in sel}
pool = json.load(open("/tmp/full_1123.json", encoding="utf-8"))
byid = {x["id"].split("v")[0]: x for x in pool}

added = []
for aid in BACKFILL:
    if aid in have:
        continue
    title, abstract = abs_meta(aid)
    sel.append({"id": aid + "v1", "title": title, "summary": abstract,
                "published": "2026-11-10", "selected_date": "2026-11-12"})
    added.append(aid)

for aid, _, _, _ in NEW_T2I + NEW_T2T:
    if aid in have:
        continue
    x = byid.get(aid, {})
    # 网页端 abs 页抓回的 title 可能带 "Title: " descriptor 前缀，落库前统一剥掉
    title = re.sub(r"^(?:Title|Abstract):\s*", "", x.get("title", "")).strip()
    abstract = re.sub(r"^(?:Title|Abstract):\s*", "", x.get("abstract", "")).strip()
    sel.append({"id": aid + "v1", "title": title,
                "summary": abstract, "published": x.get("published", TODAY),
                "selected_date": TODAY})
    added.append(aid)

wr("selected_papers.json", json.dumps(sel, ensure_ascii=False, indent=1) + "\n")
print("selected_papers:", len(sel), "| added:", added)

# ---------- 2. _meta.json ----------
meta = {
    "_meta_version": "1.0",
    "last_updated": TODAY,
    "paper_counts": COUNTS,
    "survey_versions": {
        "t2t-survey": {"date": TODAY, "count": 132},
        "t2i-survey": {"date": TODAY, "count": 156},
        "agentic-search-survey": {"date": "2026-10-30", "version": "v1.9", "count": 40},
        "landscape_2026": {"date": TODAY, "version": "v3.18", "total_papers": 328},
    },
    "benchmark_status": {
        "t2t_benchmark": {"entries": 29, "last_updated": TODAY},
        "t2i_benchmark": {"entries": 50, "last_updated": TODAY},
        "agentic_benchmark": {"entries": 10, "last_updated": "2026-04-30"},
    },
    "daily_reports": {
        "latest": TODAY,
        "this_month_count": 9,
        "missing_dates": MISSING,
    },
    "workflow_version": "2.3",
    "today_selection": {
        "t2i": ["2611.26569_editsafetybench_text_aware_vision_blind",
                "2611.20821_curse_bench_cultural_blind_spots",
                "2611.25929_deferred_semantic_commitment",
                "2611.25226_tripwire_wm_forgery_evident"],
        "t2t_migration": ["2611.19216_operating_point_failure_frozen_guardrail",
                          "2611.20156_risk_certified_prompt_optimization"],
        "theme": "部件合格，不等于组合安全",
    },
    "_note": "This file is the single source of truth for all paper counts. Automation must update this file on every run. Never estimate counts — always use search_file to scan papers/ directories.",
}
wr("_meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
print("_meta.json: 328 / missing_dates", len(MISSING))

# ---------- 3. README 数字与日期（今日区块单独编辑） ----------
r = rd("README.md")
r = r.replace("Papers-316-green.svg", "Papers-328-green.svg")
r = r.replace("Last-Update-2026--11--10-orange.svg", "Last-Update-2026--11--23-orange.svg")
r = r.replace("基于 **316** 篇安全论文萃取的全局视野", "基于 **328** 篇安全论文萃取的全局视野")
r = r.replace("## 🔥 今日最具业务价值论文评测 (2026-11-10)",
              "## 🔥 今日最具业务价值论文评测 (2026-11-23)")
# Survey 状态行的日期
r = re.sub(r"\| 2026-11-10 \|", "| 2026-11-23 |", r)
wr("README.md", r)
print("README: badge/date/count updated")

# ---------- 4. t2i-survey ----------
s = rd("insights/t2i-survey.md")
s = s.replace("本项目收录的 **148** 篇 T2I 安全论文", "本项目收录的 **156** 篇 T2I 安全论文")
s = s.replace("**更新日期**: 2026-11-10", "**更新日期**: 2026-11-23")
rows = [
 "| **EditSafetyBench / Text-Aware, Vision-Blind** | [2611.26569](https://arxiv.org/abs/2611.26569) | 2026 (**CISPA Helmholtz + 港科广 + 港科大**) | **编辑器在读文字没在读图**：5,940 image-instruction 对 / 11 风险类目 / 3 编辑意图 / 4 系统；UIR（恶意指令拒答）Gemini **87.1%** / GPT **81.6%**，而 UNR（风险图+中性指令）只 **24.2% / 22.4%**；SOR（安全图误拒）**14.0% / 11.5%**，主题中性图降到 **3.6%**；图审核分由视觉主导（0.195 > 0.113）而放行率由文本主导（unsafe-intent 下图片安全只差 **0.4% / 0.2%**）；GPT 放行 **70.4%** 不安全政治编辑、Gemini 仅 **34.8%**；GPT 对两个文本审核分同为 **0.063** 的样本拒 **100%** vs **33%** ⇒ 关键词触发。Discussion 明确 UNR 格正确处置「取决于部署语境」，建议 policy-adaptive 图护栏 + 意图感知决策 (NEW) |",
 "| **CuRSE-Bench** | [2611.20821](https://arxiv.org/abs/2611.20821) | 2026 (**KAIST**) | **通用 rubric 无害、目标文化有害**：CultureCraft 构造 **10,709** 条 culture-specific + **2,648** 条不变换 controls / 6 地区 × 10 harm axes / 每条 harm vector ≥2 独立来源；7 个评分视角（6 region persona + 1 paired culture-blind）；culture-blind judge 只在 culture-specific 集低估、controls 上一致 ⇒ **选择性盲区**；5 个已部署生成管线仍可绕过且**未做针对过滤器优化**；五组配对对照（knowledge-swap / 命名指称泄漏 / 骨干消融 / 天花板 / per-cell bootstrap）。**English-only 明确列为局限** ⇒ 文化视角覆盖 ≠ 语言覆盖 (NEW) |",
 "| **DSC / Deferred Semantic Commitment** | [2611.25929](https://arxiv.org/abs/2611.25929) | 2026 (**夏威夷大学 + 独立研究者**) | **语义一字未改、只改承诺形式**：300 条挑战集，直接陈述 Returned **16.3%** / Endorsed **15.3%**，问句+肯定线索 **43.3% / 41.3%**；MPUP 100 条 78%→**91%**；直接陈述未返回图的 **251** 条里单次 DSC 产出 **91 张(36.3%)** 背书原命题；Qwen3.5-VL-27B 严格拒答 **29.6%→8.3%**；layer-52 activation patching 完整残差恢复 **12/13**、refusal-aligned 分量 **11/13**、减投影掉到 **1/13**、随机方向 0；natural refusal AUC **layer 31** 才 >0.95；✓ / YES / 对勾图片三线索结果一致 (NEW) |",
 "| **Tripwire-WM / Reject and Report** | [2611.25226](https://arxiv.org/abs/2611.25226) | 2026 (**滑铁卢 + Vector Institute + KTH**) | **拒了伪造却没留证据**：把图语义提交到初始潜噪声**幅度**（符号水印未用的信道），伪造图水印有效但 commitment 与内容不符 ⇒ 检测器既 reject 又 report；MS-COCO / 10⁻⁶ FPR 下 imprinting 伪造接受 **0%**（SemBind 最高 **55.0%**）、reprompting 最多 **1.8%**（SemBind **46.2%**）、真图 ≥**99%**；外部异常检测器 G-Cos 只标 **19.7–24.0%**、PGID-F 只标 **18.6–39.7%** 且误报真图 ⇒ 加一层外部检测器再次被证伪。与 NotaryMark 合起来要求判定/信息/事件三栏 (NEW) |",
]
anchor = "*本次 Survey 更新：2026-11-10"
if "2611.26569" not in s:
    s = s.replace(anchor, "\n".join(rows) + "\n\n" + anchor, 1)
s = re.sub(r"\*本次 Survey 更新：2026-11-10（[^）]*）。\*",
           "*本次 Survey 更新：2026-11-23（新增 4 篇：2611.26569 EditSafetyBench 图文联合安全错配、2611.20821 CuRSE-Bench 文化盲区与跨语言口径、2611.25929 DSC 语义承诺与拒答错配、2611.25226 Tripwire-WM 判定/信息/事件三栏；并修复 11-12 补录造成的 148→152 计数漂移，现为 156）。*",
           s, count=1)
wr("insights/t2i-survey.md", s)
print("t2i-survey: 156 / +4 rows")

# ---------- 5. t2t-survey ----------
s = rd("insights/t2t-survey.md")
s = s.replace("本项目收录的 **128** 篇 T2T 安全论文", "本项目收录的 **132** 篇 T2T 安全论文")
s = s.replace("**更新日期**: 2026-11-10", "**更新日期**: 2026-11-23")
rows = [
 "| **Operating-Point Failure of Frozen Guardrail Probes** | [2611.19216](https://arxiv.org/abs/2611.19216) | 2026 (**Kookmin University**, IEEE TDSC 投稿) | 冻结阈值 / 多版本回归 / 策略热更新 | **AUROC 一动不动而误杀率涨 15 倍**：18 cells / 16 次公开 LM 更新，Phase 2 预注册；1% 目标下 Phase 1 **8/9** fail closed；最大 FPR **1.01%→15.12%** 而 **AUROC 变化 ≤0.0058**，staleness 判据**一个都没报**；label-free 两矩估计标记 **0.918** 受损 cells、清除 **0.898** 未受损；两矩模型 63 cells 中 **0.905** 解释到 1.5 倍内；**存储良性 prompt 重设阈值 9/9 恢复（0.96–1.02×）无需新标签**，但**参考集投毒 1% 后最多只剩 0.017 有害被标记**；攻击者控制更新在 **3/5 seeds** 压低定向类目，两种无标签检查都漏过 (NEW) |",
 "| **Risk-certified Prompt Optimization** | [2611.20156](https://arxiv.org/abs/2611.20156) | 2026 (**Capgemini + 埃夫里大学 + CentraleSupélec + ENSIIE**) | 约束式选点 / 分布无关风险认证 / 可配置护栏 | 把 system prompt 选点写成 `max 良性放行率 s.t. missed-attack ≤ α`；CPS（固定池 + LTT + Bonferroni + Clopper–Pearson UCB）与 CRISP（**hard example-guided rewriting** + reusable-holdout + Guess-and-Check，certified/uncertified 两种群）；**固定数据、生成假设**下靠受限 holdout 访问保住证书；4 数据集（BIPIA / Deepset / SPL / SID）三份互斥切分；留出测试持续遵守目标风险、效用随 α 放宽提升。**α 约束的是风险率不是覆盖率**；单一 α、无 per-category 阈值 (NEW) |",
]
anchor = "*本次 Survey 更新：2026-11-10"
if "2611.19216" not in s:
    s = s.replace(anchor, "\n".join(rows) + "\n\n" + anchor, 1)
s = re.sub(r"\*本次 Survey 更新：2026-11-10（[^）]*）。\*",
           "*本次 Survey 更新：2026-11-23（新增 2 篇：2611.19216 冻结护栏 operating point 在模型更新后失效、2611.20156 风险认证式策略选点；并修复 11-12 补录造成的 128→130 计数漂移，现为 132）。*",
           s, count=1)
wr("insights/t2t-survey.md", s)
print("t2t-survey: 132 / +2 rows")

# ---------- 6. benchmark README ----------
b = rd("categories/t2i/benchmark/README.md")
b = b.replace("最后回填: 2026-11-10 | 共 **47** 条", "最后回填: 2026-11-23 | 共 **50** 条")
newrows = [
 "| **EditJudge Bench（合成 GT）** | [2611.12524](https://arxiv.org/abs/2611.12524) | 2026 arXiv | 11-12 补录回填：以合成 ground truth 构建编辑评测，规避人工判定方差 (NEW) |",
 "| **EditSafetyBench** | [2611.26569](https://arxiv.org/abs/2611.26569) | 2026 arXiv（**CISPA + 港科广 + 港科大**） | **第一个把 I2I 图文联合安全做成析因格子的工作**：5,940 配对 / 11 风险类目 / 3 编辑意图 / 4 系统；UIR **87.1%/81.6%** 而 UNR 仅 **24.2%/22.4%**，SOR **14.0%/11.5%**；审核分由视觉主导（0.195 > 0.113）而放行率由文本主导（图片安全只差 0.2–0.4%）⇒ **判定层没读图审输出** (NEW) |",
 "| **CuRSE-Bench** | [2611.20821](https://arxiv.org/abs/2611.20821) | 2026 arXiv（**KAIST**） | **T2I 安全评测的文化盲区基准**：10,709 文化特定 + 2,648 不变换 controls / 6 地区 × 10 harm axes / 7 评分视角；culture-blind judge 只在特定集低估、controls 一致 ⇒ 选择性盲区；**English-only 为局限**，文化视角 ≠ 语言覆盖 (NEW) |",
]
tail = "\n[← 返回文生图目录](../README.md)"
if "2611.26569" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + "\n" + tail, 1)
wr("categories/t2i/benchmark/README.md", b)

b = rd("categories/t2t/benchmark/README.md")
b = re.sub(r"最后回填: 2026-11-10 \| 共 \*\*27\*\* 条", "最后回填: 2026-11-23 | 共 **29** 条", b)
newrows = [
 "| **Beyond AUROC: low-FPR operating point** | [2611.11067](https://arxiv.org/abs/2611.11067) | 2026 arXiv | 11-12 补录回填：低 FPR 区间下 AUROC 与决策质量脱钩 (NEW) |",
 "| **HC-ROCP: certify, report, refuse** | [2611.12662](https://arxiv.org/abs/2611.12662) | 2026 arXiv | 11-12 补录回填：风险受控下的认证 / 报告 / 拒答三段式 (NEW) |",
]
tail = "\n[← 返回文生文目录](../README.md)"
if "2611.11067" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + "\n" + tail, 1)
wr("categories/t2t/benchmark/README.md", b)
print("benchmark: t2i 50 / t2t 29")

# ---------- 7. Landscape ----------
L = rd("insights/AI_Security_Landscape_2026.md")
L = L.replace("基于本项目收录的 **316 篇**", "基于本项目收录的 **328 篇**")
L = L.replace("**更新日期**: 2026-11-10（v3.17 增量更新）", "**更新日期**: 2026-11-23（v3.18 增量更新）")
L = L.replace("### T2T 论文分布（126 篇）", "### T2T 论文分布（132 篇）")
L = L.replace("### T2I 论文分布（144 篇）", "### T2I 论文分布（156 篇）")
L = L.replace("### Agentic Search 论文分布（39 篇）", "### Agentic Search 论文分布（40 篇）")
L = L.replace("*最近更新：2026-11-10（v3.17 增量更新），累计论文数 **316**（T2T: **128** 篇，T2I: **148** 篇，Agentic Search: **40** 篇）。*",
              "*最近更新：2026-11-23（v3.18 增量更新），累计论文数 **328**（T2T: **132** 篇，T2I: **156** 篇，Agentic Search: **40** 篇）。*")

hot30 = """### 🔥 热点三十：部件合格，不等于组合安全（2026-11-23 新增）

热点二十九说"约束写下去了，绑定发生在别处"。这一轮六篇把镜头再往上一层：**约束也好、判定也好，检查都发生在入口、单件、平均那一层，而风险长在组合之后那一层**——所以即使每个部件都"合格"，整体依然不安全。

六组配对，一一对应：

| 被检查的部件 | 真正出事的组合 | 实测 |
|---|---|---|
| 文本编辑意图 | 风险源图 + 中性指令 | UIR **87.1%/81.6%** 而 UNR **24.2%/22.4%**（EditSafetyBench） |
| 通用 rubric 判无害 | 目标地区文化语境 | culture-blind 只在特定集低估、controls 一致（CuRSE-Bench） |
| 问句与对勾各自中性 | 组合后恢复有害断言 | Returned **16.3%→43.3%**、Endorsed **15.3%→41.3%**（DSC） |
| 水印判定合法 | 伪造事件本身 | 被拒却不报告的伪造最高占 **46%**；SemBind 接受 **55.0%**（Tripwire-WM） |
| 排序（AUROC）不变 | 冻结阈值的 operating point | AUROC **≤0.0058** 而 FPR **1.01%→15.12%** |
| 平均性能达标 | 显式风险约束未认证 | `max 效用 s.t. 风险 ≤ α` 才给有限样本证书 |

**由此提炼三条新纪律**：① **任何只在单个部件 / 入口 / 平均值上做的验收，必须补一个组合层的生效指标**（图文联合状态 / 完整命题 / 判定-信息-事件 / 排序-操作点 / 效用-约束）；② **"空窗"要拆开写**——本轮 3849 篇里 NSFW 严格词边界 3 命中、阈值 39、水印 13，但 `t2_prompt_rewrite` 严格 0 ⇒ 正确表述是"改写方法零供给、评测与护栏有供给"，笼统写"整批零供给"会把 4 篇可迁移工作一起否定；③ **并发打导出 API 会把整个 IP 限掉且不限查询类型**，网页端 arxiv.org 是独立限流池，全批池拉全后主题词/形态通道一律本地正则复现。

**权重侧/输入侧边界第十轮**：本轮权重侧有供给但全在候选观察（24220 擦除被下游 LoRA/DreamBooth 微调恢复、20625/20623 necessity-driven 局部外科式抑制、25640 证明全局与任务条件 guardedness 不可同时成立）。结论不变为互补非替代，但**新增一条修正**：11-08 记的"全世界都还没公开做 I2I 改写"应改成——**改写方法仍空白，但该分流的输入状态已被 EditSafetyBench 公开刻画**（UNR 格），0/0% 因此拿到第四种可证伪归因：**分流只读文本通路**。

"""
if "热点三十" not in L:
    L = L.replace("### 🔥 热点二十九：", hot30 + "### 🔥 热点二十九：", 1)

v318 = """*本次 v3.18 更新：新增 4 篇 T2I/T+I2I 论文（EditSafetyBench 图文联合安全错配 UIR 87.1%/81.6% 而 UNR 24.2%/22.4%、且 UNR 格正确处置被明确交给部署语境；CuRSE-Bench 10,709+2,648 配对揭示选择性文化盲区且 English-only 为局限；DSC 语义一字未改而 Returned 16.3%→43.3%、Endorsed 15.3%→41.3%；Tripwire-WM 伪造接受 0% vs SemBind 55.0%、真图 ≥99% @10⁻⁶ FPR、拒了必须报告）与 2 篇方法论迁移（Operating-Point Failure：18 cells/16 更新下 FPR 1.01%→15.12% 而 AUROC ≤0.0058、存储良性 prompt 重设 9/9 恢复但 1% 投毒即废；Risk-certified Prompt Opt：LTT+Clopper–Pearson+Bonferroni 的约束式策略选点与 reusable-holdout 自适应搜索），并新增一条范式信号（热点三十）：**部件合格，不等于组合安全**。供给侧为**断档回补轮**：上一份日报 11-10、11-12 有 6 篇补录精读但无日报且未同步门面（316→322 漂移，本轮一并修复为 328）；导出 API 被并发 429 限流后改走 arxiv.org 网页端，**十分类 × 11-16→11-20 五个公告批次 = 3849 篇全批池**（1923 篇带摘要），主题词 10 路与形态 10 路在本地正则复现；`t2_prompt_rewrite` 严格 **0**（主线空窗第 16 周），`t10_video_safety` 0，但 `t3_i2i_edit_safety` **首次命中 1 篇**，NSFW 严格词边界 3 命中 ⇒ 空窗性质由"整批供给为零"修正为"改写方法零供给、评测与护栏有供给"。头部公司 0 篇，如实标注。*
"""
if "v3.18 更新" not in L:
    L = L.replace("*本次 v3.17 更新：", v318 + "*本次 v3.17 更新：", 1)
wr("insights/AI_Security_Landscape_2026.md", L)
print("Landscape: v3.18 / 328 / 热点三十")
