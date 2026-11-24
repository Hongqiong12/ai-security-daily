#!/usr/bin/env python3
"""2026-11-24 分层筛选（全部在 /tmp/full_1124.json 本地池上复现，零检索请求）。

按用户检索供给策略：
① 主题词检索（本地正则复现，覆盖 (1)-(5) 五个方向）
② 主线零命中时改按批次全量扫描（全批池已含十分类，逐篇 title+abstract 判可迁移性）
③ 方法论形态通道（校准/风险控制/一致性/奖励设计/数据重加权/评测集构建，不绑安全语义）
④ 会议接收列表/模型卡/厂商技术报告兜底（在报告层补，不在本脚本）
输出 /tmp/cand_1124.json 候选池供逐篇核验。
"""
import json, re, os, glob
from collections import Counter

papers = json.load(open("/tmp/full_1124.json"))
have = set()
for p in glob.glob("categories/*/papers/*.md"):
    have.add(os.path.basename(p).split("_")[0])

print("POOL", len(papers), "| 磁盘已建档", len(have),
      "| 带摘要", sum(1 for p in papers if p.get("abstract")))
print("DATES", dict(sorted(Counter(p["published"] for p in papers).items())))
CATS = Counter(c for p in papers for c in p["cats"])
print("TOP CATS", dict(CATS.most_common(14)))
fresh = [p for p in papers if p["id"].split("v")[0] not in have]
print("NOT-collected:", len(fresh))
print("FRESH DATES", dict(sorted(Counter(p["published"] for p in fresh).items())))

NSFW = re.compile(r"\b(NSFW|nude|nudity|naked|pornograph\w*|obscen\w*|vulgar\w*|sexual content|explicit content|adult content)\b", re.I)
MOD = re.compile(r"(image moderation|content moderation|safety classifier|safety filter|guard model|guardrail|image safety|harmful image|unsafe image|moderation model)", re.I)
REWRITE = re.compile(r"(rewrit\w*|rephras\w*|sanitiz\w*|paraphras\w*)", re.I)
SAFE = re.compile(r"(saf\w*|harm\w*|toxic\w*|policy|risk|NSFW|moderation)", re.I)
GEN = re.compile(r"(text-to-image|t2i|image generation|image generator|diffusion model|diffusion transformer|generative model|image editing|image editor|editing instruction|instruction-based editing|unified .*generation|image synthesis|visual generation)", re.I)
EDIT = re.compile(r"(image editing|image editor|editing instruction|instruction-based editing|unified .*generation|editing model|edit benchmark|image edit)", re.I)
WM = re.compile(r"(watermark|provenance|AIGC detection|image forensics|deepfake detection)", re.I)

# ② 主题词通道：覆盖方向 (1)-(5)
THEMED = {
    "t1_t2i_safety": [re.compile(r"(text-to-image|image generation|diffusion)", re.I), re.compile(r"(safety|harmful|NSFW|moderation|guard)", re.I)],
    "t2_prompt_rewrite": [re.compile(r"(prompt rewrite|prompt rewriting|safety rewriting|sanitiz|safe rephras|intent-preserving|prompt sanitization)", re.I)],
    "t3_i2i_edit_safety": [re.compile(r"(image editing|editing instruction|instruction-based editing|image edit)", re.I), re.compile(r"(safety|guard|harm|refus|moderation)", re.I)],
    "t4_image_moderation": [re.compile(r"(content moderation|image moderation|NSFW|safety classifier|image safety|image-only|VLM-as-judge)", re.I)],
    "t5_watermark": [re.compile(r"(watermark|provenance|AIGC detection|deepfake detection)", re.I)],
    "t6_concept_erasure": [re.compile(r"(concept erasure|machine unlearning|concept unlearning|safe latent|inference-time guidance|negative prompt|classifier-free guidance)", re.I)],
    "t7_threshold": [re.compile(r"(operating point|threshold calibration|conformal|misblock|false positive|precision-recall|per-category threshold)", re.I)],
    "t8_hard_negative": [re.compile(r"(hard negative|hard-negative mining|data curation|active learning|label audit|label noise)", re.I)],
    "t9_unified_edit": [re.compile(r"unified", re.I), re.compile(r"(generation and editing|image editing|generation and understanding)", re.I)],
    "t10_video_safety": [re.compile(r"(video generation|text-to-video|image-to-video)", re.I), re.compile(r"(safety|moderation|harm|guard)", re.I)],
    "t11_multilingual": [re.compile(r"(multilingual|cross-lingual|code-switch|code-mixing|language drift|translation)", re.I), re.compile(r"(safety|harm|ASR|attack success|rewrite|moderation)", re.I)],
    "t12_overrefusal": [re.compile(r"(over-refusal|overrefusal|helpfulness|refusal calibration|false refusal|abstention budget)", re.I)],
    "t13_rl_rewrite": [re.compile(r"(GRPO|group relative policy|verifiable reward|reward hacking|RLHF.*rewrit|reinforcement learning.*rewrit|edit rate|Levenshtein)", re.I)],
    "t14_policy_guard": [re.compile(r"(in-context policy|configurable guardrail|policy guardrailing|policy-as-|risk knowledge|L0/L1/L2|hot update|lexicon.*retrieval|vector retrieval|hybrid retrieval)", re.I)],
    "t15_eval_regression": [re.compile(r"(eval set|eval harness|version regression|macro average|aggregate.*diverge|per-class regression|shadow deployment|canary|PSI|drift)", re.I)],
    "t16_inference_accel": [re.compile(r"(vLLM|SGLang|prefix caching|continuous batching|fp8|fp4|quantization.*safety|TTFT|single-token|max_tokens|speculative decoding)", re.I)],
    "t17_ordinal_taxonomy": [re.compile(r"(ordinal calibration|hierarchical label|severity level|taxonom|fine-grained risk|tag-weighted|CoT tag|class-weighted)", re.I)],
    "t18_generated_risk": [re.compile(r"(generated-image|inherent risk|rewrite-then-block|spatial classifier guidance|safe guidance|generation-time|inference-time|step-wise steeri|latent steeri)", re.I)],
}

# ③ 方法论形态通道（不绑安全语义）
FORMS = {
    "f1_calibration": [re.compile(r"(calibration|calibrated|confidence calibration)", re.I)],
    "f2_risk_control": [re.compile(r"(risk control|risk-controlling|conformal prediction|error rate control|risk-certified)", re.I)],
    "f3_consistency": [re.compile(r"(consistency measure|semantic consistency|fidelity metric|preservation rate|semantic fidelity)", re.I)],
    "f4_reward_design": [re.compile(r"(reward design|verifiable reward|reward hacking|reward model|bounded reward)", re.I)],
    "f5_reweighting": [re.compile(r"(reweighting|importance weighting|distribution shift correction|downsampling|resampling)", re.I)],
    "f6_eval_set": [re.compile(r"(evaluation set|eval harness|benchmark construction|test set construction|evaluation protocol)", re.I)],
    "f7_regression": [re.compile(r"(version regression|per-class|macro average|aggregate metric|paired control)", re.I)],
    "f8_ordinal": [re.compile(r"(ordinal|rank calibration|graded label|severity level)", re.I)],
    "f9_abstention": [re.compile(r"(abstention|selective prediction|reject option|coverage)", re.I)],
    "f10_telemetry": [re.compile(r"(observability|telemetry|audit log|shadow deployment|canary|event logging)", re.I)],
    "f11_attribution": [re.compile(r"(failure attribution|root cause|case attribution|error analysis|counterfactual control)", re.I)],
    "f12_paired_control": [re.compile(r"(paired control|matched control|twin sample|placebo control|invariant control|ablation control)", re.I)],
}


def show(tag, rx_list, pool=None, limit=40):
    pool = pool if pool is not None else papers
    hits = [p for p in pool if all(r.search(p["title"] + " " + p.get("abstract", "")) for r in rx_list)]
    print("\n[%s] %d" % (tag, len(hits)))
    for p in hits[:limit]:
        print("  %s [%s] | %s" % (p["id"], p["published"], p["title"][:110]))
    return hits


print("\n========== ① 严格分层 ==========")
show("NSFW strict (whole pool)", [NSFW])
show("moderation", [MOD])
show("rewrite x safe", [REWRITE, SAFE])
show("gen x safe", [GEN, SAFE], limit=30)
show("edit structure", [EDIT], limit=40)
show("watermark/provenance", [WM], limit=30)

print("\n========== ② 主题词通道（本地复现，覆盖方向 1-5） ==========")
for k, v in THEMED.items():
    show(k, v, limit=16)

print("\n========== ③ 方法论形态通道（本地复现，不绑安全语义） ==========")
for k, v in FORMS.items():
    show(k, v, limit=16)

# ④ 候选池：fresh 里与任一形态/主题/审核/编辑/水印/校准相关的，供逐篇判读
INTEREST = [NSFW, MOD, GEN, EDIT, WM] + [r for v in THEMED.values() for r in v] + [r for v in FORMS.values() for r in v]
cand = [p for p in fresh if any(r.search(p["title"] + " " + p.get("abstract", "")) for r in INTEREST)]
print("\n\n========== ④ CAND POOL (fresh & any signal) %d ==========" % len(cand))
for p in cand:
    print("  %s [%s] | %s" % (p["id"], p["published"], p["title"][:110]))

json.dump([{"id": p["id"], "t": p["title"], "d": p["published"], "a": p.get("abstract", ""),
            "c": p.get("cats", []), "au": p.get("authors", ""), "cm": p.get("comments", "")}
           for p in cand], open("/tmp/cand_1124.json", "w"), ensure_ascii=False, indent=1)
json.dump([{"id": p["id"], "t": p["title"], "d": p["published"], "a": p.get("abstract", "")}
           for p in fresh], open("/tmp/fresh_1124.json", "w"), ensure_ascii=False, indent=1)
