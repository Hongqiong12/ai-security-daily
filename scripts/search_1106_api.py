#!/usr/bin/env python3
"""arXiv API 检索通道 —— 2026-11-06 日报，窗口 2026-10-30 ~ 2026-11-05。

供给侧探测（11-06 00:0x）: cat:cs.CV 最新 published = 11-04(111) / 11-03(169) / 11-02(20)，11-05 未生成
  ⇒ 相对 11-05 那轮（最新 11-03），本轮新增 11-04 一个批次。

供给侧探测（11-03 00:0x）: 最新 published 批次 = 2026-10-30（单查询 cs.CV+cs.CR & abs:safety 口径下
  10-21:9 / 10-22:9 / 10-23:5 / 10-24:2 / 10-25:3 / 10-26:10 / 10-27:7 / 10-28:4 / 10-29:10 / 10-30:1）
  ⇒ 相对 11-02 那轮（最新 10-29），本轮**只新增 10-30 一个批次**。10-31/11-01 为周末，
    11-02（周一）/11-03 批次在 00:00 尚未生成 ⇒ 本轮新增供给极小，属「薄供给轮」。

本轮相对 11-02 的变化:
 1) 窗口前移 10-26→10-27（10-26 已在 10-30 / 11-02 两轮扫过）。
 2) 保留 11-02 全部 54 路作为基座，便于跨轮比对「哪一路归零」。
 3) 新增 8 路（d1-d8），针对本轮 prompt 强化的四个新缺口：
    - 分业务粒度阈值管控 / per-category operating point 校准（误杀-漏过联合优化）
    - eval harness / 版本回归看板
    - hard negative mining
    - I2V/T2V 视频生成安全（AIGC 全模态落表）

用法: python3 scripts/search_1104_api.py > /tmp/papers_1103_api.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request

FROM_DATE = "2026-10-30"
TO_DATE = "2026-11-05"

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

    # ================= 10-30 新增 12 路口语化 / 产品化查询 =================
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

    # ================= 11-02 新增 8 路：I2I 编辑安全改写 + 图审 AB =================
    "c1_edit_policy_refusal": '(abs:"editing" OR abs:"edit") AND (abs:refus OR abs:"policy violation" OR abs:"harmful instruction" OR abs:"unsafe instruction") AND (abs:image OR abs:visual OR abs:multimodal)',
    "c2_edit_guardrail": '(abs:"guardrail" OR abs:"shielding" OR abs:"protect") AND (abs:"image editing" OR abs:"image-to-image" OR abs:"generative editing")',
    "c3_instruction_sanitize": '(abs:"instruction" OR abs:"prompt") AND (abs:sanitiz OR abs:"decomposition" OR abs:"decompose" OR abs:"clarif") AND (abs:safety OR abs:risk OR abs:harm)',
    "c4_generated_image_filter": '(abs:"generated image" OR abs:"synthetic image") AND (abs:detect OR abs:filter OR abs:moderat OR abs:classif) AND (abs:NSFW OR abs:unsafe OR abs:harm OR abs:policy)',
    "c5_ab_compare_judge": '(abs:"two" OR abs:"pairwise" OR abs:"A/B") AND (abs:judge OR abs:annotator OR abs:model) AND (abs:disagree OR abs:agreement OR abs:calibrat) AND (abs:safety OR abs:moderation OR abs:content)',
    "c6_tag_weighted_loss": '(abs:"class imbalance" OR abs:"weighted loss" OR abs:"reweight" OR abs:"long-tail") AND (abs:classif OR abs:"fine-tune" OR abs:training) AND (abs:safety OR abs:harm OR abs:moderation OR abs:risk)',
    "c7_region_culture_safety": '(abs:"culture" OR abs:"regional" OR abs:"localized" OR abs:"jurisdiction") AND (abs:safety OR abs:moderation OR abs:policy) AND (abs:LLM OR abs:multimodal OR abs:model)',
    "c8_reasoning_distill_guard": '(abs:"reasoning" OR abs:"rationale") AND (abs:distill OR abs:"small model" OR abs:"compact") AND (abs:safety OR abs:moderation OR abs:guard OR abs:classif)',

    # ================= 11-03 新增 8 路：阈值 operating point / eval harness / hard negative / 视频 =================
    "d1_threshold_operating_point": '(abs:"operating point" OR abs:threshold OR abs:"precision-recall" OR abs:calibration) AND (abs:moderation OR abs:"false positive" OR abs:"false negative" OR abs:misclassif OR abs:escalat)',
    "d2_eval_harness_regression": '(abs:"evaluation harness" OR abs:"regression" OR abs:"eval suite" OR abs:"model version" OR abs:"benchmark contamination") AND (abs:safety OR abs:moderation OR abs:evaluation)',
    "d3_hard_negative": '(abs:"hard negative" OR abs:"hard example" OR abs:"contrastive" OR abs:"boundary case") AND (abs:classif OR abs:detect OR abs:moderation OR abs:safety)',
    "d4_video_generation_safety": '(abs:"video generation" OR abs:text-to-video OR abs:"image-to-video" OR abs:"video diffusion") AND (abs:safety OR abs:harmful OR abs:NSFW OR abs:moderation OR abs:guard)',
    "d5_video_temporal_risk": '(abs:"temporal" OR abs:"frame-level" OR abs:"temporal consistency") AND (abs:moderation OR abs:safety) AND (abs:video OR abs:sequence)',
    "d6_cascade_routing": '(abs:"cascade" OR abs:"routing" OR abs:"escalation" OR abs:"two-stage") AND (abs:moderation OR abs:classif OR abs:guard OR abs:safety)',
    "d7_safety_telemetry": '(abs:"observability" OR abs:telemetry OR abs:"audit log" OR abs:"incident" OR abs:"attribution") AND (abs:safety OR abs:moderation OR abs:guardrail)',
    "d8_sensitive_image_pii": '(abs:"sensitive image" OR abs:"private image" OR abs:"identity document" OR abs:"face recognition") AND (abs:detect OR abs:moderat OR abs:privac OR abs:risk)',

    # ================= 11-04 新增 8 路：供给解冻轮定向补齐 =================
    "e1_safety_rewriting_t2i": '(abs:"safety rewriting" OR abs:"safety-aware" OR abs:"safe rewrite" OR abs:"safety rewrite") AND (abs:image OR abs:prompt OR abs:diffusion OR abs:generation)',
    "e2_policy_granularity": '(abs:"policy" OR abs:"guideline") AND (abs:granularity OR abs:"leaf" OR abs:"subcategory" OR abs:"category-level" OR abs:"per-category") AND (abs:moderation OR abs:safety OR abs:vulnerab)',
    "e3_guardrail_t2i": '(abs:guardrail OR abs:"safety check") AND (abs:"text-to-image" OR abs:"image generation" OR abs:"image generator" OR abs:"generative model")',
    "e4_unlearn_diffusion": '(abs:unlearn OR abs:erasure OR abs:forget) AND (abs:diffusion OR abs:"text-to-image" OR abs:"image generation")',
    "e5_edit_distance_constraint": '(abs:"edit distance" OR abs:Levenshtein OR abs:"minimal edit" OR abs:"edit rate") AND (abs:rewrite OR abs:prompt OR abs:text)',
    "e6_prompt_perturb_safety": '(abs:"prompt perturbation" OR abs:"prompt variation" OR abs:"prompt sensitivity" OR abs:"paraphrase robustness") AND (abs:safety OR abs:moderation OR abs:judge OR abs:classif)',
    "e7_image_safety_bench": '(abs:"image safety" OR abs:"safety benchmark" OR abs:"safety evaluation") AND (abs:image OR abs:vision OR abs:generation)',
    "e8_moderation_sft": '(abs:SFT OR abs:"supervised fine-tuning" OR abs:"instruction tuning") AND (abs:moderation OR abs:"content safety" OR abs:"risk classification")',

    # ================= 11-05 新增 8 路：按用户六条主线定向补齐 =================
    "f1_rewrite_industrial": '(abs:"rewriting" OR abs:"refine" OR abs:"refinement") AND (abs:"safety" OR abs:"policy") AND (abs:"image" OR abs:"visual") AND (abs:"prompt" OR abs:"instruction")',
    "f2_semantic_edit_metric": '(abs:"semantic" OR abs:"intent") AND (abs:"metric" OR abs:"measure" OR abs:"evaluat") AND (abs:"editing" OR abs:"rewriting" OR abs:"rewrite")',
    "f3_t2i_redteam_report": '(abs:"text-to-image" OR abs:"image generation model" OR abs:"generative image") AND (abs:"report" OR abs:"deployment" OR abs:"production" OR abs:"industry")',
    "f4_moderation_taxonomy_hier": '(abs:"hierarchical classification" OR abs:"label hierarchy" OR abs:"category tree" OR abs:"multi-level") AND (abs:"content" OR abs:"harm" OR abs:"safety")',
    "f5_threshold_per_category": '(abs:"per-class" OR abs:"class-wise" OR abs:"class-specific" OR abs:"category-specific") AND (abs:"threshold" OR abs:"calibrat" OR abs:"operating")',
    "f6_regression_dashboard": '(abs:"version" OR abs:"iteration") AND (abs:"regression" OR abs:"dashboard" OR abs:"leaderboard" OR abs:"comparison") AND (abs:"model" OR abs:"evaluation") AND (abs:safety OR abs:moderation OR abs:quality)',
    "f7_active_label_audit": '(abs:"active learning" OR abs:"weak supervision" OR abs:"label audit" OR abs:"human-in-the-loop" OR abs:"annotation") AND (abs:"safety" OR abs:"moderation" OR abs:"harm")',
    "f8_vlm_image_judge": '(abs:"vision-language model" OR abs:VLM OR abs:MLLM) AND (abs:"judge" OR abs:"evaluator" OR abs:"classifier") AND (abs:"safety" OR abs:"harm" OR abs:"moderation" OR abs:"NSFW")',

    # ================= 11-06 新增 8 路：本轮六个缺口定向补齐 =================
    "g1_edit_safety_product": '(abs:"image editing" OR abs:"image editor" OR abs:"editing model" OR abs:"editing system") AND (abs:risk OR abs:policy OR abs:violat OR abs:malicious OR abs:attack)',
    "g2_safe_edit_data": '(abs:editing OR abs:edit) AND (abs:dataset OR abs:data OR abs:corpus) AND (abs:safety OR abs:harmful OR abs:unsafe OR abs:refus)',
    "g3_multihead_moderation": '(abs:"multi-label" OR abs:"multi-task" OR abs:"multi-head" OR abs:"multi-class") AND (abs:moderation OR abs:"content safety" OR abs:NSFW OR abs:harm)',
    "g4_leakage_shortcut": '(abs:contamination OR abs:leakage OR abs:shortcut OR abs:"spurious correlation") AND (abs:benchmark OR abs:evaluation OR abs:dataset) AND (abs:safety OR abs:moderation OR abs:vision OR abs:image)',
    "g5_rl_rewrite_pref": '(abs:GRPO OR abs:DPO OR abs:"preference optimization" OR abs:"policy gradient") AND (abs:rewrite OR abs:rewriting OR abs:refine OR abs:reformulat)',
    "g6_porn_vulgar_explicit": '(abs:porn OR abs:vulgar OR abs:obscene OR abs:"explicit content" OR abs:"adult content")',
    "g7_moderation_deployment": '(abs:deployed OR abs:production OR abs:"real-world deployment" OR abs:serving OR abs:"online system") AND (abs:moderation OR abs:"safety system" OR abs:guardrail OR abs:"content safety")',
    "g8_distill_safety_vision": '(abs:distill OR abs:"teacher model" OR abs:"compact model" OR abs:"small model") AND (abs:safety OR abs:guard OR abs:moderation) AND (abs:vision OR abs:image OR abs:multimodal)',
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
    "operating point": 5, "threshold": 3, "calibration": 4, "false positive": 4,
    "hard negative": 4, "video generation": 4, "text-to-video": 4, "temporal": 2,
    "cascade": 3, "routing": 3, "regression": 4, "harness": 4,
    "safety rewriting": 5, "safe rewrite": 5, "policy granularity": 5, "per-category": 5,
    "unlearn": 3, "edit distance": 4, "levenshtein": 4, "paraphrase robustness": 4,
    "image safety": 4, "sft": 3, "image generator": 4, "leaf": 3,
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
        xml = fetch(build_sq(q, FROM_DATE.replace("-", ""), TO_DATE.replace("-", "")), start=start)
        page = parse(xml)
        batch = [p for p in page if FROM_DATE <= p["published"] <= TO_DATE]
        got.extend(batch)
        if len(page) < 200 or start >= 400:
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
