import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.thedrk.com/post/feelings-in-focus-how-drk-turns-emotion-videography-into-2025-s-research-edge'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')
article = soup.find('article')
out = []
if article:
    out.append('Found article tag!')
    for elem in article.find_all(['p', 'img', 'div', 'h1', 'h2', 'h3']):
        if elem.name == 'img':
            src = elem.get('src')
            if src and 'media' in src:
                out.append(f'[IMG: {src}]')
        elif elem.name in ['p', 'h1', 'h2', 'h3']:
            text = elem.get_text(strip=True)
            if text:
                out.append(f'[{elem.name.upper()}]: {text}')
        elif elem.name == 'div':
            # Check for data injected images
            html_chunk = str(elem)
            matches = re.finditer(r'\"uri\":\"(a14e67_[a-zA-Z0-9]+~mv2\.(?:jpg|png|webp|jpeg))\"', html_chunk)
            for m in matches:
                out.append(f'[GALLERY_JSON_IMG: {m.group(1)}]')
else:
    out.append('No article tag found.')

with open('debug_dom.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
