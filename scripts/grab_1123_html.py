#!/usr/bin/env python3
"""2026-11-23 网页端十分类全批扫描（导出 API 被 429 限流时的兜底主通道）。

背景：本轮三进程并发打 export.arxiv.org 触发 IP 级 429，连带 id_list /
submittedDate / 简单 cat 查询全部被限；但 **arxiv.org 网页端独立可用**
（list + abs 页均 HTTP 200）。故改为：
  step1: 十分类 /list/<cat>/recent?show=2000 抓 ID + 标题 + 公告日期 + 作者 + comments
  step2: 本地按公告日期窗口过滤 + 合并去重 + 与磁盘已建档做差集
  step3: 对宽口径初筛命中的候选抓 /abs/<id> 补摘要（逐篇核验用）
输出 /tmp/full_1123.json（funnel_1123.py 直接消费）。

用法: python3 scripts/grab_1123_html.py listing   # 只抓 listing
      python3 scripts/grab_1123_html.py abstracts # 补候选摘要
"""
import re, json, html as H, os, sys, glob, time, subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

CATS = ["cs.CV", "cs.LG", "cs.CL", "cs.AI", "cs.CR",
        "cs.MM", "cs.RO", "cs.HC", "cs.SE", "eess.IV"]
WIN_FROM, WIN_TO = "2026-11-16", "2026-11-23"
POOL = "/tmp/pool_1123.json"
CAND = "/tmp/cand_ids_1123.json"
FINAL = "/tmp/full_1123.json"

MON = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
       "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
ITEM = re.compile(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", re.S)
H3 = re.compile(r"<h3>(.*?)</h3>", re.S)


def curl(url, timeout=90):
    for a in range(4):
        r = subprocess.run(["curl", "-sL", "--max-time", str(timeout),
                            "-A", "Mozilla/5.0", url], capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 2000:
            return r.stdout
        time.sleep(5 + 5 * a)
    return ""


def clean(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def date_of(h3):
    m = re.search(r"(\d{1,2}) ([A-Za-z]{3}) (\d{4})", h3)
    if not m:
        return None
    return "%s-%s-%02d" % (m.group(3), MON.get(m.group(2), "00"), int(m.group(1)))


def parse_listing(txt, cat):
    heads = [(m.start(), date_of(m.group(1))) for m in H3.finditer(txt)]
    heads = [(p, d) for p, d in heads if d]
    out = []
    for m in ITEM.finditer(txt):
        pos = m.start()
        cur = None
        for p, d in heads:
            if p < pos:
                cur = d
            else:
                break
        if cur is None or not (WIN_FROM <= cur <= WIN_TO):
            continue
        aid = re.search(r"/abs/(\d{4}\.\d{4,5})", m.group(1))
        if not aid:
            continue
        tm = re.search(r"list-title[^>]*>(.*?)</div>", m.group(2), re.S)
        am = re.search(r"list-authors[^>]*>(.*?)</div>", m.group(2), re.S)
        cm = re.search(r"list-comments[^>]*>(.*?)</div>", m.group(2), re.S)
        out.append({"id": aid.group(1), "title": clean(tm.group(1)) if tm else "",
                    "authors": clean(am.group(1)) if am else "",
                    "comments": clean(cm.group(1)) if cm else "",
                    "published": cur, "cats": [cat], "abstract": ""})
    return out


def step_listing():
    allp = {}
    for cat in CATS:
        url = "https://arxiv.org/list/%s/recent?skip=0&show=2000" % cat
        txt = curl(url)
        items = parse_listing(txt, cat)
        print("%s: raw_html=%d items_in_window=%d" % (cat, len(txt), len(items)), flush=True)
        for p in items:
            key = p["id"].split("v")[0]
            if key in allp:
                allp[key]["cats"] = sorted(set(allp[key]["cats"] + p["cats"]))
            else:
                allp[key] = p
        time.sleep(2.0)
    papers = list(allp.values())
    # 合并此前 API 通道已成功落盘的 400 篇（带真实摘要）
    if os.path.exists(FINAL):
        try:
            old = json.load(open(FINAL))
            for p in old:
                key = p["id"].split("v")[0]
                if key in allp:
                    allp[key]["abstract"] = p.get("abstract", "")
                else:
                    allp[key] = p
            print("merged API pages: %d" % len(old), flush=True)
        except Exception as e:
            print("merge skip:", e, flush=True)
    papers = list(allp.values())
    json.dump(papers, open(POOL, "w"), ensure_ascii=False)
    print("=== POOL %d ===" % len(papers), flush=True)
    print("DATES", dict(sorted(Counter(p["published"] for p in papers).items())), flush=True)
    print("CATS", dict(Counter(c for p in papers for c in p["cats"]).most_common(14)), flush=True)
    have = {os.path.basename(f).split("_")[0] for f in glob.glob("categories/*/papers/*.md")}
    fresh = [p for p in papers if p["id"].split("v")[0] not in have]
    print("NOT-collected:", len(fresh), flush=True)


# 宽口径初筛（标题级，宁可多抓；不绑安全语义）
WIDE = re.compile(
    r"(safety|safe|harm|risk|guard|moderation|moderate|NSFW|toxic|refus|"
    r"align|jailbreak|adversarial|attack|defen|policy|privacy|watermark|provenance|"
    r"rewrite|rephras|sanitiz|paraphras|prompt|instruction|"
    r"text-to-image|image generation|image editing|image edit|diffusion|generat|"
    r"benchmark|evaluation|eval|dataset|audit|annotat|label|"
    r"calibrat|conformal|threshold|operating point|coverage|confidence|uncertaint|"
    r"reward|preference|optimiz|reinforcement|GRPO|"
    r"consisten|fidelity|preserv|regression|drift|robust|"
    r"reweight|resampl|imbalanc|hard negative|active learning|distill|"
    r"ordinal|hierarch|taxonom|granular|multi-class|"
    r"multilingual|cross-lingual|code-switch|translation|"
    r"video|temporal|trace|telemetry|observab|canary|shadow|"
    r"concept eras|unlearn|erase|forget|ablat|"
    r"edit|instruction-based|unified)", re.I)


def step_abstracts():
    papers = json.load(open(POOL))
    have = {os.path.basename(f).split("_")[0] for f in glob.glob("categories/*/papers/*.md")}
    cand = [p for p in papers if p["id"].split("v")[0] not in have
            and WIDE.search(p["title"] or "")]
    # API 已带摘要的不再抓
    need = [p for p in cand if not p.get("abstract")]
    print("CAND by title: %d | need abstract: %d" % (len(cand), len(need)), flush=True)
    json.dump([p["id"] for p in cand], open(CAND, "w"))

    def one(p):
        txt = curl("https://arxiv.org/abs/%s" % p["id"], timeout=60)
        m = re.search(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>', txt, re.S)
        if m:
            p["abstract"] = re.sub(r"\s+", " ", clean(m.group(1))).replace("Abstract:", "").strip()
        cm = re.search(r'<td class="tablecell comments[^>]*>(.*?)</td>', txt, re.S)
        if cm and not p.get("comments"):
            p["comments"] = clean(cm.group(1))
        return p

    done = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(one, p): p for p in need}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:
                print("abs err", e, flush=True)
            done += 1
            if done % 50 == 0:
                print("  abs done %d/%d" % (done, len(need)), flush=True)
    byid = {p["id"]: p for p in papers}
    for p in cand:
        byid[p["id"]] = p
    # 输出仍是"全批池"（非候选集），保证 funnel 的扫描分母如实
    final = list(byid.values())
    json.dump(final, open(FINAL, "w"), ensure_ascii=False)
    withabs = sum(1 for p in final if p.get("abstract"))
    print("=== FINAL POOL %d | with abstract %d | cand %d ===" % (len(final), withabs, len(cand)), flush=True)
    print("DATES", dict(sorted(Counter(p["published"] for p in final).items())), flush=True)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "listing"
    if step == "listing":
        step_listing()
    else:
        step_abstracts()
