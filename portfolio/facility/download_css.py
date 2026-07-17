import urllib.request
with open('design-system.css', 'w', encoding='utf-8') as f:
    f.write(urllib.request.urlopen('https://www.thedrk.com/css/design-system.css').read().decode('utf-8'))
with open('pages.css', 'w', encoding='utf-8') as f:
    f.write(urllib.request.urlopen('https://www.thedrk.com/css/pages.css').read().decode('utf-8'))
