import json
import os

# Regions to cover different parts of Seoul (commercial + residential)
regions = [
    "강남구", "서초구", "송파구", "강동구",  # 강남/동남권
    "영등포구", "마포구", "강서구", "양천구", # 강서/서남권
    "종로구", "중구", "용산구", "성동구",     # 도심/중앙
    "노원구", "강북구", "성북구", "광진구", "동대문구", "은평구", "서대문구" # 강북/동북/서북권
]

foods = {
    "일식": ["일식우동", "일식소바", "우동", "소바"]
}

categories = []

for category_name, subcategories in foods.items():
    cat_obj = {
        "name": category_name,
        "subcategories": []
    }
    for sub_name in subcategories:
        sub_obj = {
            "name": sub_name,
            "keywords": []
        }
        for region in regions:
            # Query format: "Region + Food + Delivery Restaurant"
            sub_obj["keywords"].append(f"{region} {sub_name} 배달 맛집")
            
        cat_obj["subcategories"].append(sub_obj)
    categories.append(cat_obj)

keyword_data = {"categories": categories}

with open("crawler/keywords.json", "w", encoding="utf-8") as f:
    json.dump(keyword_data, f, ensure_ascii=False, indent=2)

print(f"Generated {sum(len(sub['keywords']) for cat in categories for sub in cat['subcategories'])} keywords.")
