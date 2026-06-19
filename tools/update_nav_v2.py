import os
import re

def update_html_files(root_dir):
    # Regex for desktop nav: find the Research Facility link and the two closing divs
    desktop_regex = re.compile(r'(href="/services/research-facility/"[^>]*>Research Facility</a>\s*</div>\s*</div>)')
    desktop_replacement = r'\1\n        <a class="nav__link" href="/portfolio/">Portfolio</a>'

    # Regex for mobile nav: find the Send RFQ link
    mobile_regex = re.compile(r'(<a[^>]*href="/contact/"[^>]*>Send RFQ</a>)')
    mobile_replacement = r'<a class="nav__mobile-link" href="/portfolio/">Portfolio</a>\n\1'

    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(d in dirpath for d in ['.git', 'venv', 'node_modules']):
            continue
            
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Skip if already updated
                if 'href="/portfolio/"' in content:
                    continue

                original_content = content
                
                # Update desktop nav
                content = desktop_regex.sub(desktop_replacement, content)
                
                # Update mobile nav
                content = mobile_regex.sub(mobile_replacement, content)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
                    
    print(f"Updated {count} HTML files.")

if __name__ == '__main__':
    workspace_dir = r"c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com"
    update_html_files(workspace_dir)
