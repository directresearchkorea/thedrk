import os
import re

POSTS_DIR = r'c:\Users\ggamy\OneDrive\Desktop\H_thedrk.com\tools\posts'
count = 0

for filename in os.listdir(POSTS_DIR):
    if not filename.endswith('.md'): continue
    filepath = os.path.join(POSTS_DIR, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the file into lines
    lines = content.split('\n')
    new_lines = []
    
    in_frontmatter = False
    frontmatter_count = 0
    
    for line in lines:
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count <= 2:
                in_frontmatter = frontmatter_count == 1
                new_lines.append(line)
                continue
                
        if in_frontmatter:
            new_lines.append(line)
            continue
            
        # If we are in the body, remove artifacts
        # 1. Remove Writer image
        if line.strip().startswith('* ![Writer:') or line.strip().startswith('![Writer:'):
            continue
            
        # 2. Remove 'min read' line
        if 'min read' in line:
            continue
            
        # 3. Remove Updated: line
        if line.strip().startswith('Updated: '):
            continue
            
        new_lines.append(line)
        
    # Remove consecutive empty lines at the start of the body
    body_start_idx = 0
    for i, line in enumerate(new_lines):
        if line.strip() == '---':
            if i > 0: # This is the second ---
                body_start_idx = i + 1
                break
                
    # Trim empty lines directly after frontmatter and first H1
    i = body_start_idx
    while i < len(new_lines) and new_lines[i].strip() == '':
        del new_lines[i]
        
    # The first line is usually the H1. Let's make sure the empty lines after H1 are not too many
    if i < len(new_lines) and new_lines[i].startswith('# '):
        i += 1
        while i < len(new_lines) and new_lines[i].strip() == '':
            del new_lines[i]
        # Insert exactly one empty line after H1 for formatting
        new_lines.insert(i, '')

    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Cleaned up author metadata in {count} files.")
