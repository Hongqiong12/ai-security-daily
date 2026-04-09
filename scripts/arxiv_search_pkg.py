import arxiv
import sys

# Construct the default API client.
client = arxiv.Client()

t2t_query = 'cat:cs.CR AND (all:jailbreak OR all:"safety alignment" OR all:"prompt injection" OR all:"red teaming" OR all:"LLM security" OR all:"adversarial attack")'
t2i_query = '(cat:cs.CV OR cat:cs.CR) AND (all:"concept erasure" OR all:NSFW OR all:"text-to-image safety" OR all:"diffusion model attack" OR all:"image generation safety")'

search_t2t = arxiv.Search(
  query = t2t_query,
  max_results = 5,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

search_t2i = arxiv.Search(
  query = t2i_query,
  max_results = 5,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

print("T2T Papers:")
for r in client.results(search_t2t):
    print(f"- {r.get_short_id()}: {r.title}")

print("\nT2I Papers:")
for r in client.results(search_t2i):
    print(f"- {r.get_short_id()}: {r.title}")

