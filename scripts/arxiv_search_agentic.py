import arxiv
import sys

client = arxiv.Client()
agent_query = '(cat:cs.IR OR cat:cs.CL OR cat:cs.CR) AND (all:"agentic search" OR all:"retrieval augmented" OR all:"search agent safety")'

search_agent = arxiv.Search(
  query = agent_query,
  max_results = 3,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

print("\nAgentic Search Papers:")
for r in client.results(search_agent):
    print(f"- {r.get_short_id()}: {r.title}")

