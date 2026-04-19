import os
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

POSTS_DIR = 'tools/posts'
count_videos = 0

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith('.md'): continue
    
    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    slug = filename[:-3]
    wix_url = f'https://www.thedrk.com/post/{slug}'
    
    try:
        req = urllib.request.Request(wix_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {wix_url}: {e}")
        continue
        
    # Find youtube IDs
    matches = re.findall(r'https://i\.ytimg\.com/vi/([a-zA-Z0-9_-]+)/', html)
    video_ids = list(set(matches))
    
    if not video_ids: continue
    
    # Check if already embedded
    if 'youtube.com/embed/' in content: continue
    
    print(f"Adding videos to {slug}: {video_ids}")
    
    embeds = ""
    for vid in video_ids:
        embeds += f'\n\n<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin: 2rem 0;"><iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;" src="https://www.youtube.com/embed/{vid}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>\n\n'
        count_videos += 1
        
    if slug == 'feelings-in-focus-how-drk-turns-emotion-videography-into-2025-s-research-edge':
        # Specific placement
        if '> **Cost Reality Check:**' in content:
            new_content = content.replace('> **Cost Reality Check:**', embeds + '\n> **Cost Reality Check:**')
        else:
            new_content = content + embeds
    else:
        # Generic placement at the bottom before tags if they exist
        if '#EyeTracking' in content or '#' in content[-200:]:
            # Find the last paragraph before tags
            lines = content.split('\n')
            for i in range(len(lines)-1, -1, -1):
                if lines[i].strip().startswith('#') and len(lines[i].split()) > 1:
                    lines.insert(i, embeds)
                    new_content = '\n'.join(lines)
                    break
            else:
                new_content = content + embeds
        else:
            new_content = content + embeds
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"\nEmbedded {count_videos} YouTube videos across posts.")
