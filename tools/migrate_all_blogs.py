import os
import sys
import re
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urlparse, unquote

sys.stdout.reconfigure(encoding='utf-8')

POSTS_DIR = 'tools/posts'
IMAGES_DIR = 'assets/images/posts'

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def download_image(url):
    try:
        # Extract base name from Wix URL, e.g. a14e67_1ae6...~mv2.png
        base_name = ""
        match = re.search(r'media/([^/]+\.(png|jpg|jpeg|webp|avif|gif))', url, re.IGNORECASE)
        if match:
            base_name = match.group(1)
            # Reconstruct high-res URL
            full_res_url = f"https://static.wixstatic.com/media/{base_name}"
        else:
            path = urlparse(url).path
            base_name = os.path.basename(path)
            full_res_url = url
            
        if not base_name or base_name == '':
            import uuid
            base_name = str(uuid.uuid4()) + ".jpg"
            full_res_url = url
            
        filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', base_name)
        filepath = os.path.join(IMAGES_DIR, filename)
        
        if not os.path.exists(filepath):
            req = urllib.request.Request(full_res_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
                
        return f"/assets/images/posts/{filename}"
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        return url

def migrate_all():
    print("Fetching blog-posts-sitemap.xml...", flush=True)
    try:
        req = urllib.request.Request('https://www.thedrk.com/blog-posts-sitemap.xml', headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=15)
        sitemap_xml = response.read()
    except Exception as e:
        print("Failed to fetch sitemap:", e, flush=True)
        return

    tree = ET.fromstring(sitemap_xml)
    urls = [loc.text for loc in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if loc.text]
    
    print(f"Found {len(urls)} blog URLs to process.", flush=True)
    
    for url in urls:
        if '/post/' not in url:
            continue
            
        slug = url.split('/')[-1]
        slug = unquote(slug)
        slug = re.sub(r'[^a-zA-Z0-9_\-]', '-', slug).lower()
        slug = re.sub(r'-+', '-', slug).strip('-')
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            title_tag = soup.find('title')
            if not title_tag:
                continue
            title = title_tag.text.split('|')[0].strip()
            
            # Skip non-English
            if re.search(r'[가-힣\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]', title):
                print(f"Skipping non-English post: {title}", flush=True)
                continue
                
            print(f"Migrating: {title}", flush=True)
            
            meta_date = soup.find('meta', property='article:published_time')
            date = meta_date['content'] if meta_date else ''
            
            meta_desc = soup.find('meta', property='og:description')
            description = meta_desc['content'] if meta_desc else ''
            
            meta_img = soup.find('meta', property='og:image')
            thumbnail_url = meta_img['content'] if meta_img else ''
            thumbnail_local = download_image(thumbnail_url) if thumbnail_url else ''
            
            article = soup.find('article')
            if not article:
                print(f"  No article tag found for {url}", flush=True)
                continue
                
            # Remove unrelated elements
            for el in article.find_all(attrs={"data-hook": ["post-footer", "social-shares", "comments"]}):
                el.decompose()
                
            # Find and download images
            for img in article.find_all('img'):
                src = img.get('src')
                if src and src.startswith('http'):
                    local_src = download_image(src)
                    img['src'] = local_src
                    
            # Convert to markdown
            markdown_content = md(str(article), heading_style="ATX", strip=['a'])
            
            frontmatter = f"""---
title: "{title.replace('"', "'")}"
date: "{date}"
category: "Insights"
thumbnail: "{thumbnail_local}"
description: "{description.replace('"', "'")}"
---

"""
            
            filepath = os.path.join(POSTS_DIR, f"{slug}.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            print(f"  Saved {slug}.md", flush=True)
                
        except Exception as e:
            print(f"  Error fetching {url}: {e}", flush=True)

if __name__ == '__main__':
    migrate_all()
