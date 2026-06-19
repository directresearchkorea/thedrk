import os
import re

def fix_html_files(root_dir):
    # Regex to find the incorrectly inserted mobile link before the desktop CTA
    # We look for: <a class="nav__mobile-link" href="/portfolio/">Portfolio</a>\n<a href="/contact/" class="nav__cta"
    error_regex = re.compile(r'<a class="nav__mobile-link" href="/portfolio/">Portfolio</a>\s*(<a[^>]*class="nav__cta"[^>]*>Send RFQ</a>)')
    
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
                
                # Remove the erroneous insertion
                content = error_regex.sub(r'\1', content)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
                    
    print(f"Fixed {count} HTML files.")

if __name__ == '__main__':
    workspace_dir = r"c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com"
    fix_html_files(workspace_dir)
