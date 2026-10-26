#!/usr/bin/env python3
"""arXiv HTML 通道 round-2 补充检索（q1/q2 失败后重跑 + 更聚焦关键词）。"""
import json
import sys

sys.path.insert(0, "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("s", "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily/scripts/search_1026_html.py")

import re
import time
import urllib.parse
import urllib.request
from datetime import datetime

FROM_DATE = "2026-10-19"
TO_DATE = "2026-10-26"
HDRS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) research-collector/1.0"}

QUERIES = {
    "r1_t2i_safety": "text-to-image safety",
    "r2_prompt_rewrite": "prompt rewrite",
    "r3_sanitize": "sanitization prompt",
    "r4_nsfw_detect": "NSFW detection",
    "r5_image_moderation": "image moderation classifier",
    "r6_guardrail": "guardrail safety classifier",
    "r7_risk_taxonomy": "risk taxonomy safety",
    "r8_t2i_bench": "text-to-image benchmark evaluation",
    "r9_erasure": "concept erasure diffusion",
    "r10_jailbreak_img": "jailbreak image generation attack",
    "r11_rl_image": "reinforcement learning image generation reward",
    "r12_multimodal_guard": "multimodal guardrail benchmark",
    "r13_label": "label noise training data quality",
    "r14_safety_rewrite": "safety rewriting LLM",
    "r15_vision_moderation": "visual content safety review",
    "r16_omni": "omni-modal safety",
}

KW = {
    "text-to-image": 3, "t2i": 3, "diffusion": 2, "image generation": 2,
    "prompt rewrit": 5, "rewriter": 4, "sanitiz": 4, "rephras": 4,
    "semantic fidelity": 4, "semantic preserv": 3, "safety": 2, "nsfw": 5,
    "harmful": 2, "moderation": 4, "guard": 3, "classifier": 3,
    "taxonomy": 3, "label": 2, "jailbreak": 3, "concept eras": 3,
    "benchmark": 2, "reinforcement": 2, "reward": 2, "audit": 2,
    "annotation": 2, "data curation": 3, "active learning": 3,
    "label noise": 3, "image safety": 5, "content safety": 3,
}


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


def fetch(query, size=200, retries=4):
    url = ("https://arxiv.org/search/?query=" + urllib.parse.quote(query)
           + f"&searchtype=all&order=-announced_date_first&size={size}")
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            return urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "ignore")
        except Exception as ex:
            print(f"    retry {a+1} {type(ex).__name__}", file=sys.stderr)
            time.sleep(12 + a * 10)
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
    tl, ab = p["title"].lower(), p["summary"].lower()
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
    time.sleep(4)

items = sorted(allp.values(), key=lambda x: -x["score"])
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
