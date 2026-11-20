#!/usr/bin/env python3
"""通道③ 2026-11-12：方法论形态扫描（不绑安全语义），只看结构可迁移性。
重点输出 11-10 新批次命中，避免重复已归零的主题查询。"""
import json, re
from collections import Counter

papers = json.load(open("/tmp/full_1112.json"))

FORMS = {
    "F1_calibration_ordinal": r"(ordinal|calibration error|ECE|temperature scaling|probability calibration|rank consistency)",
    "F2_risk_control_conformal": r"(conformal|risk control|guarantee\w* coverage|distribution-free|PAC bound)",
    "F3_threshold_operating": r"(operating point|decision threshold|precision-recall trade|cost-sensitive|threshold tuning)",
    "F4_reweight_resample": r"(reweight\w*|resampl\w*|class imbalance|long-tail\w*|importance weight)",
    "F5_active_label_audit": r"(active learning|label noise|annotation\w* (quality|audit)|inter-annotator|human-in-the-loop)",
    "F6_reward_design_consistency": r"(reward model|reward hacking|verifier|consistency reward|reward design)",
    "F7_eval_harness_regression": r"(eval\w* harness|benchmark suite|regression testing|version comparison|leaderboard)",
    "F8_distill_efficiency": r"(LoRA|QLoRA|distill\w*|quantiz\w*|packing|zero redundancy|ZeRO|gradient checkpoint)",
    "F9_negation_composition": r"(negation|negated|compositional binding|attribute binding|counting)",
    "F10_drift_monitoring": r"(distribution shift|drift detection|PSI|monitoring|telemetry|observability)",
    "F11_abstain_selective": r"(abstention|selective prediction|reject option|coverage|defer)",
    "F12_pairwise_control": r"(paired|paired audit|matched samples|twin|counterfactual pair|control group)",
}

for name, rx in FORMS.items():
    r = re.compile(rx, re.I)
    hits = [p for p in papers if r.search(p["title"] + " " + p["abstract"])]
    d10 = [p for p in hits if p["published"] == "2026-11-10"]
    print("\n=== %s : %d (11-10: %d)" % (name, len(hits), len(d10)))
    for p in d10[:15]:
        print("  [D10] %s | %s" % (p["id"], p["title"][:110]))
    for p in [x for x in hits if x["published"] != "2026-11-10"][:8]:
        print("     %s [%s] | %s" % (p["id"], p["published"], p["title"][:105]))
