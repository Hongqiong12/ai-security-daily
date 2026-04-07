import urllib.request
import xml.etree.ElementTree as ET

ids = ['2604.04060', '2604.03870', '2604.03598', '2604.01888']
url = 'http://export.arxiv.org/api/query?id_list=' + ','.join(ids)
response = urllib.request.urlopen(url)
data = response.read()
root = ET.fromstring(data)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

for entry in root.findall('atom:entry', ns):
    arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1].split('v')[0]
    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
    authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
    published = entry.find('atom:published', ns).text
    print(f"--- {arxiv_id} ---")
    print(f"Title: {title}")
    print(f"Authors: {', '.join(authors)}")
    print(f"Published: {published}")
    print(f"Abstract: {summary}\n")

