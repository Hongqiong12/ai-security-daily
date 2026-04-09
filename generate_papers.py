import arxiv
import os
from pathlib import Path

selected_ids = {
    't2t': ['2604.06840v1', '2604.06833v1'],
    't2i': ['2604.03941v1', '2604.06662v1'],
    'agentic-search': ['2604.07223v1', '2604.06811v1']
}

client = arxiv.Client()
for category, ids in selected_ids.items():
    search = arxiv.Search(id_list=ids)
    for result in client.results(search):
        print(f"=== {category} | {result.get_short_id()} ===")
        print(f"Title: {result.title}")
        print(f"Authors: {[a.name for a in result.authors]}")
        print(f"Summary: {result.summary}\n")
