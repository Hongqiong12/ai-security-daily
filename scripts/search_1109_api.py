#!/usr/bin/env python3
"""2026-11-09 日报检索脚本。

供给侧探测（11-09 09:5x）:
  cat:cs.CV submittedDate [11-04 TO 11-09]: 11-04:124 / 11-05:123
  11-06 / 11-07 / 11-08 **三个批次均未生成**（相对 11-08 那轮零新增供给）
  ⇒ 本轮为「零新增供给轮」，不允许再靠加查询路数硬凑。

策略:
  A. FULLBATCH —— 全量拉 11-01→11-05 五个批次，十类全包（不绑安全词），
     与已收录 304 篇做差集，得到「未读存量候选池」，逐篇按结构匹配人工扫。
  B. THEMED —— 保留一句主题探测，只用于记录归零路数，不作为主供给通道。

用法: python3 scripts/search_1109_api.py full   > /tmp/full_1109.json
"""
import re
import json
import time
import sys
import urllib.parse
import urllib.request

FROM_TS = "202611010000"
TO_TS = "202611092359"

CATS = ("(cat:cs.CV OR cat:cs.CR OR cat:cs.CL OR cat:cs.LG OR cat:cs.AI "
        "OR cat:cs.MM OR cat:cs.RO OR cat:cs.HC OR cat:cs.SE OR cat:eess.IV)")

ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)


def _t(tag, block):
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), block, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def fetch(query, max_results=2000):
    out = []
    start = 0
    while start < max_results:
        params = {
            "search_query": query,
            "start": start,
            "max_results": 200,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        for attempt in range(4):
            try:
                data = urllib.request.urlopen(req, timeout=90).read().decode()
                break
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(4 + 3 * attempt)
        entries = ENTRY_RE.findall(data)
        if not entries:
            break
        for e in entries:
            aid = _t("id", e).split("/abs/")[-1]
            out.append({
                "id": aid,
                "title": _t("title", e),
                "abstract": _t("summary", e),
                "published": _t("published", e)[:10],
                "cats": re.findall(r'term="([^"]+)"', e),
            })
        if len(entries) < 200:
            break
        start += 200
        time.sleep(3.2)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "full":
        q = "%s AND submittedDate:[%s TO %s]" % (CATS, FROM_TS, TO_TS)
        papers = fetch(q)
        json.dump(papers, sys.stdout, ensure_ascii=False)
        print("\n// total:", len(papers), file=sys.stderr)
    else:
        # 主题探测（仅用于记录归零，不用于供数）
        queries = {
            "t1_t2i_safety": '(abs:"text-to-image" OR abs:"image generation") AND (abs:safety OR abs:harmful OR abs:NSFW)',
            "t2_prompt_rewrite": '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"safety rewriting" OR abs:"sanitiz")',
            "t3_i2i_edit_safety": '(abs:"image editing" OR abs:"editing instruction") AND (abs:safety OR abs:guard OR abs:harm OR abs:refus)',
            "t4_image_moderation": '(abs:"content moderation" OR abs:"image moderation" OR abs:"NSFW" OR abs:"safety classifier")',
            "t5_watermark": '(abs:watermark OR abs:provenance) AND (abs:image OR abs:diffusion)',
            "t6_concept_erasure": '(abs:"concept erasure" OR abs:"machine unlearning") AND (abs:diffusion OR abs:image)',
            "t7_threshold": '(abs:"operating point" OR abs:"threshold calibration" OR abs:"conformal") AND (abs:safety OR abs:moderation OR abs:classification)',
            "t8_hard_negative": '(abs:"hard negative" OR abs:"hard-negative mining" OR abs:"data curation")',
        }
        res = {}
        for k, v in queries.items():
            q = "%s AND (%s) AND submittedDate:[%s TO %s]" % (CATS, v, FROM_TS, TO_TS)
            try:
                r = fetch(q)
            except Exception as e:
                r = []
                print("ERR", k, e, file=sys.stderr)
            res[k] = r
            print("%s: %d" % (k, len(r)), file=sys.stderr)
            time.sleep(3.2)
        json.dump(res, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
