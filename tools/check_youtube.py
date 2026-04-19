import urllib.request
import re

url = 'https://www.thedrk.com/post/feelings-in-focus-how-drk-turns-emotion-videography-into-2025-s-research-edge'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

matches = re.findall(r'(https?://(?:www\.)?youtube\.com/[^\s\"\'<>]+|https?://youtu\.be/[^\s\"\'<>]+)', html)
print('Found YouTube URLs:')
for m in set(matches):
    print(m)

# Let's also check for iframes
iframes = re.findall(r'<iframe.*?src=[\"\'](.*?)[\"\'].*?>', html)
print('\nFound iframes:')
for i in iframes:
    print(i)
    
# Let's check for Wix Video Widget JSON config
video_json = re.findall(r'\"videoId\":\"(.*?)\"', html)
print('\nFound videoIds:')
for v in set(video_json):
    print(v)
