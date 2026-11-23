#!/usr/bin/env python3
"""2026-11-23 检索：主题词通道 + 方法论形态通道 + 十分类全批扫描。

纪律（来自 automation memory 11-06/11-08/11-09/11-10 四轮固化）：
① 主题词检索；② 主线零命中 → 十分类按批次全量扫描（不绑安全词，逐篇
   title+abstract 判可迁移性）；③ 仍不足 → 方法论形态通道（不绑安全语义）；
④ 会议接收列表 / 模型卡 / 厂商技术报告兜底。
主线自 11-09 起默认按零供给规划，故 ②③ 为常规动作而非应急动作。

用法:
  python3 scripts/search_1123_api.py full   > /tmp/full_1123.json
  python3 scripts/search_1123_api.py themed > /tmp/themed_1123.json
  python3 scripts/search_1123_api.py forms  > /tmp/forms_1123.json
"""
import re, json, time, sys, urllib.parse, urllib.request

FROM_TS = "202611160000"
TO_TS = "202611232359"

CATS = ("(cat:cs.CV OR cat:cs.CR OR cat:cs.CL OR cat:cs.LG OR cat:cs.AI "
        "OR cat:cs.MM OR cat:cs.RO OR cat:cs.HC OR cat:cs.SE OR cat:eess.IV)")

ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)


def _t(tag, block):
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), block, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def fetch(query, max_results=8000):
    out, start = [], 0
    seen = set()
    while start < max_results:
        params = {"search_query": query, "start": start, "max_results": 200,
                  "sortBy": "submittedDate", "sortOrder": "descending"}
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        for attempt in range(6):
            try:
                data = urllib.request.urlopen(req, timeout=90).read().decode()
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(8 + 8 * attempt)
        entries = ENTRY_RE.findall(data)
        if not entries:
            break
        for e in entries:
            aid = _t("id", e).split("/abs/")[-1]
            if aid in seen:
                continue
            seen.add(aid)
            out.append({"id": aid, "title": _t("title", e),
                        "abstract": _t("summary", e),
                        "published": _t("published", e)[:10],
                        "cats": re.findall(r'term="([^"]+)"', e)})
        if len(entries) < 200:
            break
        start += 200
        time.sleep(5.0)
    return out


# ① 主题词通道（绑安全语义）
THEMED = {
    "t1_t2i_safety": '(abs:"text-to-image" OR abs:"image generation") AND (abs:safety OR abs:harmful OR abs:NSFW)',
    "t2_prompt_rewrite": '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"safety rewriting" OR abs:"sanitiz" OR abs:"rephras")',
    "t3_i2i_edit_safety": '(abs:"image editing" OR abs:"editing instruction" OR abs:"instruction-based editing") AND (abs:safety OR abs:guard OR abs:harm OR abs:refus)',
    "t4_image_moderation": '(abs:"content moderation" OR abs:"image moderation" OR abs:NSFW OR abs:"safety classifier" OR abs:"image safety")',
    "t5_watermark": '(abs:watermark OR abs:provenance OR abs:"AIGC detection") AND (abs:image OR abs:diffusion)',
    "t6_concept_erasure": '(abs:"concept erasure" OR abs:"machine unlearning" OR abs:"concept unlearning") AND (abs:diffusion OR abs:image)',
    "t7_threshold": '(abs:"operating point" OR abs:"threshold calibration" OR abs:conformal OR abs:"misclassification rate")',
    "t8_hard_negative": '(abs:"hard negative" OR abs:"hard-negative mining" OR abs:"data curation" OR abs:"active learning")',
    "t9_unified_edit": '(abs:unified AND (abs:"generation and editing" OR abs:"image editing"))',
    "t10_video_safety": '(abs:"video generation" OR abs:"text-to-video") AND (abs:safety OR abs:moderation OR abs:harm)',
}

# ③ 方法论形态通道（不绑安全语义）——校准 / 风险控制 / 一致性度量 /
#    奖励设计 / 数据重加权 / 评测集构建 / 序数校准 / 回归对比 / 覆盖稳定性
FORMS = {
    "f1_calibration": '(abs:calibration OR abs:calibrated OR abs:"confidence calibration")',
    "f2_risk_control": '(abs:"risk control" OR abs:"risk-controlling" OR abs:"conformal prediction" OR abs:"error rate control")',
    "f3_consistency": '(abs:"consistency measure" OR abs:"semantic consistency" OR abs:"fidelity metric" OR abs:"preservation rate")',
    "f4_reward_design": '(abs:"reward design" OR abs:"verifiable reward" OR abs:"reward hacking" OR abs:"reward model")',
    "f5_reweighting": '(abs:reweighting OR abs:"importance weighting" OR abs:"distribution shift correction" OR abs:downsampling)',
    "f6_eval_set": '(abs:"evaluation set" OR abs:"eval harness" OR abs:"benchmark construction" OR abs:"test set construction")',
    "f7_regression": '(abs:"version regression" OR abs:"per-class" OR abs:"macro average" OR abs:"aggregate metric")',
    "f8_ordinal": '(abs:"ordinal" OR abs:"rank calibration" OR abs:"graded label" OR abs:"severity level")',
    "f9_abstention": '(abs:abstention OR abs:"selective prediction" OR abs:"reject option" OR abs:"coverage")',
    "f10_telemetry": '(abs:observability OR abs:telemetry OR abs:"audit log" OR abs:"shadow deployment" OR abs:canary)',
}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "full":
        q = "%s AND submittedDate:[%s TO %s]" % (CATS, FROM_TS, TO_TS)
        papers = fetch(q)
        json.dump(papers, sys.stdout, ensure_ascii=False)
        from collections import Counter
        print("\n// total:", len(papers), file=sys.stderr)
        print("// dates:", dict(sorted(Counter(p["published"] for p in papers).items())), file=sys.stderr)
    else:
        queries = THEMED if mode == "themed" else FORMS
        res = {}
        for k, v in queries.items():
            q = "%s AND (%s) AND submittedDate:[%s TO %s]" % (CATS, v, FROM_TS, TO_TS)
            try:
                r = fetch(q, max_results=600)
            except Exception as e:
                r = []
                print("ERR", k, e, file=sys.stderr)
            res[k] = r
            print("%s: %d" % (k, len(r)), file=sys.stderr)
            time.sleep(3.2)
        json.dump(res, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
