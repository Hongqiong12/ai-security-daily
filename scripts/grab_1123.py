#!/usr/bin/env python3
"""2026-11-23 六篇入选论文：HTML 正文 + PDF 首页机构 + abs comments。
用法: python3 scripts/grab_1123.py 2611.26569 2611.20821 ...
"""
import sys, re, subprocess, os


def curl(url, timeout=90, out=None):
    cmd = ["curl", "-sL", "--max-time", str(timeout), "-A", "Mozilla/5.0"]
    if out:
        cmd += ["-o", out]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout


def html_text(aid):
    for url in ["https://arxiv.org/html/%s" % aid, "https://arxiv.org/html/%sv1" % aid]:
        s = curl(url, 60)
        if len(s) > 5000 and "ltx_" in s:
            return s
    return ""


def strip(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<math[^>]*>.*?</math>", " [M] ", h, flags=re.S)
    h = re.sub(r"</(p|div|tr|h[1-6]|li|table)>", "\n", h)
    h = re.sub(r"</t[dh]>", " | ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = h.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ")
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\n\s*\n+", "\n", h)
    return h


def pdf_first(aid):
    p = "/tmp/%s_1123.pdf" % aid
    if not os.path.exists(p):
        curl("https://arxiv.org/pdf/%s" % aid, 90, out=p)
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    try:
        r = PdfReader(p)
        return "\n".join((r.pages[i].extract_text() or "") for i in range(min(2, len(r.pages))))
    except Exception as e:
        return "PDFERR %s" % e


if __name__ == "__main__":
    for aid in sys.argv[1:]:
        h = html_text(aid)
        t = strip(h) if h else ""
        open("/tmp/%s_1123.txt" % aid, "w").write(t)
        print("=" * 24, aid, "HTMLLEN", len(h), "TEXTLEN", len(t))
        aff = re.findall(r'(?:Affiliation|ltx_role_affiliation)[^\n]{0,220}', t)
        print("--- HTML AFF ---")
        print("\n".join(aff[:6]) if aff else "(empty)")
        print("--- PDF HEAD ---")
        print(pdf_first(aid)[:1800])
