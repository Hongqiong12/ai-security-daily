#!/usr/bin/env python3
"""2026-11-23 一致性校验：磁盘实际 papers/*.md 计数 == 各门面文件声明值。

本轮额外修复 11-12 补录造成的漂移：那次只加 6 篇精读，未同步
_meta/README/Survey/Landscape/benchmark/selected_papers。
"""
import glob, json, re, os, sys

os.chdir("/Users/ageisliu/WorkBuddy/Claw/ai-security-daily")

counts = {
    "t2t": len(glob.glob("categories/t2t/papers/*.md")),
    "t2i": len(glob.glob("categories/t2i/papers/*.md")),
    "agentic": len(glob.glob("categories/agentic-search/papers/*.md")),
}
counts["total"] = sum(counts.values())
print("=== 磁盘实际 ===", counts)

meta = json.load(open("_meta.json"))
print("_meta.paper_counts:", meta["paper_counts"])

readme = open("README.md").read()
badge = re.search(r"Papers-(\d+)-green", readme)
last = re.search(r"Last-Update-(\d{4})--(\d{2})--(\d{2})-orange", readme)
print("README badge:", badge.group(1) if badge else None,
      "| Last-Update:", "-".join(last.groups()) if last else None)
print("README 正文 316/322 出现:", {n: readme.count(n) for n in ("316", "328")})

t2i_survey = open("insights/t2i-survey.md").read()
t2t_survey = open("insights/t2t-survey.md").read()
print("t2i-survey 数据基础:", re.search(r"收录的 \*\*(\d+)\*\* 篇", t2i_survey).group(1))
print("t2t-survey 数据基础:", re.search(r"收录的 \*\*(\d+)\*\* 篇", t2t_survey).group(1))

land = open("insights/AI_Security_Landscape_2026.md").read()
print("Landscape 数据来源:", re.search(r"收录的 \*\*(\d+) 篇\*\*", land).group(1))
print("Landscape 尾部计数:", re.search(r"累计论文数 \*\*(\d+)\*\*", land).group(1))

sel = json.load(open("selected_papers.json"))
print("selected_papers 条数:", len(sel))

for name in ("categories/t2i/benchmark/README.md", "categories/t2t/benchmark/README.md"):
    txt = open(name).read()
    m = re.search(r"共 \*\*(\d+)\*\* 条", txt)
    rows = len(re.findall(r"^\| \*\*", txt, re.M))
    print(name, "声明", m.group(1) if m else None, "| 表格行", rows)

# 六模块检查（本轮新增文件由外部传入 ID 列表）
new_ids = sys.argv[1:]
for aid in new_ids:
    fs = glob.glob("categories/*/papers/%s_*.md" % aid)
    if not fs:
        print("MISSING", aid)
        continue
    txt = open(fs[0]).read()
    mods = len(re.findall(r"^## [一二三四五六]、", txt, re.M))
    print("6MOD", aid, mods, "OK" if mods == 6 else "FAIL", os.path.basename(fs[0]))
