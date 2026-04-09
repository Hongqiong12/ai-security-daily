import arxiv

def fetch_recent(query, max_results=4):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in client.results(search):
        papers.append({
            'id': result.get_short_id(),
            'title': result.title,
            'summary': result.summary,
            'published': result.published.strftime('%Y-%m-%d'),
            'url': result.entry_id
        })
    return papers

print("T2T:")
for p in fetch_recent('cat:cs.CR AND (abs:"jailbreak" OR abs:"alignment" OR abs:"safety")', 4):
    print(f"- {p['id']}: {p['title']}")

print("\nT2I:")
for p in fetch_recent('cat:cs.CV AND abs:"diffusion" AND (abs:"attack" OR abs:"watermark" OR abs:"safety")', 4):
    print(f"- {p['id']}: {p['title']}")

print("\nAgentic:")
for p in fetch_recent('cat:cs.AI AND abs:"agent" AND (abs:"security" OR abs:"safety" OR abs:"attack")', 4):
    print(f"- {p['id']}: {p['title']}")
