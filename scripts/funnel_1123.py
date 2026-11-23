#!/usr/bin/env python3
"""2026-11-23 分层筛选（全部在 /tmp/full_1123.json 本地池上复现，零 API 请求）。

① 严格词边界 NSFW / 审核 / 改写×安全 / 生成×安全 / 编辑结构 / 水印溯源
② 主题词 10 路（等价于 themed 通道的本地正则复现）
③ 方法论形态 10 路（等价于 forms 通道的本地正则复现，不绑安全语义）
④ 与磁盘已建档做差集，输出候选池供逐篇 title+abstract 判读
"""
import json, re, os, glob
from collections import Counter

papers = json.load(open("/tmp/full_1123.json"))
have = set()
for p in glob.glob("categories/*/papers/*.md"):
    have.add(os.path.basename(p).split("_")[0])

print("POOL", len(papers), "| 磁盘已建档", len(have))
print("DATES", dict(sorted(Counter(p["published"] for p in papers).items())))
CATS = Counter(c for p in papers for c in p["cats"])
print("TOP CATS", dict(CATS.most_common(14)))
fresh = [p for p in papers if p["id"].split("v")[0] not in have]
print("NOT-collected:", len(fresh))
print("FRESH DATES", dict(sorted(Counter(p["published"] for p in fresh).items())))

NSFW = re.compile(r"\b(NSFW|nude|nudity|naked|pornograph\w*|obscen\w*|vulgar\w*|sexual content|explicit content|adult content)\b", re.I)
MOD = re.compile(r"(image moderation|content moderation|safety classifier|safety filter|guard model|guardrail|image safety|harmful image|unsafe image|moderation model)", re.I)
REWRITE = re.compile(r"(rewrit\w*|rephras\w*|sanitiz\w*|paraphras\w*)", re.I)
SAFE = re.compile(r"(saf\w*|harm\w*|toxic\w*|policy|risk)", re.I)
GEN = re.compile(r"(text-to-image|t2i|image generation|image generator|diffusion model|diffusion transformer|generative model|image editing|image editor|editing instruction|instruction-based editing|unified .*generation|image synthesis|visual generation)", re.I)
EDIT = re.compile(r"(image editing|image editor|editing instruction|instruction-based editing|unified .*generation|editing model|edit benchmark|image edit)", re.I)
WM = re.compile(r"(watermark|provenance|AIGC detection|image forensics)", re.I)

# ② 主题词通道本地复现
THEMED = {
    "t1_t2i_safety": [re.compile(r"(text-to-image|image generation)", re.I), re.compile(r"(safety|harmful|NSFW)", re.I)],
    "t2_prompt_rewrite": [re.compile(r"(prompt rewrite|prompt rewriting|safety rewriting|sanitiz|rephras)", re.I)],
    "t3_i2i_edit_safety": [re.compile(r"(image editing|editing instruction|instruction-based editing)", re.I), re.compile(r"(safety|guard|harm|refus)", re.I)],
    "t4_image_moderation": [re.compile(r"(content moderation|image moderation|NSFW|safety classifier|image safety)", re.I)],
    "t5_watermark": [re.compile(r"(watermark|provenance|AIGC detection)", re.I), re.compile(r"(image|diffusion)", re.I)],
    "t6_concept_erasure": [re.compile(r"(concept erasure|machine unlearning|concept unlearning)", re.I), re.compile(r"(diffusion|image)", re.I)],
    "t7_threshold": [re.compile(r"(operating point|threshold calibration|conformal|misclassification rate)", re.I)],
    "t8_hard_negative": [re.compile(r"(hard negative|hard-negative mining|data curation|active learning)", re.I)],
    "t9_unified_edit": [re.compile(r"unified", re.I), re.compile(r"(generation and editing|image editing)", re.I)],
    "t10_video_safety": [re.compile(r"(video generation|text-to-video)", re.I), re.compile(r"(safety|moderation|harm)", re.I)],
}

# ③ 方法论形态通道本地复现（不绑安全语义）
FORMS = {
    "f1_calibration": [re.compile(r"(calibration|calibrated|confidence calibration)", re.I)],
    "f2_risk_control": [re.compile(r"(risk control|risk-controlling|conformal prediction|error rate control)", re.I)],
    "f3_consistency": [re.compile(r"(consistency measure|semantic consistency|fidelity metric|preservation rate)", re.I)],
    "f4_reward_design": [re.compile(r"(reward design|verifiable reward|reward hacking|reward model)", re.I)],
    "f5_reweighting": [re.compile(r"(reweighting|importance weighting|distribution shift correction|downsampling)", re.I)],
    "f6_eval_set": [re.compile(r"(evaluation set|eval harness|benchmark construction|test set construction)", re.I)],
    "f7_regression": [re.compile(r"(version regression|per-class|macro average|aggregate metric)", re.I)],
    "f8_ordinal": [re.compile(r"(ordinal|rank calibration|graded label|severity level)", re.I)],
    "f9_abstention": [re.compile(r"(abstention|selective prediction|reject option|coverage)", re.I)],
    "f10_telemetry": [re.compile(r"(observability|telemetry|audit log|shadow deployment|canary)", re.I)],
}


def show(tag, rx_list, pool=None, limit=40):
    pool = pool if pool is not None else papers
    hits = [p for p in pool if all(r.search(p["title"] + " " + p["abstract"]) for r in rx_list)]
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

print("\n========== ② 主题词 10 路（本地复现） ==========")
for k, v in THEMED.items():
    show(k, v, limit=18)

print("\n========== ③ 方法论形态 10 路（本地复现） ==========")
for k, v in FORMS.items():
    show(k, v, limit=18)

# ④ 候选池：fresh 里与任一形态/主题/审核/编辑/水印/校准相关的，供逐篇判读
INTEREST = [NSFW, MOD, GEN, EDIT, WM] + [r for v in THEMED.values() for r in v] + [r for v in FORMS.values() for r in v]
cand = [p for p in fresh if any(r.search(p["title"] + " " + p["abstract"]) for r in INTEREST)]
print("\n\n========== ④ CAND POOL (fresh & any signal) %d ==========" % len(cand))
for p in cand:
    print("  %s [%s] | %s" % (p["id"], p["published"], p["title"][:110]))

json.dump([{"id": p["id"], "t": p["title"], "d": p["published"], "a": p["abstract"]}
           for p in cand], open("/tmp/cand_1123.json", "w"), ensure_ascii=False, indent=1)
json.dump([{"id": p["id"], "t": p["title"], "d": p["published"], "a": p["abstract"]}
           for p in fresh], open("/tmp/fresh_1123.json", "w"), ensure_ascii=False, indent=1)
