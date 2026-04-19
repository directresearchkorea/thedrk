import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.thedrk.com/post/what-game-genres-do-korean-gamers-prefer-in-2026'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

print('Title:', soup.find('title').text)
meta_img = soup.find('meta', property='og:image')
print('Thumbnail:', meta_img['content'] if meta_img else 'None')
meta_date = soup.find('meta', property='article:published_time')
print('Date:', meta_date['content'] if meta_date else 'None')

article = soup.find('article')
if article:
    print('Found article tag.')
    imgs = article.find_all('img')
    print('Images found:', len(imgs))
    for i, img in enumerate(imgs[:3]):
        src = img.get('src')
        data_src = img.get('data-src')
        print(f'Img {i}: src={src} data-src={data_src}')
else:
    print('No article tag found.')
