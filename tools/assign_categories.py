import os
import re

post_dir = 'tools/posts'
categories_map = {
    'Gaming': [r'\bgame\b', r'\bgaming\b', r'\besport\b', r'\besports\b', r'\bsteam\b', r'\bplatform\b'],
    'Car': [r'\bcar\b', r'\bcars\b', r'\bev\b', r'\bevs\b', r'\bvehicle\b', r'\bauto\b', r'\bmotor\b'],
    'Alcohols': [r'\balcohol\b', r'\bwine\b', r'\bwhiskey\b', r'\bdrink\b', r'\bliquor\b', r'\bbeer\b', r'\bsoju\b'],
    'COVIDs': [r'\bcovid\b', r'\bcovid-19\b', r'\bpandemic\b', r'\bmigration\b'],
    'Events & Awards': [r'\baward\b', r'\bevent\b', r'\bpopcon\b', r'\bg-star\b', r'\bbiff\b', r'\bexpo\b', r'\bfestival\b'],
    'Movie & Annimation': [r'\bmovie\b', r'\bfilm\b', r'\bcinema\b', r'\bbroadcast\b', r'\btv\b', r'\banimation\b', r'\bnetflix\b', r'\bcontent\b'],
    'Consumers': [r'\bconsumer\b', r'\bmz\b', r'\bgeneration\b', r'\btrend\b', r'\blifestyle\b', r'\bshoppers\b'],
    'Pet': [r'\bpet\b', r'\bdog\b', r'\bcat\b', r'\banimal\b', r'\bveterinary\b'],
    'Beauty': [r'\bbeauty\b', r'\bcosmetic\b', r'\bcosmetics\b', r'\bskin\b', r'\bskincare\b', r'\bmakeup\b'],
    'Retail': [r'\bretail\b', r'\bstore\b', r'\boffline\b', r'\bshop\b', r'\bpackage\b', r'\bcommerce\b', r'\bdelivery\b'],
    'Service & Cases': [r'\bservice\b', r'\bcase\b', r'\bfield\b', r'\bcompetitiveness\b', r'\bmethodology\b', r'\bresearch\b', r'\binsight\b'],
    'Training & Lectures': [r'\btraining\b', r'\blecture\b', r'\bclass\b', r'\beducation\b']
}

count = 0
for file in os.listdir(post_dir):
    if not file.endswith('.md'): continue
    path = os.path.join(post_dir, file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'^title:\s*"(.*?)"', content, flags=re.MULTILINE)
    title = match.group(1).lower() if match else file.lower()
    
    assigned_cats = set()
    for cat, keywords in categories_map.items():
        for kw in keywords:
            if re.search(kw, title, re.IGNORECASE):
                assigned_cats.add(cat)
                break
            
    if not assigned_cats:
        assigned_cats.add('Insights')
        
    cat_str = ', '.join(assigned_cats)
    
    # Replace category line
    new_content = re.sub(r'^category:\s*".*?"', f'category: "{cat_str}"', content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Updated categories for {count} posts based on strict keywords.')
