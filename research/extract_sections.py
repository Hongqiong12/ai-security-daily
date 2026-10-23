#!/usr/bin/env python3
"""按标题锚点抽取论文章节文本，供六模块精读使用"""
import re
import sys
import time
import urllib.request

TARGETS = {
    "2610.24508": ["4 Learning the Divergence", "4.2 A Family of Potentials", "4.3 Selecting a Potential",
                   "5 Experiments", "6 Conclusion"],
    "2610.28195": ["3.3 Reward Models Inherit the Bias", "4 Mitigation", "5 Discussion"],
    "2610.27516": ["Evaluation Criteria and HealScore", "Tri-dimensional Heal Scorer",
                   "Prompt Rewriting as Intervention", "Exploratory RL Fine-Tuning with THS Reward", "Conclusion"],
    "2610.22068": ["IV-B Risk-Conditioned Uncertainty Estimation", "IV-D Outer Loop",
                   "IV-E Composite Reward", "VI-B Main Results", "VI-D Over-Refusal Analysis"],
    "2610.27728": ["3.2 Non-Target Logit Over-Suppression", "4.1 Confusion-based Instance-wise LA",
                   "4.2 Batch-adaptation Noise-Injection", "5.1 Experimental Results"],
    "2610.25215": ["3 Preliminary: Training Dynamics Score", "4.2 HC Algorithm", "6.2.2 Domin Experiments"],
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def strip(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


for pid, anchors in TARGETS.items():
    print("#" * 100)
    print("ID:", pid)
    try:
        t = strip(get(f"https://arxiv.org/html/{pid}v1"))
    except Exception as e:
        print("ERR", e)
        continue
    for a in anchors:
        idx = t.find(a)
        if idx < 0:
            print(f"\n--- [{a}] NOT FOUND")
            continue
        # 跳过锚点自身重复
        idx = t.find(a, idx + len(a) - 1) if t.count(a) > 1 else idx
        print(f"\n--- [{a}] ---")
        print(t[idx:idx + 2600])
    time.sleep(3)
