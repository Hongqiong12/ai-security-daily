#!/usr/bin/env python3
"""2026-11-25 机构核验 + PDF 全文抓取（供 6 模块精读取数）。

沿用第 11 次连续的教训：arxiv.org HTML 的 ltx_role_affiliation 常只回
`Affiliation:` 空值，机构一律走 curl arxiv.org/pdf/<id> + pypdf 读首页作者块。
本轮额外把 PDF 全文抽成 /tmp/papers_1125/<id>.txt，便于逐列核对表格数字。
"""
import re, os, sys, json, html as H, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

IDS = sys.argv[1:] or [
    "2611.25382", "2611.30545", "2611.30117", "2611.30592",
    "2611.23685", "2611.29629",
]
OUT = "/tmp/inst_1125.json" if len(IDS) > 1 else "/tmp/inst_1125_one.json"
TXT = "/tmp/papers_1125"
os.makedirs(TXT, exist_ok=True)


def curl(url, timeout=120, binary=False):
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
    blocks = re.findall(r'<span class="ltx_role_affiliation"[^>]*>(.*?)</span>', t, re.S)
    txt = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", b))).strip() for b in blocks]
    txt = [x for x in txt if x and x.lower() != "affiliation:"]
    return txt[:6]


def pdf_all(aid):
    raw = curl("https://arxiv.org/pdf/%s" % aid, timeout=150, binary=True)
    path = "/tmp/papers_1125/%s.pdf" % aid
    if not raw or len(raw) < 5000:
        return "", "", 0
    open(path, "wb").write(raw)
    try:
        from pypdf import PdfReader
        rd = PdfReader(path)
        pages = [(p.extract_text() or "") for p in rd.pages]
        full = "\n\n=== PAGE BREAK ===\n\n".join(pages)
        with open("%s/%s.txt" % (TXT, aid), "w", encoding="utf-8", errors="replace") as fh:
            fh.write(full)
        first = "\n".join(pages[:2])[:4200]
        return first, full[:200], len(rd.pages)
    except Exception as e:
        return "PDF_ERR:%s" % e, "", 0


def one(aid):
    rec = {"id": aid, "http": status("https://arxiv.org/abs/%s" % aid),
           "html_affil": html_affil(aid)}
    first, head, n = pdf_all(aid)
    rec["pdf_first"] = first
    rec["pages"] = n
    rec["txt_bytes"] = len(open("%s/%s.txt" % (TXT, aid), "rb").read()) if os.path.exists("%s/%s.txt" % (TXT, aid)) else 0
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
    print("\n==== %s  HTTP %s | pages %s | txt %s bytes" % (r["id"], r["http"], r["pages"], r["txt_bytes"]))
    print("HTML_AFFIL:", r["html_affil"])
    print("PDF_FIRST:\n", r["pdf_first"][:1500])
