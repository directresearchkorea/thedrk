import os
import re

contact_file = r'c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com\contact\index.html'
with open(contact_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the email info card
content = re.sub(r'<div class="contact__info-card">\s*<div class="contact__info-icon">✉️</div>\s*<h3 class="contact__info-title">Email</h3>\s*<p class="contact__info-text"><a href="mailto:.*?</a></p>\s*</div>', '', content)

with open(contact_file, 'w', encoding='utf-8') as f:
    f.write(content)

print('Removed email box from contact page.')

count = 0
for root, dirs, files in os.walk(r'c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html') or f.endswith('.js') or f.endswith('.json'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                
            if 'drk@thedrk.com' in file_content:
                new_content = file_content.replace('drk@thedrk.com', 'jacob.ahn@thedrk.com')
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1

print(f'Replaced email in {count} files.')
