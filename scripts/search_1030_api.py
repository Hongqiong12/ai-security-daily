#!/usr/bin/env python3
"""arXiv API 检索通道 —— 2026-10-30 日报，窗口 2026-10-23 ~ 2026-10-30。

供给侧探测（10-30 00:0x）: 最新 published 批次仍停在 **2026-10-27**，
arXiv /list/cs.CV/recent 页头也仍是 "Wed, 28 Oct 2026" —— 即 10-29 / 10-30
两个公告批次均未生成，本轮相对 10-29 那轮**新增供给为 0**。
⇒ 本轮定位为「**补筛轮**」：不追求新量，改用 10-29 记忆里记下的教训
   （学术术语查询已被"用尽"，换口语化/产品化措辞）去捞前几轮漏筛的存量。

本轮相对 10-29 的变化:
 1) 新增 12 路口语化/产品化查询（photo editing assistant / edit request /
    prompt guard / query rewrite / image filter / trust & safety / age
    assurance / brand safety 等），专门针对 a1/a28/a30 三个归零查询换词。
 2) CATS 扩容: 加入 cs.MM / eess.IV / cs.IR（前几轮只扫 4 类，多媒体与图像
    处理类目里的图审/编辑工作可能整体被漏掉）。
 3) 保留 10-29 全部 34 路作为基座，便于跨轮比对"哪一路归零"。

用法: python3 scripts/search_1030_api.py > /tmp/papers_1030_api.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request

FROM_DATE = "2026-10-23"
TO_DATE = "2026-10-30"

CATS = "(cat:cs.CV OR cat:cs.CR OR cat:cs.CL OR cat:cs.LG OR cat:cs.AI OR cat:cs.MM OR cat:eess.IV)"

QUERIES = {
    # --- I2I 指令式编辑安全（对齐 0/0% 分流缺口）---
    "a1_i2i_edit_safety": 'abs:"image editing" AND (abs:safety OR abs:harmful OR abs:NSFW OR abs:moderation OR abs:guard)',
    "a2_edit_instruction": 'abs:"editing instruction" OR abs:"instruction-based editing" OR abs:"instruction-guided editing"',
    "a3_edit_rewrite": 'abs:"editing" AND (abs:rewrite OR abs:rewriting OR abs:sanitiz OR abs:rephras)',
    "a27_edit_fidelity": '(abs:"editing" OR abs:"image edit") AND (abs:"semantic fidelity" OR abs:"instruction following" OR abs:"fidelity")',
    # --- 输入侧改写 ---
    "a4_prompt_rewrite": '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"rewriter" OR abs:"rephrase")',
    "a5_semantic_fidelity": '(abs:"semantic fidelity" OR abs:"semantic preservation" OR abs:"intent-preserving" OR abs:"intent preservation")',
    "a6_prompt_safety": 'abs:prompt AND (abs:"safety rewrite" OR abs:"safety rewriting" OR abs:"sanitization" OR abs:"harmful prompt")',
    # --- 输出侧图审 ---
    "a7_image_moderation": '(abs:"content moderation" OR abs:"image moderation" OR abs:"safety classifier" OR abs:"safety filter")',
    "a8_nsfw": '(abs:NSFW OR abs:"not safe for work" OR abs:"sexual content")',
    "a9_guard_model": '(abs:"guard model" OR abs:"guardrail" OR abs:"moderation model" OR abs:"safety guard")',
    "a28_image_only_sft": '(abs:"image classifier" OR abs:"image-only" OR abs:"pure vision") AND (abs:safety OR abs:NSFW OR abs:moderation OR abs:harmful)',
    "a29_moderation_ab": '(abs:"moderation" OR abs:"safety judge") AND (abs:"agreement" OR abs:"comparison" OR abs:"ensemble" OR abs:"disagreement")',
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
    "a30_edit_instr_rewrite": '(abs:"editing instruction" OR abs:"edit instruction" OR abs:"instruction editing") AND (abs:rewrite OR abs:safe OR abs:robust OR abs:adversarial OR abs:mismatch)',
    "a31_moderation_data_synth": '(abs:"moderation" OR abs:"safety") AND (abs:"synthetic" OR abs:"data generation" OR abs:"pseudo-label" OR abs:"distillation") AND (abs:image OR abs:vision OR abs:multimodal)',
    "a32_hier_taxonomy": '(abs:"hierarchical" OR abs:"multi-label" OR abs:"fine-grained") AND (abs:"moderation" OR abs:"content safety" OR abs:"harm" OR abs:"risk") AND (abs:classification OR abs:annotat OR abs:label)',
    "a33_nsfw_boundary": '(abs:NSFW OR abs:pornograph OR abs:obscene OR abs:vulgar OR abs:"sexual") AND (abs:detect OR abs:classif OR abs:boundary OR abs:confus OR abs:benchmark)',
    "a34_low_resource_safety": '(abs:"low-resource" OR abs:"compute-efficient" OR abs:"parameter-efficient" OR abs:"quantization") AND (abs:safety OR abs:moderation OR abs:guard OR abs:alignment)',

    # ================= 2026-10-30 新增 12 路口语化 / 产品化查询 =================
    # 针对 10-29 三个归零查询（a1/a28/a30）换词，绕开已被"用尽"的学术术语
    "b1_photo_edit_assistant": '(abs:"photo editing" OR abs:"image editing assistant" OR abs:"editing tool" OR abs:"photo editor") AND (abs:safety OR abs:policy OR abs:guard OR abs:refus OR abs:harm)',
    "b2_edit_request": '(abs:"edit request" OR abs:"editing request" OR abs:"modify the image" OR abs:"requested edit")',
    "b3_prompt_guard": '(abs:"prompt guard" OR abs:"input filter" OR abs:"input-side" OR abs:"gatekeeper" OR abs:"pre-filter") AND (abs:safety OR abs:harm OR abs:content)',
    "b4_query_rewrite": '(abs:"query rewrite" OR abs:"query rewriting" OR abs:"query reformulation" OR abs:"query refinement") AND (abs:safety OR abs:policy OR abs:harm)',
    "b5_image_filter": '(abs:"image filter" OR abs:"output filter" OR abs:"post-filter" OR abs:"content filter") AND (abs:image OR abs:generation OR abs:vision)',
    "b6_trust_safety": '(abs:"trust and safety" OR abs:"trust & safety" OR abs:"safety operations" OR abs:"policy enforcement")',
    "b7_age_assurance": '(abs:"age assurance" OR abs:"age estimation" OR abs:minor OR abs:child) AND (abs:safety OR abs:content OR abs:moderation OR abs:generation)',
    "b8_brand_safety": '(abs:"brand safety" OR abs:"advertising safety" OR abs:"adversarial content") AND (abs:image OR abs:moderation OR abs:multimodal)',
    "b9_safety_training_data": '(abs:"safety data" OR abs:"refusal data" OR abs:"preference data" OR abs:"red team data") AND (abs:curat OR abs:synthes OR abs:select OR abs:audit)',
    "b10_generation_moderation_loop": '(abs:"generate then filter" OR abs:"safety checker" OR abs:"post-hoc" OR abs:"generation-time") AND (abs:image OR abs:diffusion OR abs:generation)',
    "b11_edit_model_bench": '(abs:edit OR abs:editing) AND (abs:benchmark OR abs:"evaluation suite" OR abs:"human evaluation") AND (abs:image OR abs:instruction)',
    "b12_visual_harm_taxonomy": '(abs:"harm" OR abs:"risk") AND (abs:"visual" OR abs:"image") AND (abs:"taxonomy" OR abs:"ontology" OR abs:"guideline" OR abs:"definition")',
}

KW = {
    "image editing": 6, "editing instruction": 5, "instruction-based": 4, "instruction-guided": 4,
    "image edit": 4, "inpaint": 2, "editing": 2, "photo editing": 5, "edit request": 5,
    "prompt rewrit": 6, "rewrit": 4, "sanitiz": 5, "rephras": 4, "paraphrase": 3,
    "query rewrite": 4, "query reformulation": 4,
    "intent-preserving": 5, "semantic fidelity": 5, "semantic preserv": 4,
    "moderation": 5, "guardrail": 4, "guard model": 4, "guard": 2, "prompt guard": 5,
    "nsfw": 5, "sexual content": 4, "safety filter": 4, "safety classifier": 4,
    "content filter": 4, "output filter": 4,
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


def build_sq(q, f, t):
    return f"{CATS} AND ({q}) AND submittedDate:[{f}0000 TO {t}2359]"


def fetch(sq, start=0, n=200, retries=4):
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(sq)
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
        xml = fetch(build_sq(q, FROM_DATE.replace("-", ""), TO_DATE.replace("-", "")))
        page = parse(xml)
        batch = [p for p in page if FROM_DATE <= p["published"] <= TO_DATE]
        got.extend(batch)
        if len(page) < 200 or start >= 600:
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
