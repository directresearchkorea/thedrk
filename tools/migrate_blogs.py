import os
import sys
import re
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urlparse

# Directories
POSTS_DIR = 'tools/posts'
IMAGES_DIR = 'assets/images/posts'

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def download_image(url):
    try:
        # Handle Wix image URLs which often look like:
        # https://static.wixstatic.com/media/a14e67_1ae65c7ea1194f97b6e505c34e5348d2~mv2.png/v1/fit/w_1000,h_1000,al_c,q_80/file.png
        # We extract the base filename e.g. a14e67_1ae65c7ea...~mv2.png
        
        base_name = ""
        match = re.search(r'media/([^/]+\.(png|jpg|jpeg|webp|avif))', url, re.IGNORECASE)
        if match:
            base_name = match.group(1)
        else:
            path = urlparse(url).path
            base_name = os.path.basename(path)
            
        if not base_name or base_name == '':
            import uuid
            base_name = str(uuid.uuid4()) + ".jpg"
            
        # Clean filename
        filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', base_name)
        
        filepath = os.path.join(IMAGES_DIR, filename)
        
        if not os.path.exists(filepath):
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            
        return f"/assets/images/posts/{filename}"
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        return url

def migrate():
    if not os.path.exists('feed.xml'):
        print("feed.xml not found. Please download it first.")
        return

    tree = ET.parse('feed.xml')
    root = tree.getroot()
    channel = root.find('channel')
    
    for item in channel.findall('item'):
        title = item.find('title').text if item.find('title') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''
        category = item.find('category').text if item.find('category') is not None else 'Uncategorized'
        description = item.find('description').text if item.find('description') is not None else ''
        
        # Strip CDATA and weird characters
        title = title.replace('<![CDATA[', '').replace(']]>', '').strip()
        description = description.replace('<![CDATA[', '').replace(']]>', '').strip()
        category = category.replace('<![CDATA[', '').replace(']]>', '').strip()
        
        # Clean description HTML tags
        description = re.sub(r'<[^>]+>', '', description)
        
        # Skip non-English posts (containing Korean, Japanese, or Chinese characters in title)
        if re.search(r'[가-힣\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]', title):
            print(f"Skipping non-English post: {title}")
            continue
        
        enclosure = item.find('enclosure')
        thumbnail_url = enclosure.get('url') if enclosure is not None else ''
        thumbnail_local = download_image(thumbnail_url) if thumbnail_url else ''
        
        slug = link.split('/')[-1]
        if not slug:
            continue
            
        # URL decode slug
        from urllib.parse import unquote
        slug = unquote(slug)
        # Remove weird characters from slug
        slug = re.sub(r'[^a-zA-Z0-9_\-]', '-', slug).lower()
        slug = re.sub(r'-+', '-', slug).strip('-')
        
        print(f"Migrating: {title} ({slug})")
        
        # Fetch full HTML
        try:
            req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find the main article
            articles = soup.find_all('article')
            if not articles:
                print(f"  No article found for {link}")
                continue
            
            # The first article is usually the main one
            article = articles[0]
            
            # Remove unrelated elements (like comments, footer inside article, social shares)
            for el in article.find_all(attrs={"data-hook": ["post-footer", "social-shares", "comments"]}):
                el.decompose()
                
            # Find images in article and download them, rewrite src
            for img in article.find_all('img'):
                src = img.get('src')
                if src and src.startswith('http'):
                    local_src = download_image(src)
                    img['src'] = local_src
                    
            # Convert to markdown
            markdown_content = md(str(article), heading_style="ATX", strip=['a'])
            
            # Create YAML frontmatter
            frontmatter = f"""---
title: "{title.replace('"', "'")}"
date: "{pubDate}"
category: "{category}"
thumbnail: "{thumbnail_local}"
description: "{description.replace('"', "'")}"
---

"""
            
            # Save file
            filepath = os.path.join(POSTS_DIR, f"{slug}.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
                
        except Exception as e:
            print(f"  Error fetching {link}: {e}")

if __name__ == '__main__':
    migrate()
