import os
import re

post_dir = 'tools/posts'

count = 0
for file in os.listdir(post_dir):
    if not file.endswith('.md'):
        continue
    
    path = os.path.join(post_dir, file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the end of frontmatter
    match = re.search(r'^---\n.*?\n---\n\n', content, re.DOTALL)
    if not match:
        continue
    
    frontmatter_end = match.end()
    frontmatter = content[:frontmatter_end]
    body = content[frontmatter_end:]
    
    original_body = body
    
    # Remove block starting with "The Dr.K" and ending with "min read"
    # This block spans multiple lines
    body = re.sub(r'^\s*The Dr\.K.*?min read\s*', '', body, flags=re.DOTALL | re.MULTILINE)
    
    # Also remove "Updated: ...."
    body = re.sub(r'^Updated:.*?\n', '', body, flags=re.MULTILINE)
    
    # Remove excessive newlines at the start of the body
    body = re.sub(r'^\s+', '', body)
    
    if body != original_body:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + body)
        count += 1

print(f"Cleaned {count} markdown files.")
