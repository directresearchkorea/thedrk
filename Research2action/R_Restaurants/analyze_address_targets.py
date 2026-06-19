import csv
import re
import json
from collections import Counter, defaultdict

csv_path = 'data/restaurants_final.csv'

# To map subcategory back to its primary high-level category
subcat_to_cat = {}
dong_counter = Counter()

dong_pattern = re.compile(r'[가-힣0-9]+(?:동|가)\b')

with open(csv_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        sub = row.get('subcategory')
        cat = row.get('category')
        if sub and cat:
            subcat_to_cat[sub] = cat
        
        addr = row.get('address', '')
        if not addr:
            continue
            
        words = addr.split()
        found_dong = None
        for word in words:
            if dong_pattern.search(word):
                clean_word = re.sub(r'[^\w]', '', word)
                if clean_word.endswith(('동', '가')):
                    prefix = re.sub(r'(동|가)', '', clean_word)
                    if not prefix.isdigit(): # Skip apt complexes like 101동
                        found_dong = clean_word
                        break
        
        if not found_dong and len(words) >= 3:
            clean_word = re.sub(r'[^\w]', '', words[2])
            if clean_word.endswith(('동', '가', '로')):
                found_dong = clean_word
                
        if found_dong:
            dong_counter[found_dong] += 1

# Top 45 commercial centers
dense_dongs = [dong for dong, count in dong_counter.most_common(45)]

# Organize into old structure: categories -> subcategories -> keywords list
# Nested default dict: categories -> subcategory -> list of queries
nested_struct = defaultdict(lambda: defaultdict(list))

for dong in dense_dongs:
    for sub, cat in subcat_to_cat.items():
        # Format: "동/로 + 업종이름"
        query = f"{dong} {sub}"
        nested_struct[cat][sub].append(query)

# Convert to standard dict for json
output_categories = []
for cat_name, subs_dict in nested_struct.items():
    subcat_list = []
    for sub_name, queries in subs_dict.items():
        subcat_list.append({
            "name": sub_name,
            "keywords": queries
        })
    output_categories.append({
        "name": cat_name,
        "subcategories": subcat_list
    })

final_json = {
    "categories": output_categories
}

# Save to keywords.json
keywords_path = 'crawler/keywords.json'
with open(keywords_path, 'w', encoding='utf-8') as fj:
    json.dump(final_json, fj, ensure_ascii=False, indent=4)

print(f"Structured output generated for {len(output_categories)} categories.")
print(f"Successfully updated {keywords_path} with compatibility schema.")
