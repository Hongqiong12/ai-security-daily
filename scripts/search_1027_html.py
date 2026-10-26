#!/usr/bin/env python3
"""arXiv 检索（HTML 搜索页通道）—— 2026-10-27 日报，窗口 2026-10-20 ~ 2026-10-27。

本轮按 5 条业务主线重排查询：I2I 编辑安全 > 输入侧改写 > 输出侧图审 > 分类标签 > 训练数据。
用法: python3 scripts/search_1027_html.py > /tmp/papers_1027.json
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
    # ---- I2I 指令式编辑安全（本轮新增重点，对齐 0/0% 命中缺口）----
    "q1_i2i_edit_safety": "instruction-based image editing safety",
    "q2_edit_guard": "image editing guardrail",
    "q3_i2i_nsfw": "image editing NSFW",
    # ---- 输入侧改写 ----
    "q4_prompt_rewrite": "prompt rewriting safety",
    "q5_prompt_sanitize": "prompt sanitization rewrite",
    "q6_semantic_fidelity": "semantic fidelity rewrite preserving intent",
    # ---- 输出侧图审 ----
    "q7_image_moderation": "image content moderation classifier",
    "q8_nsfw_detect": "NSFW image detection",
    "q9_vlm_judge": "vision language model judge safety evaluation",
    # ---- T2I 核心 ----
    "q10_t2i_safety": "text-to-image safety",
    "q11_t2i_align": "text-to-image alignment harmful",
    "q12_jailbreak_t2i": "jailbreak text-to-image diffusion",
    # ---- 分类体系 ----
    "q13_taxonomy": "harmful content taxonomy fine-grained classification",
    "q14_region_political": "political sensitivity moderation region",
    "q15_cot_classify": "chain-of-thought classification labels",
    # ---- RL 改写 / 擦除 ----
    "q16_rl_reward": "reinforcement learning reward image generation alignment",
    "q17_concept_erase": "concept erasure diffusion unlearning",
    "q18_edit_rate": "edit distance constraint constrained generation",
    # ---- 数据构建 / 训练效率 ----
    "q19_active_learn": "active learning label noise data curation",
    "q20_lora_efficient": "LoRA QLoRA efficient safety fine-tuning",
    # ---- 补充 ----
    "q21_pii": "privacy PII image recognition",
    "q22_injection": "prompt injection jailbreak defense",
}

KW = {
    # I2I / 编辑
    "image editing": 5, "instruction-based": 5, "instruction-guided": 4,
    "editing instruction": 5, "image edit": 4, "inpaint": 3, "editing": 3,
    # 改写
    "prompt rewrit": 5, "rewriter": 4, "sanitiz": 4, "rephras": 4,
    "rewrite": 4, "intent-preserving": 4, "semantic fidelity": 4,
    "semantic preserv": 3, "paraphrase": 3,
    # 输出侧图审
    "image moderation": 5, "content moderation": 4, "nsfw": 4,
    "image safety": 4, "safety filter": 4, "detector": 2, "classifier": 3,
    "judge": 3, "guard": 3,
    # T2I 主体
    "text-to-image": 3, "t2i": 3, "diffusion": 2, "image generation": 2,
    "image synthesis": 2, "generative": 1,
    # 分类标签
    "taxonomy": 3, "hierarchical": 3, "fine-grained": 2, "label": 2,
    "annotation": 2, "risk": 1, "policy": 2,
    # 攻击
    "jailbreak": 3, "adversarial": 2, "bypass": 2, "red team": 2,
    # 擦除
    "concept eras": 3, "unlearn": 3, "forget": 2,
    # RL / 度量
    "reinforcement": 3, "reward": 2, "preference": 2,
    "edit distance": 2, "levenshtein": 3, "constraint": 2,
    # 数据 / 训练
    "data curation": 3, "active learning": 3, "label noise": 3,
    "synthetic data": 2, "distill": 2, "lora": 2, "quantiz": 2,
    "efficient": 1, "benchmark": 2, "dataset": 2,
    # 补充
    "pii": 2, "privacy": 1, "injection": 2,
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
            time.sleep(8 + a * 8)
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
    time.sleep(3.0)

items = sorted(allp.values(), key=lambda x: -x["score"])
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
