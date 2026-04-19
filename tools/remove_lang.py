import os, re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove lang switcher container
    new_content = re.sub(r'<div class="lang-switcher-container">.*?</div>', '', content, flags=re.DOTALL)
    
    # Remove script tags
    new_content = new_content.replace('<script src="/js/translations.js"></script>', '')
    new_content = new_content.replace('<script src="/js/i18n.js"></script>', '')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))
