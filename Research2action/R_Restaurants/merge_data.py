import csv
import glob
import os

DAY_MAPPING = {
    '강남구': 1, '서초구': 1, '송파구': 1,
    '강서구': 2, '양천구': 2, '구로구': 2,
    '마포구': 3, '서대문구': 3, '은평구': 3,
    '영등포구': 4, '동작구': 4, '관악구': 4,
    '종로구': 5, '중구': 5, '용산구': 5,
    '성동구': 6, '광진구': 6, '동대문구': 6,
    '성북구': 7, '강북구': 7, '도봉구': 7, '노원구': 7,
    '중랑구': 8, '강동구': 8, '금천구': 8
}

def get_day(address, keyword):
    for gu, day in DAY_MAPPING.items():
        if gu in address or gu in keyword:
            return day
    return 8

def get_segment(row):
    cat = row.get('category', '')
    sub = row.get('subcategory', '')
    kw = row.get('keyword', '')
    name = row.get('name', '')
    
    combined = f"{sub} {kw} {name}".lower()
    
    # Explicit Priority Mappings per User Request
    seafood_stew_keywords = ['해물순두부', '동태탕', '대구탕', '해물탕', '꽃게탕', '알탕', '동태찌개', '대구지리']
    if any(x in combined for x in seafood_stew_keywords):
        return '8. 한식 (해물 찌개・탕 전문점)'
        
    if any(x in combined for x in ['생선회', '횟집', '활어']):
        return '6. 한식 (해물 정식・회 전문점)'
    
    if cat == '일식':
        if any(x in combined for x in ['이자카야', '선술집', '오뎅', '꼬치']): return '1. 일식 (선술집)'
        elif any(x in combined for x in ['초밥', '스시', '정식', '돈카츠', '돈까스']): return '2. 일식 (정식・초밥)'
        elif any(x in combined for x in ['우동', '소바', '모밀']): return '3. 일식 (우동・소바)'
        else: return '4. 일식 (기타 전문점：카레・라면 등)'
    elif cat == '한식':
        is_seafood = any(x in combined for x in ['해물', '아구', '아귀', '회', '생선', '동태', '대구', '낙지', '쭈꾸미', '주꾸미', '새우', '오징어'])
        is_stew = any(x in combined for x in ['찌개', '탕', '국', '순두부'])
        is_normal_stew = any(x in combined for x in ['김치찌개', '된장찌개', '부대찌개', '갈비탕', '삼계탕', '감자탕', '설렁탕', '곰탕', '국밥', '순대'])
        is_normal_meal = any(x in combined for x in ['제육', '백반', '된장', '비빔밥', '정식', '쌈밥', '보리밥'])
        
        if is_seafood:
            if is_stew: return '8. 한식 (해물 찌개・탕 전문점)'
            else: return '6. 한식 (해물 정식・회 전문점)'
        elif is_normal_stew: return '7. 한식 (일반 찌개・탕 전문점)'
        elif is_normal_meal: return '5. 한식 (일반 정식)'
        else: return '9. 한식 (기타 전문점：고기 구이・냉면・칼국수 등)'
            
    return '0. 미분류'

def main():
    base_csv = "data/restaurants.csv"
    chunk_files = glob.glob("data/restaurants_*.csv")
    
    records = {}
    
    # Load base records
    if os.path.exists(base_csv):
        with open(base_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records[row["place_id"]] = row
                
    # Overwrite with enriched chunk records
    for cf in chunk_files:
        with open(cf, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records[row["place_id"]] = row

    # Add route_day
    final_records = list(records.values())
    for r in final_records:
        r["route_day"] = get_day(r.get("address", ""), r.get("keyword", ""))
        r["segment"] = get_segment(r)
        
    # Write to restaurants_final.csv
    fieldnames = ["place_id", "category", "subcategory", "segment", "keyword", "name", "address", "route_day", "phone", "hours"]
    
    with open("data/restaurants_final.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(final_records)
        
    print(f"Successfully merged {len(final_records)} records into restaurants_final.csv")

if __name__ == "__main__":
    main()
