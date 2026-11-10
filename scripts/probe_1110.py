#!/usr/bin/env python3
"""2026-11-10 供给探测：cs.CV 近一周逐日批次量。"""
import re, time, urllib.parse, urllib.request
from collections import Counter

Q = '(cat:cs.CV) AND submittedDate:[202611030000 TO 202611102359]'
ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)

def t(tag, b):
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), b, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""

out, start = [], 0
while start < 1600:
    p = {"search_query": Q, "start": start, "max_results": 200,
         "sortBy": "submittedDate", "sortOrder": "descending"}
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for a in range(4):
        try:
            data = urllib.request.urlopen(req, timeout=90).read().decode(); break
        except Exception:
            if a == 3: raise
            time.sleep(4 + 3*a)
    es = ENTRY_RE.findall(data)
    if not es: break
    for e in es:
        out.append(t("published", e)[:10])
    if len(es) < 200: break
    start += 200
    time.sleep(3.2)

c = Counter(out)
for d in sorted(c, reverse=True):
    print(d, c[d])
print("TOTAL", len(out))
