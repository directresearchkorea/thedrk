import sys
import re

with open('tools/build_post.py', 'r', encoding='utf-8') as f:
    code = f.read()

index_builder = '''
def build_index(posts_meta):
    print('\\n📊 생성: insights/index.html (블로그 목록)')
    
    # Sort posts by date descending
    posts_meta.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Extract unique categories
    categories = []
    for meta in posts_meta:
        cat = meta.get('category', '').lower()
        if cat and cat not in categories:
            categories.append(cat)
            
    # Build filter HTML
    filter_html = '<div class="insights-filter reveal" id="insight-filter">\\n'
    filter_html += '  <button class="insights-filter__btn active" data-filter="all">All</button>\\n'
    for cat in categories:
        filter_html += f'  <button class="insights-filter__btn" data-filter="{cat}">{cat.capitalize()}</button>\\n'
    filter_html += '</div>'
    
    # Build grid HTML
    grid_html = '<div class="insights-grid" id="insights-grid">\\n'
    for meta in posts_meta:
        slug = meta.get('slug', '')
        title = meta.get('title', '')
        desc = meta.get('description', '')
        cat = meta.get('category', '').lower()
        date_str = meta.get('date', '')
        thumb = meta.get('thumbnail', '/assets/images/logo.png')
        
        # Format date
        formatted_date = date_str
        try:
            from datetime import datetime
            d = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_date = d.strftime('%b %d')
        except:
            try:
                from datetime import datetime
                d = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = d.strftime('%b %d')
            except:
                pass
            
        read_time = max(1, len(desc) // 200) # dummy read time
        
        card = f"""
      <a href="/insights/{slug}/" class="card" data-category="{cat}">
        <img src="{thumb}" alt="" class="card__image" loading="lazy">
        <div class="card__body">
          <div class="card__author">
            <div class="card__author-left">
              <img src="/assets/icons/favicon.svg" alt="Dr.K" class="card__avatar">
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
        <div class="card__footer">
          <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          0
        </div>
      </a>"""
        grid_html += card + '\\n'
        
    grid_html += '    </div>'
    
    # Read template
    template_path = SCRIPT_DIR / 'insights-template.html'
    if not template_path.exists():
        print('  ❌ insights-template.html 이 없습니다.')
        return
        
    html = template_path.read_text(encoding='utf-8')
    html = html.replace('<!-- INSIGHTS_FILTER -->', filter_html)
    html = html.replace('<!-- INSIGHTS_GRID -->', grid_html)
    
    # Save index
    INSIGHTS_PAGE.write_text(html, encoding='utf-8')
'''

# Find the end of build_post
code = re.sub(r'def update_sitemap\(posts_meta\):', index_builder + '\n\ndef update_sitemap(posts_meta):', code)

# Update main to call build_index
code = re.sub(r'# sitemap 업데이트\s+if built:\s+update_sitemap\(built\)', '# sitemap 및 목록 업데이트\n    if built:\n        build_index(built)\n        update_sitemap(built)', code)

with open('tools/build_post.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated build_post.py')
