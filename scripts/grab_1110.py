#!/usr/bin/env python3
"""抓 HTML 正文 + PDF 首页机构块。用法: python3 scripts/grab_1110.py 2611.09304 ..."""
import sys, re, subprocess, os

def html_text(aid):
    for url in ["https://arxiv.org/html/%s" % aid, "https://arxiv.org/html/%sv1" % aid]:
        try:
            out = subprocess.run(["curl", "-sL", "--max-time", "60", url],
                                 capture_output=True, text=True).stdout
            if len(out) > 5000 and "ltx_" in out:
                return out
        except Exception:
            pass
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
    p = "/tmp/%s.pdf" % aid
    if not os.path.exists(p):
        subprocess.run(["curl", "-sL", "--max-time", "90", "-o", p,
                        "https://arxiv.org/pdf/%s" % aid], capture_output=True)
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
        open("/tmp/%s.txt" % aid, "w").write(t)
        print("=" * 20, aid, "HTMLLEN", len(h), "TEXTLEN", len(t))
        print("--- PDF HEAD ---")
        print(pdf_first(aid)[:1800])
