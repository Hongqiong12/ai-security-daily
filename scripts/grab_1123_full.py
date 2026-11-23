#!/usr/bin/env python3
"""2026-11-23 十分类全批拉取（健壮版，串行 + 增量落盘 + 429 强退避）。

教训（本轮新增）：三进程并发打 export.arxiv.org 会整体触发 429，
连 probe 能成功的 http 通道也会被限。⇒ 全批拉取必须**单进程串行**，
且主题词/形态通道改为**在本地全批池上用正则复现**，不再另发 API 请求。

每拉一页即把累计结果写入 /tmp/full_1123.json，避免中途失败前功尽弃。
"""
import re, json, time, urllib.parse, urllib.request

FROM_TS = "202611160000"
TO_TS = "202611232359"
OUT = "/tmp/full_1123.json"

CATS = ("(cat:cs.CV OR cat:cs.CR OR cat:cs.CL OR cat:cs.LG OR cat:cs.AI "
        "OR cat:cs.MM OR cat:cs.RO OR cat:cs.HC OR cat:cs.SE OR cat:eess.IV)")

ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)


def _t(tag, block):
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), block, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def one_page(query, start):
    params = {"search_query": query, "start": start, "max_results": 200,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(9):
        try:
            return urllib.request.urlopen(req, timeout=90).read().decode()
        except Exception as e:
            print("  retry %d @start=%d: %s" % (attempt + 1, start, e), flush=True)
            if attempt == 8:
                raise
            time.sleep(15 + 12 * attempt)  # 15/27/39/51/63/75/87/99 s


def main():
    q = "%s AND submittedDate:[%s TO %s]" % (CATS, FROM_TS, TO_TS)
    seen, out = set(), []
    start, MAX = 0, 8000
    while start < MAX:
        data = one_page(q, start)
        entries = ENTRY_RE.findall(data)
        if not entries:
            print("empty page @start=%d, stop" % start, flush=True)
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
        # 增量落盘
        json.dump(out, open(OUT, "w"), ensure_ascii=False)
        print("page start=%d entries=%d累计=%d" % (start, len(entries), len(out)), flush=True)
        if len(entries) < 200:
            break
        start += 200
        time.sleep(7.0)
    from collections import Counter
    print("=== TOTAL %d ===" % len(out), flush=True)
    print("DATES", dict(sorted(Counter(p["published"] for p in out).items())), flush=True)


if __name__ == "__main__":
    main()
