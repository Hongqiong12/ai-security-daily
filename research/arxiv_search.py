import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime

def search_arxiv(query, max_results=10):
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
    print(f"Searching: {url}")
    response = urllib.request.urlopen(url)
    data = response.read()
    root = ET.fromstring(data)
    
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        published = entry.find('atom:published', ns).text
        id_url = entry.find('atom:id', ns).text
        arxiv_id = id_url.split('/abs/')[-1].split('v')[0]
        categories = [cat.attrib['term'] for cat in entry.findall('atom:category', ns)]
        papers.append({
            'id': arxiv_id,
            'title': title,
            'published': published,
            'categories': categories,
            'summary': summary
        })
    return papers

# T2T query
t2t_query = '(cat:cs.CR OR cat:cs.CL OR cat:cs.LG) AND (all:jailbreak OR all:"prompt injection" OR all:"adversarial attack" OR all:"red teaming" OR all:"safe alignment")'
print("T2T Papers:")
for p in search_arxiv(t2t_query, 5):
    print(f"- [{p['id']}] {p['title']} ({p['published']})")

# T2I query
t2i_query = '(cat:cs.CV OR cat:cs.CR) AND (all:"text-to-image" OR all:"diffusion") AND (all:jailbreak OR all:"concept erase" OR all:"safety filter" OR all:security)'
print("\nT2I Papers:")
for p in search_arxiv(t2i_query, 5):
    print(f"- [{p['id']}] {p['title']} ({p['published']})")

