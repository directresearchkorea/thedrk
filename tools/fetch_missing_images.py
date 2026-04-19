import os
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

POSTS_DIR = 'tools/posts'
IMAGES_DIR = 'assets/images/posts'
GLOBAL_EXCLUDE = ['a14e67_27ef640b583c4ddc90e9c87cfb560f09'] # Dr.K Avatar

def download_image(hash_name):
    url = f"https://static.wixstatic.com/media/{hash_name}"
    # Replace ~mv2 with _mv2 for local filesystem consistency as done in previous script
    local_filename = hash_name.replace('~mv2', '_mv2')
    local_filepath = os.path.join(IMAGES_DIR, local_filename)
    
    if os.path.exists(local_filepath):
        return f"/assets/images/posts/{local_filename}"
        
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(local_filepath, 'wb') as out_file:
                out_file.write(response.read())
        return f"/assets/images/posts/{local_filename}"
    except Exception as e:
        print(f"  [ERROR] Failed to download {hash_name}: {e}")
        return None

count_files_updated = 0
total_images_recovered = 0

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith('.md'): continue
    
    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Get original URL from slug
    slug = filename[:-3]
    wix_url = f"https://www.thedrk.com/post/{slug}"
    
    try:
        req = urllib.request.Request(wix_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    except Exception as e:
        print(f"Could not fetch HTML for {slug}: {e}")
        continue
        
    # 2. Extract all wix image hashes
    wix_hashes_full = set(re.findall(r'(a14e67_[a-zA-Z0-9]+~mv2\.(?:jpg|png|webp|jpeg))', html))
    
    # Extract base hashes without extension to compare with markdown
    wix_hashes = set()
    for full in wix_hashes_full:
        base_hash = full.split('~mv2')[0]
        if base_hash not in GLOBAL_EXCLUDE:
            wix_hashes.add(full)
            
    if not wix_hashes:
        continue
        
    # 3. Check markdown to see what hashes are already there
    missing = []
    for full_hash in wix_hashes:
        base_hash = full_hash.split('~mv2')[0]
        # Previous script saved them as _mv2
        if base_hash not in content:
            missing.append(full_hash)
            
    if missing:
        print(f"Found {len(missing)} missing images for {slug}")
        recovered_md = "\n\n<!-- Recovered Missing Images -->\n"
        added = False
        for m_hash in missing:
            local_path = download_image(m_hash)
            if local_path:
                recovered_md += f"![Recovered Image]({local_path})\n\n"
                added = True
                total_images_recovered += 1
                
        if added:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(recovered_md)
            count_files_updated += 1

print(f"\nRecovery Complete! Recovered {total_images_recovered} images across {count_files_updated} posts.")
