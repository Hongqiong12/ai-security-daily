import urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import json, time, sys

NS = "{http://www.w3.org/2005/Atom}"
DATE = "submittedDate:[202610150000 TO 202610222359]"

QUERIES = {
 "q1_rewrite": '(abs:"prompt rewrite" OR abs:"prompt rewriting" OR abs:"safety rewriting" OR abs:"prompt sanitization" OR abs:"safe rephrasing" OR abs:"intent-preserving" OR abs:"query rewriting safety") AND ' + DATE,
 "q2_output_moderation": '(abs:"image moderation" OR abs:"content moderation" OR abs:"NSFW detection" OR abs:"generated image detection" OR abs:"image safety classifier" OR abs:"harmful image") AND ' + DATE,
 "q3_taxonomy_cot": '(abs:"hierarchical label" OR abs:"fine-grained taxonomy" OR abs:"risk taxonomy" OR abs:"content safety classification" OR abs:"chain-of-thought classification" OR abs:"label hierarchy") AND ' + DATE,
 "q4_rl_rewrite": '(abs:"reinforcement learning" OR abs:"GRPO" OR abs:"policy optimization") AND (abs:"rewriting" OR abs:"rewriter" OR abs:"prompt optimization") AND (abs:"safety" OR abs:"harmful" OR abs:"moderation") AND ' + DATE,
 "q5_data_curation": '(abs:"active learning" OR abs:"data curation" OR abs:"label noise" OR abs:"annotation quality" OR abs:"data auditing") AND (abs:"safety" OR abs:"moderation" OR abs:"harmful") AND ' + DATE,
 "q6_t2i_safety": '(abs:"text-to-image" OR abs:"image generation" OR abs:"diffusion model") AND (abs:"safety" OR abs:"NSFW" OR abs:"harmful content" OR abs:"jailbreak" OR abs:"guardrail") AND ' + DATE,
 "q7_pii_image": '(abs:"privacy" OR abs:"PII" OR abs:"sensitive image" OR abs:"face recognition") AND (abs:"image generation" OR abs:"diffusion" OR abs:"image detection") AND ' + DATE,
 "q8_prompt_injection": '(abs:"prompt injection" OR abs:"jailbreak defense" OR abs:"adversarial prompt") AND (abs:"defense" OR abs:"guard" OR abs:"filter" OR abs:"detection") AND ' + DATE,
 "q9_semantic_fidelity": '(abs:"semantic fidelity" OR abs:"semantic preservation" OR abs:"edit distance" OR abs:"instruction following") AND (abs:"rewriting" OR abs:"moderation" OR abs:"safety" OR abs:"prompt") AND ' + DATE,
 "q10_multimodal_guard": '(abs:"multimodal" OR abs:"vision-language") AND (abs:"safety" OR abs:"guard" OR abs:"moderation" OR abs:"risk") AND (abs:"benchmark" OR abs:"classifier" OR abs:"alignment") AND ' + DATE,
}

def fetch(q, n=40, retries=4):
    url = ("http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q)
           + f"&sortBy=submittedDate&sortOrder=desc&max_results={n}")
    for a in range(retries):
        try:
            r = urllib.request.urlopen(url, timeout=60)
            root = ET.fromstring(r.read())
            out = []
            for e in root.findall(NS + "entry"):
                aid = e.find(NS + "id").text.split("/abs/")[-1]
                out.append({
                    "id": aid,
                    "title": " ".join(e.find(NS + "title").text.split()),
                    "summary": " ".join(e.find(NS + "summary").text.split()),
                    "published": e.find(NS + "published").text[:10],
                    "comment": (e.find("{http://arxiv.org/schemas/atom}comment").text if e.find("{http://arxiv.org/schemas/atom}comment") is not None else ""),
                    "cats": [c.get("term") for c in e.findall(NS + "category")],
                    "authors": [a.find(NS + "name").text for a in e.findall(NS + "author")][:12],
                })
            return out
        except Exception as ex:
            print(f"  retry {a+1} {type(ex).__name__}", file=sys.stderr)
            time.sleep(5 + a * 4)
    return []

allp = {}
for name, q in QUERIES.items():
    res = fetch(q)
    print(f"{name}: {len(res)}", file=sys.stderr)
    for p in res:
        p.setdefault("hits", []).append(name)
        if p["id"] in allp:
            allp[p["id"]]["hits"].append(name)
        else:
            allp[p["id"]] = p
    time.sleep(4)

print(json.dumps(list(allp.values()), ensure_ascii=False, indent=1))
print(f"TOTAL_UNIQUE {len(allp)}", file=sys.stderr)
