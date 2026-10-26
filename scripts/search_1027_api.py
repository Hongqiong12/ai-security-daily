#!/usr/bin/env python3
"""arXiv API 检索通道 —— 2026-10-27 日报，窗口 2026-10-20 ~ 2026-10-27。

背景：HTML 搜索页通道在本轮严重欠召回（44 查询仅 22 篇），且 arXiv 最新提交止于
2026-10-23（10-24/25 周末 + 10-26 批次未发）。改用 export API + submittedDate 倒序，
按查询逐页拉取，遇到早于 FROM_DATE 即停，保证每个查询在窗口内取满。

用法: python3 scripts/search_1027_api.py > /tmp/papers_1027_api.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request

FROM_DATE = "2026-10-20"
TO_DATE = "2026-10-27"

CATS = "(cat:cs.CV OR cat:cs.CR OR cat:cs.CL OR cat:cs.LG OR cat:cs.AI)"

QUERIES = {
    # --- I2I 指令式编辑安全（本轮重点，对齐 0/0% 分流缺口）---
    "a1_i2i_edit_safety": 'abs:"image editing" AND (abs:safety OR abs:harmful OR abs:NSFW OR abs:moderation OR abs:guard)',
    "a2_edit_instruction": 'abs:"editing instruction" OR abs:"instruction-based editing" OR abs:"instruction-guided editing"',
    "a3_edit_rewrite": 'abs:"editing" AND (abs:rewrite OR abs:rewriting OR abs:sanitiz OR abs:rephras)',
    # --- 输入侧改写 ---
    "a4_prompt_rewrite": '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"prompt rewriting" OR abs:"rewriter" OR abs:"rephrase")',
    "a5_semantic_fidelity": '(abs:"semantic fidelity" OR abs:"semantic preservation" OR abs:"intent-preserving" OR abs:"intent preservation")',
    "a6_prompt_safety": 'abs:prompt AND (abs:"safety rewrite" OR abs:"safety rewriting" OR abs:"sanitization" OR abs:"harmful prompt")',
    # --- 输出侧图审 ---
    "a7_image_moderation": '(abs:"content moderation" OR abs:"image moderation" OR abs:"safety classifier" OR abs:"safety filter")',
    "a8_nsfw": '(abs:NSFW OR abs:"not safe for work" OR abs:"sexual content")',
    "a9_guard_model": '(abs:"guard model" OR abs:"guardrail" OR abs:"moderation model" OR abs:"safety guard")',
    # --- T2I 核心 ---
    "a10_t2i_safety": '(abs:"text-to-image" OR abs:"image generation") AND (abs:safety OR abs:harmful OR abs:unsafe)',
    "a11_t2i_jailbreak": '(abs:jailbreak OR abs:"red teaming") AND (abs:diffusion OR abs:"text-to-image" OR abs:"image generation" OR abs:image)',
    "a12_t2i_benchmark": '(abs:"text-to-image" OR abs:diffusion) AND (abs:benchmark OR abs:evaluation) AND (abs:safety OR abs:alignment OR abs:policy)',
    # --- 分类体系 / 标签 ---
    "a13_taxonomy": '(abs:taxonomy OR abs:"hierarchical label" OR abs:"risk category" OR abs:"fine-grained classification") AND (abs:safety OR abs:harmful OR abs:content)',
    "a14_political": '(abs:political OR abs:region) AND (abs:moderation OR abs:safety OR abs:sensitivity OR abs:policy)',
    "a15_cot_moderation": '(abs:"chain-of-thought" OR abs:"reasoning") AND (abs:moderation OR abs:"safety classification" OR abs:"harmful content")',
    # --- RL / 奖励 / 擦除 ---
    "a16_rl_rewrite": '(abs:"reinforcement learning" OR abs:"policy optimization" OR abs:RLHF) AND (abs:rewrite OR abs:image OR abs:diffusion) AND (abs:safety OR abs:alignment OR abs:reward)',
    "a17_concept_erasure": '(abs:"concept erasure" OR abs:"concept unlearning" OR abs:"machine unlearning" OR abs:"concept forgetting")',
    "a18_reward_bias": '(abs:"reward model" OR abs:reward) AND (abs:bias OR abs:hacking OR abs:"shortcut" OR abs:faithful)',
    # --- 数据 / 训练效率 ---
    "a19_data_audit": '(abs:"data quality" OR abs:"label noise" OR abs:"annotation quality" OR abs:"data audit" OR abs:"active learning")',
    "a20_efficient_tune": '(abs:LoRA OR abs:QLoRA OR abs:distillation) AND (abs:safety OR abs:alignment OR abs:guard)',
    # --- 补充 ---
    "a21_pii": '(abs:"personally identifiable" OR abs:PII OR abs:privacy) AND (abs:image OR abs:multimodal OR abs:detection)',
    "a22_injection": '(abs:"prompt injection" OR abs:"jailbreak defense" OR abs:"indirect injection")',
    "a23_watermark": '(abs:watermark OR abs:provenance) AND (abs:image OR abs:generation OR abs:generated)',
    "a24_vlm_judge": '(abs:"LLM-as-a-judge" OR abs:"judge model" OR abs:"VLM judge" OR abs:"MLLM judge")',
    "a25_erasure_attack": '(abs:"erasure" OR abs:unlearning) AND (abs:attack OR abs:restore OR abs:recover OR abs:bypass)',
    "a26_dataset_curation": '(abs:"data curation" OR abs:"synthetic data") AND (abs:safety OR abs:moderation OR abs:alignment)',
}

KW = {
    "image editing": 6, "editing instruction": 5, "instruction-based": 4, "instruction-guided": 4,
    "image edit": 4, "inpaint": 2, "editing": 2,
    "prompt rewrit": 6, "rewrit": 4, "sanitiz": 5, "rephras": 4, "paraphrase": 3,
    "intent-preserving": 5, "semantic fidelity": 5, "semantic preserv": 4,
    "moderation": 5, "guardrail": 4, "guard model": 4, "guard": 2,
    "nsfw": 5, "sexual content": 4, "safety filter": 4, "safety classifier": 4,
    "classifier": 2, "detector": 2, "judge": 3,
    "taxonomy": 4, "hierarchical": 3, "fine-grained": 2, "label": 2, "annotation": 2,
    "audit": 3, "policy": 2, "political": 3, "region": 1,
    "text-to-image": 3, "t2i": 3, "diffusion": 2, "image generation": 2,
    "unlearn": 3, "eras": 3, "forget": 2, "jailbreak": 3, "adversarial": 2, "bypass": 2,
    "reinforcement": 3, "reward": 3, "preference": 2, "distill": 2, "lora": 2,
    "benchmark": 2, "dataset": 2, "watermark": 2, "provenance": 3,
    "chain-of-thought": 3, "data quality": 3, "label noise": 3, "active learning": 3,
    "pii": 2, "privacy": 1, "injection": 2, "safety": 2, "harmful": 2, "unsafe": 2,
}

HDRS = {"User-Agent": "Mozilla/5.0 research-collector/1.0"}

ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)


def clean(s):
    s = (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
          .replace("&#39;", "'").replace("&quot;", '"'))
    return " ".join(s.split())


def fetch(q, start=0, n=200, retries=4):
    sq = f"{CATS} AND ({q}) AND submittedDate:[202610200000 TO 202610272359]"
    url = ("http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(sq)
           + f"&start={start}&max_results={n}&sortBy=submittedDate&sortOrder=descending")
    for a in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=120).read().decode("utf-8", "ignore")
        except Exception as ex:
            print(f"    retry {a+1} {type(ex).__name__}", file=sys.stderr)
            time.sleep(10 + a * 10)
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
        cats = re.findall(r'<category term="([^"]+)"', blk)
        out.append({
            "id": aid,
            "title": clean(t.group(1)) if t else "",
            "authors": au[:12],
            "summary": clean(su.group(1)) if su else "",
            "published": pu.group(1)[:10] if pu else "",
            "cats": cats,
            "comment": clean(cm.group(1)) if cm else "",
            "version": aid_full[len(aid):] or "v1",
        })
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
    got, start = [], 0
    while True:
        xml = fetch(q, start=start)
        batch = [p for p in parse(xml) if FROM_DATE <= p["published"] <= TO_DATE]
        got.extend(batch)
        if len(parse(xml)) < 200 or start >= 600:
            break
        start += 200
    for p in got:
        if p["id"] in allp:
            allp[p["id"]]["hits"].append(name)
        else:
            p["hits"] = [name]
            p["score"] = score(p)
            allp[p["id"]] = p
    print(f"{name}: {len(got)}", file=sys.stderr)
    time.sleep(3.2)

items = sorted(allp.values(), key=lambda x: -x["score"])
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
