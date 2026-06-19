import csv
import re
from collections import defaultdict

csv_path = 'data/restaurants_final.csv'
output_path = 'data/sales_routes_optimized.csv'

# Define Tiers based on segments
TIER_1_SEGMENTS = ['1. 일식 (선술집)', '3. 일식 (우동・소바)', '8. 한식 (해물 찌개・탕 전문점)']
TIER_2_SEGMENTS = ['7. 한식 (일반 찌개・탕 전문점)', '2. 일식 (정식・초밥)']

def get_dong(address):
    # Extract neighborhood (Dong) for clustering
    dong_pattern = re.compile(r'[가-힣0-9]+(?:동|가)\b')
    words = address.split()
    for word in words:
        if dong_pattern.search(word):
            clean = re.sub(r'[^\w]', '', word)
            if clean.endswith(('동', '가')):
                prefix = re.sub(r'(동|가)', '', clean)
                if not prefix.isdigit():
                    return clean
    if len(words) >= 3:
        return words[1] + " " + words[2] # Fallback to Gu + Dong roughly
    return "기타 지역"

# Group by Dong -> Tier -> List of Records
clusters = defaultdict(lambda: {1: [], 2: []})

with open(csv_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        seg = row.get('segment', '')
        addr = row.get('address', '')
        if not addr: continue
        
        dong = get_dong(addr)
        
        if any(t in seg for t in TIER_1_SEGMENTS):
            clusters[dong][1].append(row)
        elif any(t in seg for t in TIER_2_SEGMENTS):
            clusters[dong][2].append(row)

# Build Routes
routes = []
route_id = 1

# Flatten to district/gu level if dongs don't have enough, but for simplicity, we'll pool by 'Gu'
gu_clusters = defaultdict(lambda: {1: [], 2: []})
for dong, data in clusters.items():
    # Extract Gu from the first record's address
    if data[1] or data[2]:
        sample_addr = (data[1] + data[2])[0]['address']
        gu_match = re.search(r'([가-힣]+구)\b', sample_addr)
        gu = gu_match.group(1) if gu_match else "기타"
        
        gu_clusters[gu][1].extend(data[1])
        gu_clusters[gu][2].extend(data[2])

# Create 10+10 routes per Gu
route_records = []
for gu, data in gu_clusters.items():
    t1_pool = sorted(data[1], key=lambda x: x['address'])
    t2_pool = sorted(data[2], key=lambda x: x['address'])
    
    while len(t1_pool) >= 10 and len(t2_pool) >= 10:
        # Take 10 from each
        selected_t1 = t1_pool[:10]
        selected_t2 = t2_pool[:10]
        t1_pool = t1_pool[10:]
        t2_pool = t2_pool[10:]
        
        route_name = f"Route {route_id} ({gu} 밀집)"
        for r in selected_t1:
            r['route_id'] = route_name
            r['tier'] = 'Tier 1 (High)'
            route_records.append(r)
        for r in selected_t2:
            r['route_id'] = route_name
            r['tier'] = 'Tier 2 (Medium)'
            route_records.append(r)
            
        route_id += 1

# Write output
if route_records:
    fieldnames = ['place_id', 'route_id', 'tier', 'segment', 'name', 'address', 'phone', 'subcategory', 'keyword']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(route_records)
    print(f"Successfully generated {route_id - 1} optimized routes in {output_path}")
else:
    print("Not enough paired data to create strict 10+10 routes.")
