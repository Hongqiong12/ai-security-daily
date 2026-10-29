#!/usr/bin/env python3
"""2026-10-29 第 2 轮：宽口径复核（不加 cat 限制），用于证伪"空窗"。

只看专项查询返回量，不看内容。用法:
  python3 scripts/search_1029_round2.py > /tmp/papers_1029_r2.json
"""
import re, json, time, sys, urllib.parse, urllib.request

FROM_DATE, TO_DATE = "2026-10-22", "2026-10-29"

QUERIES = {
    "b01_image_edit_refuse": 'abs:"image editing" AND (abs:refuse OR abs:refusal OR abs:harmful OR abs:unsafe OR abs:malicious)',
    "b02_editor_guardrail": 'abs:editor AND (abs:guardrail OR abs:safety OR abs:policy) AND (abs:image OR abs:visual)',
    "b03_nsfw_detect": 'abs:NSFW AND (abs:detection OR abs:classifier OR abs:benchmark OR abs:dataset)',
    "b04_porn_vulgar": '(abs:pornography OR abs:vulgar OR abs:obscene OR abs:explicit content)',
    "b05_harmful_prompt_detect": 'abs:"harmful prompt" OR abs:"unsafe prompt" OR abs:"prompt harm"',
    "b06_arguard": 'abs:ArGuard OR abs:"Arabic harmful" OR abs:"harmful content detection"',
    "b07_safety_distill_image": 'abs:"safety" AND abs:"distillation" AND (abs:diffusion OR abs:"image generation")',
    "b08_few_step_safety": '(abs:"few-step" OR abs:"distillation" OR abs:"consistency model") AND abs:safety',
    "b09_concept_erase_diff": 'abs:"concept erasure" OR abs:"erase concept" OR abs:"concept removal"',
    "b10_image_guard_vlm": '(abs:"vision-language" OR abs:VLM OR abs:MLLM) AND (abs:"safety" OR abs:moderation) AND (abs:image OR abs:content)',
    "b11_moderation_taxonomy": '(abs:moderation OR abs:"content policy") AND (abs:taxonomy OR abs:hierarchy OR abs:"risk level" OR abs:"severity")',
    "b12_political_region": '(abs:political OR abs:"sensitive region" OR abs:geopolitical) AND (abs:content OR abs:moderation OR abs:image)',
    "b13_prompt_rewrite_llm": '(abs:"prompt rewriting" OR abs:"prompt rewrite" OR abs:"query rewriting") AND (abs:safety OR abs:safe OR abs:harm)',
    "b14_redteam_image": '(abs:"red teaming" OR abs:redteam) AND (abs:image OR abs:diffusion OR abs:"visual generation")',
    "b15_data_poison": '(abs:"data poisoning" OR abs:"backdoor") AND (abs:diffusion OR abs:"text-to-image" OR abs:image)',
    "b16_watermark_lora": '(abs:watermark OR abs:"provenance") AND (abs:LoRA OR abs:"low-rank" OR abs:diffusion)',
    "b17_label_noise_audit": '(abs:"label noise" OR abs:"annotation error" OR abs:"label error") AND (abs:safety OR abs:moderation OR abs:content)',
    "b18_active_learning_safety": '(abs:"active learning" OR abs:"uncertainty sampling") AND (abs:safety OR abs:moderation OR abs:"data selection")',
    "b19_i2i_safety": '(abs:"image-to-image" OR abs:"image editing") AND (abs:safety OR abs:guard)',
    "b20_generated_image_detect": '(abs:"generated image" OR abs:"AI-generated") AND (abs:detect OR abs:classification OR abs:provenance)',
}

HDRS = {"User-Agent": "Mozilla/5.0 research-collector/1.0"}
ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)

def clean(s):
    s = (s.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">")
          .replace("&#39;","'").replace("&quot;",'"'))
    return " ".join(s.split())

def fetch(sq, n=200, retries=4):
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(sq)
           + f"&start=0&max_results={n}&sortBy=submittedDate&sortOrder=descending")
    for a in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=120).read().decode("utf-8","ignore")
        except Exception as ex:
            print(f"    retry {a+1} {type(ex).__name__}", file=sys.stderr)
            time.sleep(10 + a*10)
    return ""

def parse(xml):
    out=[]
    for blk in ENTRY.findall(xml):
        m = re.search(r"<id>http://arxiv.org/abs/([^<]+)</id>", blk)
        if not m: continue
        aid = re.sub(r"v\d+$","",m.group(1))
        t = re.search(r"<title>(.*?)</title>", blk, re.S)
        su = re.search(r"<summary>(.*?)</summary>", blk, re.S)
        pu = re.search(r"<published>(.*?)</published>", blk)
        au = re.findall(r"<name>(.*?)</name>", blk)
        cm = re.search(r'<arxiv:comment[^>]*>(.*?)</arxiv:comment>', blk, re.S)
        cats = re.findall(r'<category term="([^"]+)"', blk)
        out.append({"id":aid,"title":clean(t.group(1)) if t else "",
                    "authors":au[:12],"summary":clean(su.group(1)) if su else "",
                    "published":pu.group(1)[:10] if pu else "","cats":cats,
                    "comment":clean(cm.group(1)) if cm else ""})
    return out

allp={}
for name,q in QUERIES.items():
    sq = f"({q}) AND submittedDate:[{FROM_DATE.replace('-','')}0000 TO {TO_DATE.replace('-','')}2359]"
    batch=[p for p in parse(fetch(sq)) if FROM_DATE <= p["published"] <= TO_DATE]
    for p in batch:
        if p["id"] in allp: allp[p["id"]]["hits"].append(name)
        else:
            p["hits"]=[name]; allp[p["id"]]=p
    print(f"{name}: {len(batch)}", file=sys.stderr)
    time.sleep(3.2)

items=list(allp.values())
print(json.dumps(items, ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(items)}", file=sys.stderr)
