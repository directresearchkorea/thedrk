import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.thedrk.com/post/ai-era-research-competitiveness-why-insight-is-won-in-the-field'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

print("Searching for categories in JSON data...")
matches = re.finditer(r'"categories":\s*\[({.*?})\]', html)
for m in matches:
    print(m.group(1))

print("Searching for categories in HTML tags...")
soup = BeautifulSoup(html, 'html.parser')
for a in soup.find_all('a'):
    href = a.get('href', '')
    if 'category' in href.lower() or 'blog' in href.lower():
        print(f"Link: {a.text.strip()}, Href: {href}")
