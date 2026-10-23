#!/usr/bin/env python3
"""T2I/T+I2I 工业安全优先检索 - 第二轮 (2026-10-22 15:00)
日期窗口: 2026-10-15 ~ 2026-10-22
"""
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = "http://export.arxiv.org/api/query"
DATE_FROM = "202610150000"
DATE_TO = "202610222359"

QUERIES = [
    # 1. 输入侧改写 / safety rewriting 核心
    '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"prompt sanitization" OR '
    'abs:"safe rephrasing" OR abs:"safety rewriting" OR abs:"intent-preserving" OR '
    'abs:"semantic-preserving rewrite")',
    # 2. T2I 安全 / 改写 / 语义保真
    '(abs:"text-to-image" OR abs:"diffusion" OR abs:"image generation" OR abs:"text-to-image model") '
    'AND (abs:"rewrite" OR abs:"rephras" OR abs:"paraphras" OR abs:"semantic fidelity" OR '
    'abs:"semantic preservation")',
    # 3. T2I 安全对齐 / NSFW / 概念擦除
    '(abs:"text-to-image" OR abs:"diffusion") AND '
    '(abs:"safety" OR abs:"NSFW" OR abs:"moderation" OR abs:"concept erasure" OR abs:"concept erase" OR '
    'abs:"safe generation" OR abs:"alignment")',
    # 4. T2I benchmark / 评测
    '(abs:"text-to-image" OR abs:"diffusion" OR abs:"image generation") AND '
    '(abs:"benchmark" OR abs:"evaluation" OR abs:"dataset") AND '
    '(abs:"safety" OR abs:"risk" OR abs:"harmful" OR abs:"instruction following")',
    # 5. 多模态安全 / VLM 护栏
    '(abs:"multimodal" OR abs:"vision-language" OR abs:"VLM") AND '
    '(abs:"safety" OR abs:"guardrail" OR abs:"moderation" OR abs:"jailbreak")',
    # 6. 内容安全分类 / 层级标签 / 加权训练
    '(abs:"content moderation" OR abs:"safety classifier" OR abs:"risk taxonomy" OR '
    'abs:"hierarchical label" OR abs:"class-imbalanced" OR abs:"label noise") AND '
    '(abs:"training" OR abs:"classification" OR abs:"annotation")',
    # 7. RL 改写 / 约束优化
    '(abs:"reinforcement learning" OR abs:"RLHF" OR abs:"DPO" OR abs:"preference optimization") AND '
    '(abs:"rewrite" OR abs:"rephras" OR abs:"edit rate" OR abs:"constrained generation" OR abs:"safety")',
    # 8. 数据构建 / 标签审计 / 主动学习
    '(abs:"active learning" OR abs:"label audit" OR abs:"data cleaning" OR abs:"noisy label" OR '
    'abs:"LLM-as-judge" OR abs:"annotation quality") AND '
    '(abs:"safety" OR abs:"instruction" OR abs:"dataset")',
    # 9. 越狱 / 对抗 prompt（T2I 侧）
    '(abs:"text-to-image" OR abs:"image generation") AND '
    '(abs:"jailbreak" OR abs:"adversarial prompt" OR abs:"bypass" OR abs:"red team")',
    # 10. 腾讯/工业界线索 + 代答护栏
    '(abs:"guardrail" OR abs:"safe response" OR abs:"safety policy") AND '
    '(abs:"generation" OR abs:"model") AND (abs:"rewrite" OR abs:"refusal" OR abs:"mitigation")',
]

NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch(query, max_results=60, tries=4):
    full = f'{query} AND submittedDate:[{DATE_FROM} TO {DATE_TO}]'
    url = BASE + "?" + urllib.parse.urlencode({
        "search_query": full,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:
            print(f"  retry {i+1}: {e}")
            time.sleep(4 * (i + 1))
    return None


def parse(raw):
    out = []
    if not raw:
        return out
    root = ET.fromstring(raw)
    for e in root.findall("a:entry", NS):
        eid = e.find("a:id", NS).text
        sid = eid.rsplit("/", 1)[-1]
        title = " ".join(e.find("a:title", NS).text.split())
        summary = " ".join(e.find("a:summary", NS).text.split())
        published = e.find("a:published", NS).text[:10]
        comment = e.find("arxiv:comment", NS)
        comment = " ".join(comment.text.split()) if comment is not None else ""
        cats = [c.get("term") for c in e.findall("a:category", NS)]
        out.append({
            "id": sid, "title": title, "summary": summary,
            "published": published, "comment": comment, "cats": cats,
            "url": f"https://arxiv.org/abs/{sid}",
        })
    return out


def main():
    all_papers = {}
    for i, q in enumerate(QUERIES, 1):
        print(f"[{i}/{len(QUERIES)}] {q[:70]}...")
        res = parse(fetch(q))
        print(f"  -> {len(res)}")
        for p in res:
            all_papers.setdefault(p["id"], p)
        time.sleep(3.5)
    print(f"\n去重后总数: {len(all_papers)}")
    with open("research/raw_round2.json", "w") as f:
        json.dump(list(all_papers.values()), f, ensure_ascii=False, indent=1)
    for p in sorted(all_papers.values(), key=lambda x: x["published"], reverse=True):
        print(f"{p['published']} | {p['id']} | {p['title'][:95]} | {p['comment'][:40]}")


if __name__ == "__main__":
    main()
