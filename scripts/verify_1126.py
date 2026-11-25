#!/usr/bin/env python3
"""2026-11-26 一致性校验（WORKFLOW.md Step 5.2）。

磁盘实际 papers/*.md == 各门面文件声明值；外加六模块精读、主日报固定板块、
关键词覆盖、死链扫描、selected_papers 幂等等质量门禁。任意一项 FAIL 即 exit 1。
"""
import glob, json, re, os, sys

ROOT = "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
os.chdir(ROOT)

TODAY = "2026-11-26"
IDS = ["2611.31048", "2611.31774", "2611.32407", "2611.27388",
       "2611.30523", "2611.32848"]
T2I_IDS, T2T_IDS = IDS[:5], IDS[5:]
FAIL = []


def ck(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


counts = {
    "t2t": len(glob.glob("categories/t2t/papers/*.md")),
    "t2i": len(glob.glob("categories/t2i/papers/*.md")),
    "agentic": len(glob.glob("categories/agentic-search/papers/*.md")),
}
counts["total"] = sum(counts.values())
print("=== 磁盘实际 ===", counts)

meta = json.load(open("_meta.json", encoding="utf-8"))
ck(meta["paper_counts"] == counts, "_meta.paper_counts == 磁盘")
ck(meta["last_updated"] == TODAY, "_meta.last_updated")
ck(meta["daily_reports"]["latest"] == TODAY, "_meta.daily_reports.latest")
ck(meta["daily_reports"]["this_month_count"] == len(glob.glob("daily-reports/2026-11/*.md")),
   "_meta.this_month_count == 11 月日报文件数")
ck(meta["survey_versions"]["landscape_2026"]["version"] == "v3.21", "_meta Landscape v3.21")
ck(meta["survey_versions"]["t2i-survey"]["count"] == counts["t2i"], "_meta t2i-survey count")
ck(meta["survey_versions"]["t2t-survey"]["count"] == counts["t2t"], "_meta t2t-survey count")
ck(meta["benchmark_status"]["t2i_benchmark"]["entries"] == 56, "_meta t2i_benchmark 56")
ck(meta["benchmark_status"]["t2t_benchmark"]["entries"] == 34, "_meta t2t_benchmark 34")
ck(len(meta["today_selection"]["t2i"]) == 5 and len(meta["today_selection"]["t2t_migration"]) == 1,
   "_meta.today_selection 5 T2I + 1 迁移")

readme = open("README.md", encoding="utf-8").read()
badge = re.search(r"Papers-(\d+)-green", readme)
last = re.search(r"Last-Update-(\d{4})--(\d{2})--(\d{2})-orange", readme)
ck(badge and int(badge.group(1)) == counts["total"], "README 徽章 == total")
ck(last and "-".join(last.groups()) == TODAY, "README Last-Update")
ck("基于 **346** 篇安全论文" in readme, "README 正文 346")
ck("## 🔥 今日最具业务价值论文评测 (2026-11-26)" in readme, "README 今日区块 11-26")
today_head = readme.split("## 🔭 前沿 Survey")[0]
ck("2026-11-25_AI安全每日深度情报.md" not in today_head, "README 今日区块不含旧日报链接")
for aid in IDS:
    ck(aid in readme, "README 索引含 %s" % aid)
ck("KlingAI" in readme and "Adobe" in readme, "README 头部公司标注")
ck("github.com/ageisliu/ai-security-daily" not in readme, "README 无旧仓库 404 死链")

t2i = open("insights/t2i-survey.md", encoding="utf-8").read()
t2t = open("insights/t2t-survey.md", encoding="utf-8").read()
ck(re.search(r"收录的 \*\*(\d+)\*\* 篇", t2i).group(1) == str(counts["t2i"]), "t2i-survey 数据基础 == t2i")
ck(re.search(r"收录的 \*\*(\d+)\*\* 篇", t2t).group(1) == str(counts["t2t"]), "t2t-survey 数据基础 == t2t")
ck("**更新日期**: 2026-11-26" in t2i and "**更新日期**: 2026-11-26" in t2t, "两份 Survey 更新日期")
ck("本次 Survey 更新：2026-11-26" in t2i and "本次 Survey 更新：2026-11-26" in t2t, "两份 Survey 更新注记")


def survey_row_hits(txt, aid):
    return sum(1 for ln in txt.split("\n") if ln.startswith("| **") and aid in ln)


for aid in T2I_IDS:
    ck(survey_row_hits(t2i, aid) == 1, "t2i-survey 恰含 1 行 %s" % aid)
for aid in T2T_IDS:
    ck(survey_row_hits(t2t, aid) == 1, "t2t-survey 恰含 1 行 %s" % aid)

land = open("insights/AI_Security_Landscape_2026.md", encoding="utf-8").read()
ck(re.search(r"收录的 \*\*(\d+) 篇\*\*", land).group(1) == str(counts["total"]), "Landscape 数据来源 == total")
ck(re.search(r"累计论文数 \*\*(\d+)\*\*", land).group(1) == str(counts["total"]), "Landscape 尾部计数 == total")
ck("### T2T 论文分布（137 篇）" in land and "### T2I 论文分布（169 篇）" in land, "Landscape 分模态计数")
ck("v3.21 增量更新" in land and "热点三十三" in land, "Landscape v3.21 / 热点三十三")
ck("本次 v3.21 更新" in land, "Landscape v3.21 更新注记")

for name, declared, mod in (("categories/t2i/benchmark/README.md", 56, "t2i"),
                            ("categories/t2t/benchmark/README.md", 34, "t2t")):
    txt = open(name, encoding="utf-8").read()
    m = re.search(r"共 \*\*(\d+)\*\* 条", txt)
    lines = [ln for ln in txt.split("\n") if ln.startswith("|")]
    header = sum(1 for ln in lines if "论文 |" in ln or "Paper |" in ln)
    sep = sum(1 for ln in lines if re.fullmatch(r"\|[-: |]+\|", ln))
    rows = len(lines) - header - sep
    ck(m and int(m.group(1)) == declared, "%s 声明 %d" % (mod, declared))
    ck(rows == declared, "%s 实际数据行 %d == 声明 %d" % (mod, rows, declared))
    ck("最后回填: 2026-11-26" in txt, "%s 回填日期" % mod)

sel = json.load(open("selected_papers.json", encoding="utf-8"))
ck(len(sel) == 120, "selected_papers 120 条")
ck(len({x["id"].split("v")[0] for x in sel}) == 120, "selected_papers ID 无重复")
for aid in IDS:
    ck(any(x["id"].startswith(aid) and x.get("title") and x.get("summary") for x in sel),
       "selected_papers %s 有标题+摘要" % aid)

print("=== 质量门禁：六模块精读 ===")
for aid in IDS:
    fs = glob.glob("categories/*/papers/%s_*.md" % aid)
    if not fs:
        ck(False, "精读存在 %s" % aid)
        continue
    txt = open(fs[0], encoding="utf-8").read()
    mods = len(re.findall(r"^## [一二三四五六]、", txt, re.M))
    ck(mods == 6, "%s 六模块 %d/6" % (aid, mods))
    ck("https://arxiv.org/abs/%s" % aid in txt, "%s arXiv 链接规范" % aid)
    ck("github.com/ageisliu/ai-security-daily" not in txt, "%s 无旧仓库死链" % aid)

rep_path = "daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md"
rep = open(rep_path, encoding="utf-8").read()
print("=== 质量门禁：主日报 ===")
for sec in ("业务对齐研究板块", "检索与质量记录", "候选观察", "下一步实验建议",
            "风险锚点处理启发", "三维评测设计启发", "直接可迁移方法", "趋势信号"):
    ck(sec in rep, "主日报含「%s」" % sec)
for kw in ("5.2%", "3.42%", "L2_30", "PORN/VULG", "GRPO", "0/0%", "serving setup",
           "2,700+", "TIDE", "BODYBENCH", "HinT", "CRIE", "VeriOrigin", "跨语言", "英文 ASR",
           "conformal", "aggregate-vs-macro F1", "PSI", "fp8", "fp4", "TTFT"):
    ck(kw in rep, "主日报覆盖关键词 %s" % kw)
ck("github.com/ageisliu/ai-security-daily" not in rep, "主日报无旧仓库死链")
ck(rep.count("https://arxiv.org/abs/2611.31048") >= 1, "主日报头条 HinT 链接")

print("\n=== 结论 ===")
print("PASS" if not FAIL else "FAIL %d 项: %s" % (len(FAIL), FAIL))
sys.exit(1 if FAIL else 0)
