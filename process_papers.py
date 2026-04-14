import arxiv
import os
import glob
import json

existing_ids = set()
for p in glob.glob('categories/*/papers/*.md'):
    basename = os.path.basename(p)
    if '_' in basename:
        existing_ids.add(basename.split('_')[0].replace('v1', '').replace('v2', ''))

def fetch_recent(query, max_results=10):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in client.results(search):
        pid = result.get_short_id().split('v')[0]
        if pid not in existing_ids:
            papers.append({
                'id': result.get_short_id(),
                'title': result.title,
                'summary': result.summary,
                'published': result.published.strftime('%Y-%m-%d'),
                'url': result.entry_id,
                'authors': [a.name for a in result.authors]
            })
    return papers

t2t_papers = fetch_recent('cat:cs.CR AND (abs:"jailbreak" OR abs:"alignment" OR abs:"safety")', 10)
t2i_papers = fetch_recent('cat:cs.CV AND abs:"diffusion" AND (abs:"attack" OR abs:"watermark" OR abs:"safety")', 10)
agent_papers = fetch_recent('cat:cs.AI AND abs:"agent" AND (abs:"security" OR abs:"safety" OR abs:"attack")', 10)

selected = []
selected.extend(t2t_papers[:3])
selected.extend(t2i_papers[:3])
selected.extend(agent_papers[:2])

with open('selected_papers.json', 'w', encoding='utf-8') as f:
    json.dump(selected, f, indent=2)

print(f"Saved {len(selected)} papers to selected_papers.json")
