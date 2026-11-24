#!/usr/bin/env python3
"""2026-11-24 机构核验 + 链接有效性：HTML affiliation 直取 + PDF 首页 pypdf 回退。

历史第九~十次连续教训：arxiv.org HTML 的 ltx_role_affiliation 常只回
`Affiliation:` 空值，机构一律走 curl arxiv.org/pdf/<id> + pypdf 读首页作者块。
"""
import re, os, sys, json, html as H, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed

IDS = sys.argv[1:] or [
    "2611.27339", "2611.27905", "2611.20623", "2611.27229",
    "2611.27155", "2611.26881", "2611.20625", "2611.27268",
]
OUT = "/tmp/inst_1124.json"


def curl(url, timeout=90, binary=False):
    cmd = ["curl", "-sL", "--max-time", str(timeout), "-A", "Mozilla/5.0", url]
    r = subprocess.run(cmd, capture_output=True, text=not binary)
    return r.stdout if r.returncode == 0 else (b"" if binary else "")


def status(url):
    r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
                        "--max-time", "40", "-A", "Mozilla/5.0", url],
                       capture_output=True, text=True)
    return r.stdout.strip()


def html_affil(aid):
    t = curl("https://arxiv.org/abs/%s" % aid)
    # 尝试多种 affiliation 标记
    blocks = re.findall(r'<span class="ltx_role_affiliation"[^>]*>(.*?)</span>', t, re.S)
    txt = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", b))).strip() for b in blocks]
    txt = [x for x in txt if x and x.lower() != "affiliation:"]
    return txt[:6]


def pdf_first(aid):
    raw = curl("https://arxiv.org/pdf/%s" % aid, timeout=120, binary=True)
    path = "/tmp/%s_1124.pdf" % aid
    if not raw or len(raw) < 5000:
        return ""
    open(path, "wb").write(raw)
    try:
        from pypdf import PdfReader
        rd = PdfReader(path)
        n = min(2, len(rd.pages))
        return "\n".join((rd.pages[i].extract_text() or "") for i in range(n))[:4200]
    except Exception as e:
        return "PDF_ERR:%s" % e


def one(aid):
    rec = {"id": aid, "http": status("https://arxiv.org/abs/%s" % aid),
           "html_affil": html_affil(aid)}
    rec["pdf_first"] = pdf_first(aid)
    return rec


res = []
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = {ex.submit(one, a): a for a in IDS}
    for f in as_completed(futs):
        try:
            res.append(f.result())
        except Exception as e:
            print("ERR", futs[f], e, flush=True)

res.sort(key=lambda x: x["id"])
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
for r in res:
    print("\n==== %s  HTTP %s" % (r["id"], r["http"]))
    print("HTML_AFFIL:", r["html_affil"])
    print("PDF_FIRST:\n", r["pdf_first"][:1600])
