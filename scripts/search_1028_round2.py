#!/usr/bin/env python3
"""2026-10-28 第二轮宽口径复核 —— 检验"T2I 安全空窗"是否为真信号。

吸取 10-27 教训：不做宽口径复核就不能下"空窗"结论。本轮换措辞、
放宽到全分类、并把 a8/a10 这类上轮命中极低的查询重跑一次（防漏召）。
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request

FROM_DATE = "2026-10-21"
TO_DATE = "2026-10-28"
HDRS = {"User-Agent": "Mozilla/5.0 research-collector/1.0"}
ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)

QUERIES = {
    "b01_nsfw_any": 'abs:NSFW OR abs:nudity OR abs:nude OR abs:sexual',
    "b02_image_safety": 'abs:"image safety" OR abs:"safe image" OR abs:"unsafe content" OR abs:"harmful content"',
    "b03_gen_safety": 'abs:generative AND abs:safety AND (abs:image OR abs:visual)',
    "b04_erase_diff": 'abs:erasure OR abs:"concept removal" OR abs:forget OR abs:ablation',
    "b05_moderation_any": 'abs:moderation OR abs:moderator',
    "b06_redteam_img": 'abs:"red team" OR abs:redteaming OR abs:attack AND abs:image',
    "b07_t2i_safety2": 'abs:"text-to-image" AND (abs:policy OR abs:prohibited OR abs:inappropriate OR abs:unsafe)',
    "b08_guard_any": 'abs:guardrail OR abs:shield OR abs:defense AND abs:generation',
    "b09_classify_safety": 'abs:"safety classification" OR abs:"risk classification" OR abs:"harm classification"',
    "b10_label_hier": 'abs:"label hierarchy" OR abs:"hierarchical classification" OR abs:"multi-label"',
    "b11_jailbreak_img": 'abs:jailbreak AND (abs:diffusion OR abs:"image generation" OR abs:"text-to-image")',
    "b12_rewrite_any": 'abs:rewrite OR abs:rewriting OR abs:sanitization',
    "b13_reward_img": 'abs:"reward model" OR abs:reward AND abs:image',
    "b14_unlearn_diff": 'abs:unlearning AND (abs:diffusion OR abs:"image generation" OR abs:"text-to-image")',
    "b15_vlm_guard": 'abs:"vision-language" AND (abs:guard OR abs:safety OR abs:moderation)',
    "b16_child": 'abs:minor OR abs:child OR abs:"underage" OR abs:CSAM',
    "b17_political_img": 'abs:political AND abs:image AND (abs:bias OR abs:sensitive OR abs:misinformation)',
    "b18_deepfake": 'abs:deepfake OR abs:"face forgery" OR abs:"manipulated image"',
}


def clean(s):
    return " ".join((s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                     .replace("&#39;", "'").replace("&quot;", '"')).split())


def fetch(sq, retries=4):
    url = ("http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(sq)
           + "&start=0&max_results=300&sortBy=submittedDate&sortOrder=descending")
    for a in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=120).read().decode("utf-8", "ignore")
        except Exception as ex:
            print(f"    retry {a+1} {type(ex).__name__}", file=sys.stderr)
            time.sleep(12 + a * 12)
    return ""


def parse(xml):
    out = []
    for blk in ENTRY.findall(xml):
        m = re.search(r"<id>http://arxiv.org/abs/([^<]+)</id>", blk)
        if not m:
            continue
        aid_full = m.group(1)
        aid = re.sub(r"v\d+$", "", aid_full)
        t = re.search(r"<title>(.*?)</title>", blk, re.S)
        su = re.search(r"<summary>(.*?)</summary>", blk, re.S)
        pu = re.search(r"<published>(.*?)</published>", blk)
        au = re.findall(r"<name>(.*?)</name>", blk)
        cm = re.search(r'<arxiv:comment[^>]*>(.*?)</arxiv:comment>', blk, re.S)
        out.append({
            "id": aid,
            "title": clean(t.group(1)) if t else "",
            "authors": au[:12],
            "summary": clean(su.group(1)) if su else "",
            "published": pu.group(1)[:10] if pu else "",
            "comment": clean(cm.group(1)) if cm else "",
        })
    return out


allp = {}
for name, q in QUERIES.items():
    sq = f"({q}) AND submittedDate:[202610210000 TO 202610282359]"
    xml = fetch(sq)
    batch = [p for p in parse(xml) if FROM_DATE <= p["published"] <= TO_DATE]
    for p in batch:
        if p["id"] in allp:
            allp[p["id"]]["hits"].append(name)
        else:
            p["hits"] = [name]
            allp[p["id"]] = p
    print(f"{name}: {len(batch)}", file=sys.stderr)
    time.sleep(3.4)

items = sorted(allp.values(), key=lambda x: -len(x["hits"]))
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
