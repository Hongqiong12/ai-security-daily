#!/usr/bin/env python3
"""2026-11-10 分层筛选：先跑严格 NSFW / 审核 / 改写三道检验，再按生成-编辑结构匹配。
用法: python3 scripts/funnel_1110.py
"""
import json, re, os, glob

papers = json.load(open("/tmp/full_1110.json"))
have = set()
for p in glob.glob("categories/*/papers/*.md"):
    have.add(os.path.basename(p).split("_")[0])
print("POOL", len(papers), "| already collected", len(have))

NSFW = re.compile(r"\b(NSFW|nude|nudity|naked|pornograph\w*|obscen\w*|vulgar\w*|sexual content|explicit content|adult content)\b", re.I)
MOD = re.compile(r"(image moderation|content moderation|safety classifier|safety filter|guard model|guardrail|image safety|harmful image|unsafe image|moderation model)", re.I)
REWRITE = re.compile(r"(rewrit\w*|rephras\w*|sanitiz\w*|paraphras\w*)", re.I)
SAFE = re.compile(r"(saf\w*|harm\w*|toxic\w*|policy|risk)", re.I)
GEN = re.compile(r"(text-to-image|t2i|image generation|image generator|diffusion model|diffusion transformer|generative model|image editing|image editor|editing instruction|instruction-based editing|unified .*generation|image synthesis|visual generation)", re.I)

def show(tag, rx_list):
    hits = []
    for p in papers:
        blob = p["title"] + " " + p["abstract"]
        if all(r.search(blob) for r in rx_list):
            hits.append(p)
    print("\n[%s] %d" % (tag, len(hits)))
    for p in hits:
        print("  %s | %s" % (p["id"], p["title"][:120]))
    return hits

h1 = show("NSFW strict", [NSFW])
h2 = show("moderation", [MOD])
h3 = show("rewrite x safe", [REWRITE, SAFE])
h4 = show("gen x safe", [GEN, SAFE])

# 生成/编辑语义词标题集
gen = [p for p in papers if GEN.search(p["title"] + " " + p["abstract"])]
print("\n[GEN structural] %d papers" % len(gen))
json.dump([{"id": p["id"], "t": p["title"], "d": p["published"]} for p in gen],
          open("/tmp/gen_1110.json", "w"), ensure_ascii=False, indent=1)
