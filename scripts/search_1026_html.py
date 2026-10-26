#!/usr/bin/env python3
"""arXiv 检索（HTML 搜索页通道）—— 2026-10-26 日报，窗口 2026-10-19 ~ 2026-10-26。

用法: python3 scripts/search_1026_html.py > /tmp/papers_1026.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request
from datetime import datetime

FROM_DATE = "2026-10-19"
TO_DATE = "2026-10-26"

QUERIES = {
    "q1_t2i": "text-to-image safety",
    "q2_t2i_rewrite": "prompt rewriting safety",
    "q3_nsfw": "NSFW image generation",
    "q4_moderation": "content moderation image",
    "q5_t2i_align": "text-to-image alignment",
    "q6_jailbreak": "jailbreak text-to-image",
    "q7_diffusion_safety": "diffusion safety erasure",
    "q8_guard": "guard model multimodal safety",
    "q9_mmsafety": "multimodal safety benchmark",
    "q10_classification": "harmful content classification taxonomy",
    "q11_rl_rewrite": "reinforcement learning prompt optimization reward",
    "q12_data_curation": "data curation label noise",
    "q13_image_filter": "image safety filter detection",
    "q14_semantic_fidelity": "semantic preservation rewrite",
    "q15_injection": "prompt injection defense",
    "q16_tencent": "safety alignment LLM industrial",
}

KW = {
    "text-to-image": 3, "t2i": 3, "diffusion": 2, "image generation": 2,
    "image synthesis": 2, "prompt rewrit": 5, "rewriter": 4, "sanitiz": 4,
    "rephras": 4, "semantic fidelity": 4, "semantic preserv": 3,
    "intent": 2, "safety": 2, "nsfw": 4, "harmful": 2, "moderation": 4,
    "guard": 2, "classifier": 3, "taxonomy": 3, "label": 2,
    "jailbreak": 3, "adversarial": 2, "concept eras": 3, "unlearn": 2,
    "watermark": 1, "benchmark": 2, "reinforcement": 3, "reward": 2,
    "edit distance": 2, "levenshtein": 3, "instruction following": 2,
    "red team": 2, "vision-language": 1, "multimodal": 1, "policy": 2,
    "audit": 2, "annotation": 2, "data curation": 3, "active learning": 3,
    "label noise": 3, "sensitive": 2, "privacy": 1, "pii": 2,
    "image safety": 4, "content safety": 3, "risk": 1, "chain-of-thought": 2,
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
    time.sleep(2.5)

items = sorted(allp.values(), key=lambda x: -x["score"])
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
