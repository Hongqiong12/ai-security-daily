#!/usr/bin/env python3
"""2026-11-12 全批扫描（纪律 ②：主线零命中 → 不绑安全词，逐篇 title+abstract 判定）。

供给探测: cs.CV 11-05:148 / 11-06:125 / 11-07:90 / 11-08:69 / 11-09:134 / 11-10:102，
          11-11/11-12 未生成 ⇒ 相对 11-11 轮（停在 11-09）新增 11-10 批次。
窗口: 11-05 → 11-12（过去 7 天），十类全包，与磁盘已建档做差集。

用法: python3 scripts/search_1112_api.py full  > /tmp/full_1112.json
      python3 scripts/search_1112_api.py themed > /tmp/themed_1112.json
"""
import re, json, time, sys, urllib.parse, urllib.request

FROM_TS = "202611050000"
TO_TS = "202611122359"

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
        queries = {
            "t1_t2i_safety": '(abs:"text-to-image" OR abs:"image generation") AND (abs:safety OR abs:harmful OR abs:NSFW)',
            "t2_prompt_rewrite": '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"safety rewriting" OR abs:"sanitiz" OR abs:"rephras")',
            "t3_i2i_edit_safety": '(abs:"image editing" OR abs:"editing instruction" OR abs:"instruction-based editing") AND (abs:safety OR abs:guard OR abs:harm OR abs:refus)',
            "t4_image_moderation": '(abs:"content moderation" OR abs:"image moderation" OR abs:"NSFW" OR abs:"safety classifier" OR abs:"image safety")',
            "t5_watermark": '(abs:watermark OR abs:provenance OR abs:"AIGC detection") AND (abs:image OR abs:diffusion)',
            "t6_concept_erasure": '(abs:"concept erasure" OR abs:"machine unlearning" OR abs:"concept unlearning") AND (abs:diffusion OR abs:image)',
            "t7_threshold": '(abs:"operating point" OR abs:"threshold calibration" OR abs:conformal OR abs:"misclassification rate")',
            "t8_hard_negative": '(abs:"hard negative" OR abs:"hard-negative mining" OR abs:"data curation" OR abs:"active learning")',
            "t9_unified_edit": '(abs:"unified" AND (abs:"generation and editing" OR abs:"image editing"))',
            "t10_video_safety": '(abs:"video generation" OR abs:"text-to-video") AND (abs:safety OR abs:moderation OR abs:harm)',
        }
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
