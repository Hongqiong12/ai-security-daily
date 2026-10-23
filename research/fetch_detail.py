#!/usr/bin/env python3
"""抓取候选论文 HTML 正文，提取机构、作者、关键量化结果"""
import re
import sys
import time
import urllib.request

IDS = ["2610.24508", "2610.28195", "2610.27516", "2610.22068", "2610.27728", "2610.25215"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        return f"__ERR__ {e}"


def strip(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


for pid in IDS:
    print("#" * 100)
    print("ID:", pid)
    for base in (f"https://arxiv.org/html/{pid}v1", f"https://arxiv.org/abs/{pid}"):
        h = get(base)
        if h.startswith("__ERR__"):
            print(f"  [{base}] {h}")
            time.sleep(2)
            continue
        t = strip(h)
        print(f"  [{base}] len={len(t)}")
        if "/html/" in base:
            # 作者块：通常在开头 3000 字符内
            print("  --- HEAD 3500 ---")
            print(t[:3500])
        else:
            m = re.search(r"Authors:.{0,900}", t)
            print("  --- AUTHORS ---")
            print(m.group(0) if m else t[:600])
            mc = re.search(r"Comments:.{0,300}", t)
            print("  --- COMMENTS ---", mc.group(0) if mc else "")
        break
    time.sleep(3)
