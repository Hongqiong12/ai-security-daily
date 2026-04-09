import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
import sys

def search_arxiv(query, max_results=10):
    url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=desc&max_results={max_results}"
    response = urllib.request.urlopen(url)
    xml_data = response.read()
    root = ET.fromstring(xml_data)
    
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.replace('\n', ' ').strip()
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.replace('\n', ' ').strip()
        link = entry.find("{http://www.w3.org/2005/Atom}id").text
        arxiv_id = link.split('/')[-1]
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        papers.append({
            "id": arxiv_id,
            "title": title,
            "summary": summary,
            "published": published
        })
    return papers

# T2T
t2t_query = 'cat:cs.CR AND (all:"jailbreak" OR all:"safety alignment" OR all:"prompt injection" OR all:"red teaming" OR all:"LLM security" OR all:"adversarial attack")'
t2t_papers = search_arxiv(t2t_query, 5)

# T2I
t2i_query = '(cat:cs.CV OR cat:cs.CR) AND (all:"concept erasure" OR all:"NSFW" OR all:"text-to-image safety" OR all:"diffusion model attack" OR all:"image generation safety")'
t2i_papers = search_arxiv(t2i_query, 5)

print("T2T Papers:")
for p in t2t_papers:
    print(f"- {p['id']}: {p['title']}")

print("\nT2I Papers:")
for p in t2i_papers:
    print(f"- {p['id']}: {p['title']}")

