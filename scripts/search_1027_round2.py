#!/usr/bin/env python3
"""arXiv 检索 第二轮（角度切换，挖掘 10-20~10-23 批次里首轮没覆盖到的论文）。
用法: python3 scripts/search_1027_round2.py > /tmp/papers_1027_r2.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request
from datetime import datetime

FROM_DATE = "2026-10-20"
TO_DATE = "2026-10-27"

QUERIES = {
    "r1_editing_instruction": "instruction guided image editing harmful",
    "r2_editing_rewrite": "editing prompt rewrite large language model",
    "r3_multimodal_guard": "multimodal guardrail safety classification",
    "r4_image_classifier_sft": "vision language model fine-tuning safety classification",
    "r5_benchmark_nsfw": "NSFW benchmark dataset evaluation",
    "r6_political": "political content safety evaluation LLM",
    "r7_risk_taxonomy": "risk taxonomy hierarchical safety label",
    "r8_cot_safety": "chain-of-thought safety reasoning moderation",
    "r9_rl_alignment_image": "reinforcement learning alignment image generation reward model",
    "r10_reward_hacking": "reward hacking reward model bias evaluation",
    "r11_unlearning": "machine unlearning diffusion model concept",
    "r12_erase_attack": "concept erasure attack restore unsafe",
    "r13_data_audit": "training data auditing annotation quality",
    "r14_distill_safety": "distillation small model safety guard",
    "r15_watermark": "watermark provenance generated image detection",
    "r16_adversarial_image": "adversarial attack safety filter image",
    "r17_semantic_similarity": "semantic similarity metric generation evaluation",
    "r18_llm_judge": "LLM as judge reliability evaluation bias",
    "r19_diffusion_edit": "diffusion model image editing safety alignment",
    "r20_prompt_engineering": "prompt optimization safety constraint LLM",
    "r21_content_policy": "content policy violation detection multimodal",
    "r22_tencent_alibaba": "content security large model industrial deployment",
}

KW = {
    "image editing": 5, "editing instruction": 5, "instruction-based": 4, "inpaint": 3,
    "prompt rewrit": 5, "rewrit": 4, "sanitiz": 4, "rephras": 3, "paraphrase": 3,
    "intent": 2, "semantic": 2, "fidelity": 3, "preserv": 2,
    "moderation": 5, "guardrail": 4, "guard": 3, "nsfw": 5, "safety filter": 4,
    "classifier": 3, "detector": 2, "judge": 3, "taxonomy": 3, "hierarchical": 3,
    "label": 2, "annotation": 2, "audit": 3, "policy": 2, "political": 3,
    "text-to-image": 3, "diffusion": 2, "image generation": 2, "generative": 1,
    "unlearn": 3, "eras": 3, "jailbreak": 3, "adversarial": 2, "bypass": 2,
    "reinforcement": 3, "reward": 3, "preference": 2, "distill": 2,
    "benchmark": 2, "dataset": 2, "evaluation": 1, "watermark": 2, "provenance": 2,
    "chain-of-thought": 3, "reasoning": 1, "data curation": 3, "label noise": 3,
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
    time.sleep(3.5)

items = sorted(allp.values(), key=lambda x: -x["score"])
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
