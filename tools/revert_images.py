import os

POSTS_DIR = 'tools/posts'
count = 0

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith('.md'): continue
    
    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '<!-- Recovered Missing Images -->' in content:
        # Split by the comment and keep only the first part
        new_content = content.split('<!-- Recovered Missing Images -->')[0].strip() + '\n'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Reverted {count} files by removing the mistaken recent posts thumbnails.')
