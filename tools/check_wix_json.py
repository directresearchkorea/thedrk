import urllib.request
import re

url = 'https://www.thedrk.com/post/feelings-in-focus-how-drk-turns-emotion-videography-into-2025-s-research-edge'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Search for any JSON containing the images
matches = re.findall(r'<script id="wix-viewer-model".*?>(.*?)</script>', html, re.DOTALL)
if matches:
    print('Found wix-viewer-model length:', len(matches[0]))
    with open('viewer_model.json', 'w', encoding='utf-8') as f:
        f.write(matches[0])
else:
    print('No wix-viewer-model')

matches = re.findall(r'window\.viewerModel\s*=\s*(.*?);', html, re.DOTALL)
if matches:
    print('Found window.viewerModel length:', len(matches[0]))
