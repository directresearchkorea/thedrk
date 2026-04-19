import os
import re

POSTS_DIR = r'c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com\tools\posts'
count = 0

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith('.md'): continue
    filepath = os.path.join(POSTS_DIR, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'thumbnail: "/assets/images/posts/maxresdefault.jpg"' in content or 'thumbnail: "/assets/images/posts/hqdefault.jpg"' in content:
        # Find video ID
        matches = re.findall(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', content)
        if matches:
            vid = matches[0]
            new_thumb = f'https://i.ytimg.com/vi/{vid}/maxresdefault.jpg'
            new_content = re.sub(r'thumbnail: "/assets/images/posts/(maxresdefault|hqdefault)\.jpg"', f'thumbnail: "{new_thumb}"', content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed thumbnail for {filename} -> {new_thumb}")

print(f"Fixed {count} files.")
