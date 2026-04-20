import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 경로 설정
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
POSTS_DIR = SCRIPT_DIR / "posts"
TEMPLATE_PATH = SCRIPT_DIR / "post-template.html"
OUTPUT_DIR = PROJECT_ROOT / "insights"
SITEMAP_PATH = PROJECT_ROOT / "sitemap.xml"
INSIGHTS_PAGE = OUTPUT_DIR / "index.html"


def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        print("  ⚠️  Frontmatter not found. Expected metadata wrapped in ---")
        return None, content
    
    meta_text = match.group(1)
    body = match.group(2)
    
    meta = {}
    for line in meta_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    
    return meta, body


def markdown_to_html(md_text):
    lines = md_text.strip().split('\n')
    html_lines = []
    in_list = False
    in_blockquote = False
    paragraph = []
    
    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            text = ' '.join(paragraph)
            text = convert_inline(text)
            html_lines.append(f'<p>{text}</p>')
            paragraph = []
    
    def convert_inline(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            flush_paragraph()
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            continue
        
        if stripped.startswith('### '):
            flush_paragraph()
            text = convert_inline(stripped[4:])
            html_lines.append(f'<h3>{text}</h3>')
            continue
        if stripped.startswith('## '):
            flush_paragraph()
            text = convert_inline(stripped[3:])
            html_lines.append(f'<h2>{text}</h2>')
            continue
        
        if stripped.startswith('> '):
            flush_paragraph()
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            text = convert_inline(stripped[2:])
            html_lines.append(f'<p>{text}</p>')
            continue
        
        if stripped.startswith('- ') or stripped.startswith('• '):
            flush_paragraph()
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = convert_inline(stripped[2:])
            html_lines.append(f'<li>{text}</li>')
            continue
        
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            flush_paragraph()
            alt = img_match.group(1)
            src = img_match.group(2)
            html_lines.append(f'<img src="{src}" alt="{alt}" loading="lazy">')
            continue
        
        if stripped in ('---', '***', '___'):
            flush_paragraph()
            html_lines.append('<hr class="divider">')
            continue
        
        paragraph.append(stripped)
    
    flush_paragraph()
    if in_list:
        html_lines.append('</ul>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n      '.join(html_lines)


def build_post(md_path):
    print(f"\n📝 Building: {md_path.name}")
    
    content = md_path.read_text(encoding='utf-8')
    meta, body = parse_frontmatter(content)
    
    if not meta:
        print("  ❌ No metadata — skipping.")
        return None
    
    required = ['title', 'description', 'category', 'date']
    for field in required:
        if field not in meta:
            print(f"  ❌ Missing required field: {field}")
            return None
    
    if 'slug' not in meta:
        meta['slug'] = md_path.stem
        
    if not meta.get('thumbnail') or meta.get('thumbnail').strip() == '':
        # Search for youtube embed in body
        yt_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', body)
        if yt_match:
            meta['thumbnail'] = f"https://i.ytimg.com/vi/{yt_match.group(1)}/maxresdefault.jpg"
        else:
            img_match = re.search(r'!\[.*?\]\((.*?)\)', body)
            if img_match:
                meta['thumbnail'] = img_match.group(1)
            else:
                meta['thumbnail'] = '/assets/images/logo.png'
        
    html_body = markdown_to_html(body)
    
    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    
    html = template.replace('%%TITLE%%', meta['title'])
    html = html.replace('%%DESCRIPTION%%', meta['description'])
    html = html.replace('%%SLUG%%', meta['slug'])
    # Parse and format the date cleanly
    try:
        from datetime import datetime
        d = datetime.strptime(meta['date'][:10], '%Y-%m-%d')
        formatted_date = d.strftime('%Y-%m-%d')
    except:
        formatted_date = meta['date'][:10]
        
    html = html.replace('%%DATE%%', formatted_date)
    html = html.replace('%%CATEGORY%%', meta['category'])
    html = html.replace('%%CONTENT%%', html_body)
    
    thumb_url = meta.get('thumbnail', '')
    if thumb_url and not thumb_url.startswith('http'):
        if not thumb_url.startswith('/'):
            thumb_url = '/' + thumb_url
        thumb_url = f"https://thedrk.com{thumb_url}"
    html = html.replace('%%THUMBNAIL%%', thumb_url)
    
    output_dir = OUTPUT_DIR / meta['slug']
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'index.html'
    output_file.write_text(html, encoding='utf-8')
    
    print(f"  ✅ Created: insights/{meta['slug']}/index.html")
    return meta

def build_index(posts_meta):
    print('\n📊 Created: insights/index.html (Blog Index)')
    
    posts_meta.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    categories = set()
    for meta in posts_meta:
        cats = [c.strip().lower() for c in meta.get('category', '').split(',') if c.strip()]
        categories.update(cats)
        
    categories = sorted(list(categories))
    
    template_path = SCRIPT_DIR / 'insights-template.html'
    if not template_path.exists():
        print('  ❌ insights-template.html is missing.')
        return
        
    template = template_path.read_text(encoding='utf-8')
    
    def create_page(target_path, active_cat, display_posts):
        filter_html = '<div class="insights-filter reveal" id="insight-filter">\n'
        active_class = ' active' if active_cat == 'all' else ''
        filter_html += f'  <a href="/insights/" class="insights-filter__btn{active_class}">All</a>\n'
        for cat in categories:
            cat_display = cat.title()
            active_class = ' active' if active_cat == cat else ''
            filter_html += f'  <a href="/insights/{cat}/" class="insights-filter__btn{active_class}">{cat_display}</a>\n'
        filter_html += '</div>'
        
        grid_html = '<div class="insights-grid" id="insights-grid">\n'
        for meta in display_posts:
            slug = meta.get('slug', '')
            title = meta.get('title', '')
            desc = meta.get('description', '')
            cats_raw = [c.strip().lower() for c in meta.get('category', '').split(',') if c.strip()]
            cat_str = ','.join(cats_raw)
            date_str = meta.get('date', '')
            thumb = meta.get('thumbnail', '/assets/images/logo.png')
            if not thumb or thumb.strip() == '':
                thumb = '/assets/images/logo.png'
            
            formatted_date = date_str[:10]
            try:
                from datetime import datetime
                d = datetime.strptime(date_str[:10], '%Y-%m-%d')
                formatted_date = d.strftime('%Y-%m-%d')
            except:
                pass
                
            read_time = max(1, len(desc) // 200)
            
            card = f"""
      <a href="/insights/{slug}/" class="card" data-category="{cat_str}">
        <img src="{thumb}" alt="" class="card__image" loading="lazy">
        <div class="card__body">
          <div class="card__author">
            <div class="card__author-left">
              <div class="card__author-info">
                <span class="card__author-name">The Dr.K</span>
                <span class="card__author-meta">{formatted_date} · {read_time} min read</span>
              </div>
            </div>
            <div class="card__more-icon">⋮</div>
          </div>
          <h2 class="card__title">{title}</h2>
          <p class="card__excerpt">{desc}</p>
        </div>
      </a>"""
            grid_html += card + '\n'
            
        grid_html += '    </div>'
        
        html = template.replace('<!-- INSIGHTS_FILTER -->', filter_html)
        html = html.replace('<!-- INSIGHTS_GRID -->', grid_html)
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(html, encoding='utf-8')

    # Main page
    create_page(INSIGHTS_PAGE, 'all', posts_meta)
    
    # Category pages
    for cat in categories:
        cat_posts = [m for m in posts_meta if cat in [c.strip().lower() for c in m.get('category', '').split(',') if c.strip()]]
        cat_path = OUTPUT_DIR / cat / "index.html"
        create_page(cat_path, cat, cat_posts)
        print(f"  ✅ Created: insights/{cat}/index.html")
def update_sitemap(posts_meta):
    if not posts_meta:
        return
    
    sitemap = SITEMAP_PATH.read_text(encoding='utf-8')
    
    for meta in posts_meta:
        url = f"https://thedrk.com/insights/{meta['slug']}/"
        if url not in sitemap:
            entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{meta['date']}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>"""
            sitemap = sitemap.replace('</urlset>', f'{entry}\n</urlset>')
    
    SITEMAP_PATH.write_text(sitemap, encoding='utf-8')
    print(f"\n🗺️  sitemap.xml updated ({len(posts_meta)}URLs added)")


def main():
    print("=" * 50)
    print("🔨 Direct Research Korea — Blog Post Builder")
    print("=" * 50)
    
    if not POSTS_DIR.exists():
        POSTS_DIR.mkdir(parents=True)
    
    if len(sys.argv) > 1:
        md_files = [POSTS_DIR / sys.argv[1]]
    else:
        md_files = sorted(POSTS_DIR.glob('*.md'))
    
    if not md_files:
        print("\n⚠️  No post files found.")
        return
    
    print(f"\n📂 {len(md_files)}files found")
    
    built = []
    for md_path in md_files:
        if md_path.exists():
            meta = build_post(md_path)
            if meta:
                built.append(meta)
        else:
            print(f"\n❌ File not found: {md_path}")
    
    if built:
        build_index(built)
        update_sitemap(built)
    
    print(f"\n{'=' * 50}")
    print(f"✨ Done! {len(built)}posts built")
    print(f"{'=' * 50}")


if __name__ == '__main__':
    main()
