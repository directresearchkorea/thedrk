import os
import re

def update_html_files(root_dir):
    # Regex to find the end of the services dropdown:
    desktop_regex = re.compile(r'(<a[^>]*href="/services/research-facility/"[^>]*>Research Facility</a>\s*</div>\s*</div>)')
    desktop_replacement = r'\1<a class="nav__link" data-i18n="nav_portfolio" href="/portfolio/">Portfolio</a>'

    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(d in dirpath for d in ['.git', 'venv', 'node_modules']):
            continue
            
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content
                
                # Update desktop nav if missing
                if not re.search(r'<a[^>]*class="nav__link"[^>]*href="/portfolio/"', content):
                    content = desktop_regex.sub(desktop_replacement, content)
                
                # Note: Not touching mobile nav here since earlier scripts handled it, 
                # or the files already had it. We're strictly fixing the missing desktop link.

                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
                    
    print(f"Updated {count} HTML files to add missing desktop Portfolio link.")

if __name__ == '__main__':
    workspace_dir = r"c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com"
    update_html_files(workspace_dir)
