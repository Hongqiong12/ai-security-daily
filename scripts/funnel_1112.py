#!/usr/bin/env python3
"""2026-11-12 分层筛选：严格词边界 + 审核 + 改写 + 生成-编辑结构 + 11-10 新批次专查。"""
import json, re, os, glob
from collections import Counter

papers = json.load(open("/tmp/full_1112.json"))
have = set()
for p in glob.glob("categories/*/papers/*.md"):
    have.add(os.path.basename(p).split("_")[0])

print("POOL", len(papers), "| 磁盘已建档", len(have))
print("DATES", dict(sorted(Counter(p["published"] for p in papers).items())))
inpool = [p for p in papers if p["id"].split("v")[0] in have]
print("IN-POOL already-collected:", len(inpool))
fresh = [p for p in papers if p["id"].split("v")[0] not in have]
print("NOT-collected:", len(fresh))
print("FRESH DATES", dict(sorted(Counter(p["published"] for p in fresh).items())))

NSFW = re.compile(r"\b(NSFW|nude|nudity|naked|pornograph\w*|obscen\w*|vulgar\w*|sexual content|explicit content|adult content)\b", re.I)
MOD = re.compile(r"(image moderation|content moderation|safety classifier|safety filter|guard model|guardrail|image safety|harmful image|unsafe image|moderation model)", re.I)
REWRITE = re.compile(r"(rewrit\w*|rephras\w*|sanitiz\w*|paraphras\w*)", re.I)
SAFE = re.compile(r"(saf\w*|harm\w*|toxic\w*|policy|risk)", re.I)
GEN = re.compile(r"(text-to-image|t2i|image generation|image generator|diffusion model|diffusion transformer|generative model|image editing|image editor|editing instruction|instruction-based editing|unified .*generation|image synthesis|visual generation)", re.I)
EDIT = re.compile(r"(image editing|image editor|editing instruction|instruction-based editing|unified .*generation|editing model|edit benchmark)", re.I)
WM = re.compile(r"(watermark|provenance|AIGC detection|image forensics)", re.I)


def show(tag, rx_list, pool=None, limit=40):
    pool = pool if pool is not None else papers
    hits = []
    for p in pool:
        blob = p["title"] + " " + p["abstract"]
        if all(r.search(blob) for r in rx_list):
            hits.append(p)
    print("\n[%s] %d" % (tag, len(hits)))
    for p in hits[:limit]:
        print("  %s [%s] | %s" % (p["id"], p["published"], p["title"][:115]))
    return hits


h1 = show("NSFW strict (whole pool)", [NSFW])
h2 = show("moderation", [MOD])
h3 = show("rewrite x safe", [REWRITE, SAFE])
h4 = show("gen x safe", [GEN, SAFE], limit=30)
h5 = show("edit structure", [EDIT], limit=40)
h6 = show("watermark/provenance", [WM], limit=30)

# 11-10 新批次专查
d10 = [p for p in fresh if p["published"] == "2026-11-10"]
print("\n\n========== 11-10 NEW BATCH (fresh %d) ==========" % len(d10))
n1 = show("11-10 NSFW strict", [NSFW], pool=d10)
n2 = show("11-10 moderation", [MOD], pool=d10)
n3 = show("11-10 rewrite x safe", [REWRITE, SAFE], pool=d10)
n4 = show("11-10 gen x safe", [GEN, SAFE], pool=d10, limit=30)
n5 = show("11-10 edit structure", [EDIT], pool=d10, limit=40)
n6 = show("11-10 watermark", [WM], pool=d10)

json.dump([{"id": p["id"], "t": p["title"], "d": p["published"], "a": p["abstract"][:600]}
           for p in d10], open("/tmp/d10_1112.json", "w"), ensure_ascii=False, indent=1)
json.dump([{"id": p["id"], "t": p["title"], "d": p["published"], "a": p["abstract"][:600]}
           for p in fresh], open("/tmp/fresh_1112.json", "w"), ensure_ascii=False, indent=1)
