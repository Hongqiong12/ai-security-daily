#!/usr/bin/env python3
"""arXiv 检索（HTML 搜索页通道）—— 用于 API 429 限流时的替代路径。

用法: python3 scripts/search_1023_html.py > /tmp/papers_1023.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request
from datetime import datetime

FROM_DATE = "2026-10-16"
TO_DATE = "2026-10-24"

QUERIES = {
    "q1_t2i": "text-to-image",
    "q2_diffusion": "diffusion model safety",
    "q3_nsfw": "NSFW",
    "q4_rewrite": "prompt rewriting",
    "q5_align": "safety alignment",
    "q6_moderation": "content moderation",
    "q7_jailbreak": "jailbreak",
    "q8_guard": "guard model safety",
    "q9_mmsafety": "multimodal safety",
    "q10_injection": "prompt injection",
    "q11_curation": "data curation label",
    "q12_erasure": "concept erasure",
    "q13_rlsafety": "reinforcement learning safety reward",
    "q14_t2i_align": "text-to-image alignment reward",
    "q15_image_filter": "image filter harmful",
}

KW = {
    "text-to-image": 3, "t2i": 3, "diffusion": 2, "image generation": 2,
    "prompt rewrit": 4, "rewriter": 3, "sanitiz": 3, "rephras": 3,
    "safety": 2, "nsfw": 3, "harmful": 2, "moderation": 3, "guard": 2,
    "jailbreak": 2, "concept eras": 2, "unlearn": 2, "watermark": 1,
    "benchmark": 2, "classifier": 2, "taxonomy": 2, "label": 1,
    "reinforcement": 2, "reward": 1, "semantic fidelity": 3,
    "semantic preserv": 2, "instruction following": 2, "red team": 2,
    "vision-language": 1, "multimodal": 1, "policy": 1, "audit": 1,
    "annotation": 1, "data curation": 2, "active learning": 2,
    "sensitive": 1, "privacy": 1, "pii": 2,
}

HDRS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) research-collector/1.0"}


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
          .replace("&#39;", "'").replace("&quot;", '"').replace("&nbsp;", " "))
    return " ".join(s.split())


def parse_date(txt):
    try:
        return datetime.strptime(txt.strip(), "%d %B, %Y").strftime("%Y-%m-%d")
    except Exception:
        return ""


def fetch(query, size=200, retries=3):
    url = ("https://arxiv.org/search/?query=" + urllib.parse.quote(query)
           + f"&searchtype=all&order=-announced_date_first&size={size}")
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            html = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "ignore")
            return html
        except Exception as ex:
            print(f"    retry {a+1} {type(ex).__name__}", file=sys.stderr)
            time.sleep(6 + a * 6)
    return ""


def parse(html):
    out = []
    for blk in html.split('<li class="arxiv-result">')[1:]:
        blk = blk.split("</li>")[0]
        m = re.search(r'<a href="https://arxiv.org/abs/([^"]+)">', blk)
        if not m:
            continue
        aid = m.group(1).split("v")[0]
        t = re.search(r'<p class="title is-5 mathjax">(.*?)</p>', blk, re.S)
        title = clean(t.group(1)) if t else ""
        au = re.search(r'<p class="authors">(.*?)</p>', blk, re.S)
        authors = []
        if au:
            authors = [clean(x) for x in re.findall(r'<a href="/search/\?searchtype=author[^"]*">(.*?)</a>', au.group(1), re.S)]
        af = re.search(r'<span class="abstract-full[^"]*"[^>]*>(.*?)</span>\s*(?:<a|</p>)', blk, re.S)
        abstract = clean(af.group(1)) if af else ""
        subj = [clean(x) for x in re.findall(r'<span class="tag is-small is-link tooltip[^"]*"[^>]*>(.*?)</span>', blk, re.S)]
        sd = re.search(r'Submitted</span>\s*([^;]+);', blk, re.S)
        pub = parse_date(sd.group(1)) if sd else ""
        cm = re.search(r'Comments?</span>:\s*(.*?)</p>', blk, re.S)
        out.append({"id": aid, "title": title, "authors": authors[:12],
                    "summary": abstract, "published": pub, "cats": subj,
                    "comment": clean(cm.group(1)) if cm else ""})
    return out


def score(p):
    s = 0
    tl = p["title"].lower()
    ab = p["summary"].lower()
    for k, w in KW.items():
        if k in tl:
            s += w * 3
        if k in ab:
            s += w
    return s


allp = {}
for name, q in QUERIES.items():
    html = fetch(q)
    res = parse(html) if html else []
    kept = 0
    for p in res:
        if not (FROM_DATE <= p["published"] <= TO_DATE):
            continue
        kept += 1
        if p["id"] in allp:
            allp[p["id"]]["hits"].append(name)
        else:
            p["hits"] = [name]
            p["score"] = score(p)
            allp[p["id"]] = p
    print(f"{name}: parsed={len(res)} in_range={kept}", file=sys.stderr)
    time.sleep(3)

items = sorted(allp.values(), key=lambda x: -x["score"])
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
