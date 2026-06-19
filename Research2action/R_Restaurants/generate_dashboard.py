import csv
import json
import os
import random
from datetime import datetime

csv_path = 'data/restaurants.csv'
html_path = 'dashboard.html'

data = []
if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

# Load optimized sales routes mapping
sales_routes_mapping = {}
route_list_names = []
routes_csv = 'data/sales_routes_optimized.csv'
if os.path.exists(routes_csv):
    with open(routes_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row.get('place_id')
            rid = row.get('route_id')
            if pid and rid:
                sales_routes_mapping[pid] = rid
                if rid not in route_list_names:
                    route_list_names.append(rid)

for item in data:
    pid = item.get('place_id')
    item['sales_route'] = sales_routes_mapping.get(pid, None)

# Day Mapping based on Seoul Districts (Gu)
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

GU_COORDS = {
    '강남구': (37.5172, 127.0473), '서초구': (37.4837, 127.0324), '송파구': (37.5145, 127.1066),
    '강서구': (37.5509, 126.8495), '양천구': (37.5169, 126.8660), '구로구': (37.4954, 126.8874),
    '마포구': (37.5665, 126.9018), '서대문구': (37.5791, 126.9368), '은평구': (37.6027, 126.9291),
    '영등포구': (37.5264, 126.8962), '동작구': (37.5124, 126.9393), '관악구': (37.4784, 126.9516),
    '종로구': (37.5729, 126.9794), '중구': (37.5636, 126.9975), '용산구': (37.5325, 126.9900),
    '성동구': (37.5635, 127.0368), '광진구': (37.5385, 127.0823), '동대문구': (37.5744, 127.0400),
    '성북구': (37.5891, 127.0182), '강북구': (37.6396, 127.0257), '도봉구': (37.6688, 127.0471),
    '노원구': (37.6542, 127.0568), '중랑구': (37.6065, 127.0924), '강동구': (37.5301, 127.1238),
    '금천구': (37.4568, 126.8954)
}

def get_day(address, keyword):
    for gu, day in DAY_MAPPING.items():
        if gu in address or gu in keyword:
            return day
    return 8 # Default to Day 8 for others

def get_gu(address, keyword):
    for gu in DAY_MAPPING.keys():
        if gu in address or gu in keyword:
            return gu
    return '종로구'

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

for item in data:
    item['day'] = get_day(item.get('address', ''), item.get('keyword', ''))
    item['segment'] = get_segment(item)
    gu = get_gu(item.get('address', ''), item.get('keyword', ''))
    base_lat, base_lng = GU_COORDS.get(gu, (37.5665, 126.9780))
    # Add small random offset to simulate actual spread
    item['lat'] = base_lat + random.uniform(-0.02, 0.02)
    item['lng'] = base_lng + random.uniform(-0.02, 0.02)
    item['gu'] = gu

json_data = json.dumps(data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurants Recruitment Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/lucide-static@0.321.0/lib/index.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        :root {{
            --bg-color: #f8f9fa;
            --surface-color: #ffffff;
            --text-primary: #121212;
            --text-secondary: #6c757d;
            --border-color: #e9ecef;
            --accent-primary: #000000;
            --accent-secondary: #495057;
            --hover-bg: #f1f3f5;
        }}

        * {{
            margin: 0; padding: 0; box-sizing: border-box;
            font-family: 'Inter', 'Noto Sans KR', sans-serif;
        }}

        body {{
            background: var(--bg-color);
            color: var(--text-primary);
            padding: 2rem;
            min-height: 100vh;
        }}

        .container {{ max-width: 1600px; margin: 0 auto; display: flex; flex-direction: column; gap: 2rem; }}

        header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 2rem;
            background: var(--surface-color);
            border-radius: 1rem; border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}

        .logo-area h1 {{
            font-size: 2.25rem; font-weight: 800;
            color: var(--accent-primary);
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }}

        .stats-row {{
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }}

        .stat-card {{
            background: var(--surface-color); padding: 1.5rem;
            border-radius: 1rem; border: 1px solid var(--border-color);
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }}

        .stat-card:hover {{
            border-color: var(--accent-primary);
            transform: translateY(-2px);
        }}

        .stat-card .label {{ color: var(--text-secondary); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}
        .stat-card .value {{ font-size: 2.25rem; font-weight: 700; margin-top: 0.5rem; letter-spacing: -0.02em; }}

        /* Route Planning Section */
        .day-grid {{
            display: flex; gap: 0.75rem; overflow-x: auto; padding-bottom: 0.5rem;
        }}

        .day-tab {{
            background: var(--surface-color); padding: 0.75rem 1.5rem;
            border-radius: 2rem; border: 1px solid var(--border-color);
            cursor: pointer; text-align: center; transition: all 0.2s;
            flex-shrink: 0; min-width: 120px;
        }}

        .day-tab.active {{
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
        }}

        .day-tab .day-num {{ font-size: 1rem; font-weight: 700; }}
        .day-tab .day-label {{ font-size: 0.75rem; margin-top: 0.25rem; opacity: 0.8; }}
        .day-tab.active .day-label {{ color: rgba(255,255,255,0.8); }}

        /* Main Workspace */
        .workspace {{
            display: grid; grid-template-columns: 350px 1fr 300px;
            gap: 1.5rem; align-items: start;
        }}

        /* Panels */
        .panel {{
            background: var(--surface-color);
            border-radius: 1rem; border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            display: flex; flex-direction: column;
        }}

        .panel-header {{
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            font-weight: 700; font-size: 1.1rem;
            display: flex; justify-content: space-between; align-items: center;
        }}

        /* Filters & Table */
        .filters-area {{ padding: 1.5rem; border-bottom: 1px solid var(--border-color); }}
        .filter-group {{ margin-bottom: 1rem; }}
        .filter-group:last-child {{ margin-bottom: 0; }}
        .filter-group label {{ display: block; margin-bottom: 0.4rem; font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); }}
        
        input, select {{
            width: 100%; background: var(--bg-color); border: 1px solid var(--border-color);
            color: var(--text-primary); padding: 0.75rem; border-radius: 0.5rem;
            outline: none; transition: border-color 0.2s; font-size: 0.9rem;
        }}
        input:focus, select:focus {{ border-color: var(--accent-primary); }}

        .checkbox-pill {{ display: inline-block; }}
        .checkbox-pill input[type="checkbox"] {{ display: none; }}
        .checkbox-pill label {{ display: inline-block; padding: 0.25rem 0.6rem; border-radius: 1rem; border: 1px solid var(--border-color); background: var(--surface-color); cursor: pointer; font-size: 0.75rem; transition: all 0.2s ease; margin-bottom: 0; font-weight: 500; }}
        .checkbox-pill input[type="checkbox"]:checked + label {{ background: var(--accent-primary); color: white; border-color: var(--accent-primary); }}

        .leads-list {{ overflow-y: auto; height: 600px; }}
        .lead-item {{
            padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--border-color);
            cursor: pointer; transition: background 0.2s;
        }}
        .lead-item:hover {{ background: var(--hover-bg); }}
        .lead-name {{ font-weight: 700; font-size: 1.05rem; margin-bottom: 0.25rem; display: flex; justify-content: space-between; }}
        .lead-meta {{ font-size: 0.8rem; color: var(--text-secondary); display: flex; gap: 0.5rem; align-items: center; }}
        .tag {{ padding: 0.15rem 0.5rem; border-radius: 1rem; font-size: 0.7rem; font-weight: 600; background: var(--bg-color); border: 1px solid var(--border-color); }}

        /* Map */
        #map {{ height: 100%; min-height: 700px; width: 100%; z-index: 1; }}

        /* Route Planner */
        .route-list {{ padding: 1rem; overflow-y: auto; flex: 1; height: 500px; }}
        .route-item {{
            display: flex; align-items: center; gap: 1rem;
            padding: 1rem; background: var(--bg-color);
            border: 1px solid var(--border-color); border-radius: 0.5rem;
            margin-bottom: 0.75rem; position: relative;
        }}
        .route-item .seq {{
            width: 24px; height: 24px; background: var(--accent-primary); color: white;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
        }}
        .route-item .info {{ flex: 1; min-width: 0; }}
        .route-item .info h4 {{ font-size: 0.9rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .route-item .info p {{ font-size: 0.75rem; color: var(--text-secondary); }}
        .route-item .remove-btn {{ cursor: pointer; color: #dc3545; font-size: 1.2rem; font-weight: bold; background: none; border: none; padding: 0.25rem; }}

        .sales-route-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 0.5rem;
            padding: 1rem;
        }}
        .sales-route-btn {{
            background: white; border: 1px solid var(--border-color);
            padding: 0.5rem; border-radius: 0.4rem; font-size: 0.75rem;
            cursor: pointer; transition: all 0.2s; text-align: center;
            font-weight: 500;
        }}
        .sales-route-btn:hover {{ background: var(--hover-bg); }}
        .sales-route-btn.active {{ background: var(--accent-primary); color: white; border-color: var(--accent-primary); }}

        .route-actions {{ padding: 1rem; border-top: 1px solid var(--border-color); display: flex; gap: 0.5rem; }}
        .btn {{
            flex: 1; padding: 0.75rem; border-radius: 0.5rem; text-align: center;
            font-weight: 600; cursor: pointer; transition: all 0.2s; border: none; font-size: 0.9rem;
        }}
        .btn-outline {{ background: white; border: 1px solid var(--border-color); color: var(--text-primary); }}
        .btn-outline:hover {{ background: var(--hover-bg); }}
        .btn-dark {{ background: var(--accent-primary); color: white; }}
        .btn-dark:hover {{ background: #333; }}

        /* Map Popup Customization */
        .leaflet-popup-content-wrapper {{ border-radius: 0.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid var(--border-color); }}
        .leaflet-popup-content {{ margin: 1rem; font-family: 'Inter', sans-serif; }}
        .popup-title {{ font-weight: 700; font-size: 1.1rem; margin-bottom: 0.25rem; }}
        .popup-meta {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.75rem; }}
        .popup-btn {{ 
            display: block; width: 100%; padding: 0.5rem; background: var(--accent-primary); 
            color: white; text-align: center; border-radius: 0.25rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; border: none; cursor: pointer;
        }}

        /* Custom Tooltip */
        .custom-tooltip {{
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 3px 6px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-primary);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            white-space: nowrap;
            transition: opacity 0.25s ease, visibility 0.25s ease, margin 0.3s ease;
        }}
        .leaflet-tooltip-top:before {{
            border-top-color: rgba(255, 255, 255, 0.9);
        }}
        .custom-tooltip.shifted::before {{
            display: none !important;
        }}

        .hide-labels .custom-tooltip {{
            display: none !important;
        }}

        .measure-tooltip {{
            background: #ff3b30;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.75rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            padding: 2px 6px;
        }}
        .measure-tooltip::before {{
            display: none !important;
        }}

        @media (max-width: 1400px) {{
            .workspace {{ grid-template-columns: 300px 1fr; }}
            .route-panel {{ grid-column: span 2; }}
        }}
        @media (max-width: 1024px) {{
            .workspace {{ grid-template-columns: 1fr; }}
            .route-panel {{ grid-column: span 1; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-area">
                <h1>Restaurants Ops</h1>
                <p style="color: var(--text-secondary); font-weight: 500;">Restaurant Recruitment Lead Dashboard • Seoul v2.0</p>
            </div>
            <div class="time-info" style="text-align: right">
                <div id="current-time" style="font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em;"></div>
                <div id="last-sync" style="font-size: 0.8rem; color: var(--text-secondary)">Last synced: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
            </div>
        </header>

        <div class="stats-row">
            <div class="stat-card">
                <div class="label">Total Leads</div>
                <div class="value" id="stat-total">0</div>
            </div>
            <div class="stat-card">
                <div class="label">Korean (한식)</div>
                <div class="value" id="stat-korean">0</div>
            </div>
            <div class="stat-card">
                <div class="label">Japanese (일식)</div>
                <div class="value" id="stat-japanese">0</div>
            </div>
            <div class="stat-card">
                <div class="label">Top District</div>
                <div class="value" id="stat-top-gu">-</div>
            </div>
        </div>

        <section class="route-section">
            <div class="day-grid" id="day-tabs">
                <div class="day-tab active" onclick="selectDay(0)">
                    <div class="day-num">All</div>
                    <div class="day-label">Entire Seoul</div>
                </div>
                <div class="day-tab" onclick="selectDay(1)">
                    <div class="day-num">Day 1</div>
                    <div class="day-label">GN / SC / SP</div>
                </div>
                <div class="day-tab" onclick="selectDay(2)">
                    <div class="day-num">Day 2</div>
                    <div class="day-label">GS / YC / GR</div>
                </div>
                <div class="day-tab" onclick="selectDay(3)">
                    <div class="day-num">Day 3</div>
                    <div class="day-label">MP / SD / EP</div>
                </div>
                <div class="day-tab" onclick="selectDay(4)">
                    <div class="day-num">Day 4</div>
                    <div class="day-label">YD / DJ / GA</div>
                </div>
                <div class="day-tab" onclick="selectDay(5)">
                    <div class="day-num">Day 5</div>
                    <div class="day-label">JR / JG / YS</div>
                </div>
                <div class="day-tab" onclick="selectDay(6)">
                    <div class="day-num">Day 6</div>
                    <div class="day-label">SD / GJ / DD</div>
                </div>
                <div class="day-tab" onclick="selectDay(7)">
                    <div class="day-num">Day 7</div>
                    <div class="day-label">SB / GB / DB / NW</div>
                </div>
                <div class="day-tab" onclick="selectDay(8)">
                    <div class="day-num">Day 8</div>
                    <div class="day-label">JN / GD / GC</div>
                </div>
            </div>
        </section>

        <div class="workspace">
            <!-- Left Panel: Data & Filters -->
            <aside class="panel">
                <div class="panel-header">
                    <span>Target Leads</span>
                    <span id="list-count" style="font-size:0.85rem; color:var(--text-secondary); font-weight:normal;">0 items</span>
                </div>
                <div class="filters-area">
                    <div class="filter-group">
                        <input type="text" id="search-input" placeholder="Search name or keyword...">
                    </div>
                    <div class="filter-group">
                        <select id="gu-filter">
                            <option value="">All Districts</option>
                        </select>
                    </div>
                    <div class="filter-group" style="margin-top: 1rem; border-top: 1px solid var(--border-color); padding-top: 1rem;">
                        <label>Category</label>
                        <div id="cat-checkboxes" style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1rem;"></div>
                        <label>Subcategory</label>
                        <div id="subcat-checkboxes" style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1rem;"></div>
                        <label>Segment</label>
                        <div id="seg-checkboxes" style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1rem;"></div>
                        
                        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
                            <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 600; color: var(--text-primary);">
                                <input type="checkbox" id="toggle-labels" checked style="width: auto; height: auto; margin: 0;">
                                <span>지도 라벨 표시 (Show Labels)</span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="leads-list" id="leads-body">
                    <!-- Loaded via JS -->
                </div>
            </aside>

            <!-- Center Panel: Map -->
            <main class="panel" style="overflow: hidden;">
                <div id="map"></div>
            </main>

            <!-- Right Panel: Route Planner -->
            <aside class="panel route-panel">
                <div class="panel-header">
                    <span>Route Planner</span>
                    <span id="route-count" style="font-size:0.85rem; color:var(--text-secondary); font-weight:normal;">0 stops</span>
                </div>
                <div class="route-list" id="route-list">
                    <div style="text-align:center; color:var(--text-secondary); margin-top: 2rem; font-size:0.85rem;">
                        Select a marker on the map<br>to add it to your route.
                    </div>
                </div>
                <div class="route-actions">
                    <button class="btn btn-outline" onclick="clearRoute()">Clear</button>
                    <button class="btn btn-dark" onclick="exportRoute()">Export Route</button>
                </div>
                
                <div class="panel-header" style="border-top: 1px solid var(--border-color);">
                    <span>Optimized Sales Routes</span>
                </div>
                <div class="sales-route-grid" id="sales-route-list">
                    <!-- Loaded via JS -->
                </div>
                <div style="padding: 0 1rem 1rem 1rem;">
                    <button class="btn btn-outline" style="width:100%;" onclick="resetSalesRoute()">Reset Filter</button>
                </div>
            </aside>
        </div>
    </div>

    <script>
        const rawLeads = {json_data};
        let currentDay = 0;
        let selectedRoute = null;
        let map, markersLayer, routeLayer;
        let routeStops = [];
        let allMarkers = [];
        let measureMarkers = [];
        let measurePolylines = [];

        // Init Map
        function initMap() {{
            map = L.map('map').setView([37.5665, 126.9780], 11);
            
            // Modern Light/Monochrome map tiles (CartoDB Positron)
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 20
            }}).addTo(map);

            markersLayer = L.layerGroup().addTo(map);
            routeLayer = L.layerGroup().addTo(map);

            map.on('moveend', manageTooltipCollisions);
            map.on('zoomend', manageTooltipCollisions);

            // Distance Measurement Tool
            map.on('click', function(e) {{
                const latlng = e.latlng;
                
                const marker = L.circleMarker(latlng, {{
                    radius: 4,
                    color: '#ff3b30',
                    fillColor: '#ffffff',
                    fillOpacity: 1,
                    weight: 2
                }}).addTo(map);
                
                measureMarkers.push(marker);
                
                if (measureMarkers.length > 1) {{
                    const prevMarker = measureMarkers[measureMarkers.length - 2];
                    const prevLatLng = prevMarker.getLatLng();
                    const distance = prevLatLng.distanceTo(latlng);
                    
                    const line = L.polyline([prevLatLng, latlng], {{
                        color: '#ff3b30',
                        weight: 3,
                        dashArray: '5, 5'
                    }}).addTo(map);
                    
                    measurePolylines.push(line);
                    
                    let distText = distance > 1000 ? (distance/1000).toFixed(2) + ' km' : Math.round(distance) + ' m';
                    
                    line.bindTooltip(distText, {{
                        permanent: true,
                        direction: 'center',
                        className: 'measure-tooltip'
                    }}).openTooltip();
                }}
            }});

            map.on('contextmenu', function(e) {{
                measureMarkers.forEach(m => map.removeLayer(m));
                measurePolylines.forEach(l => map.removeLayer(l));
                measureMarkers = [];
                measurePolylines = [];
            }});
        }}

        // Tooltip Collision Detection & Displacement
        function manageTooltipCollisions() {{
            requestAnimationFrame(() => {{
                const tooltips = document.querySelectorAll('.custom-tooltip');
                const rects = [];
                
                const candidates = [
                    [0, 0],
                    [0, -24], [0, 26], 
                    [70, 0], [-70, 0],
                    [70, -24], [-70, -24],
                    [70, 26], [-70, 26],
                    [140, 0], [-140, 0],
                    [0, -48], [0, 52]
                ];

                tooltips.forEach(t => {{
                    t.style.opacity = '1';
                    t.style.visibility = 'visible';
                    t.style.zIndex = '';
                    t.style.marginTop = '0px';
                    t.style.marginLeft = '0px';
                }});

                // Force layout reflow once after resetting margins
                if (tooltips.length > 0) void tooltips[0].offsetHeight;

                tooltips.forEach(t => {{
                    const baseRect = t.getBoundingClientRect();
                    let placed = false;
                    
                    for (let c of candidates) {{
                        const dx = c[0];
                        const dy = c[1];
                        
                        const candidateRect = {{
                            left: baseRect.left + dx,
                            right: baseRect.right + dx,
                            top: baseRect.top + dy,
                            bottom: baseRect.bottom + dy
                        }};
                        
                        let overlap = false;
                        for (let i = 0; i < rects.length; i++) {{
                            const r = rects[i];
                            if (!(candidateRect.right + 2 < r.left || 
                                  candidateRect.left - 2 > r.right || 
                                  candidateRect.bottom + 2 < r.top || 
                                  candidateRect.top - 2 > r.bottom)) {{
                                overlap = true;
                                break;
                            }}
                        }}
                        
                        if (!overlap) {{
                            if (dx !== 0 || dy !== 0) {{
                                t.style.marginLeft = dx + 'px';
                                t.style.marginTop = dy + 'px';
                                t.classList.add('shifted');
                            }} else {{
                                t.classList.remove('shifted');
                            }}
                            rects.push(candidateRect);
                            placed = true;
                            break;
                        }}
                    }}
                    
                    if (!placed) {{
                        t.style.opacity = '0';
                        t.style.visibility = 'hidden';
                        t.classList.remove('shifted');
                    }}
                }});
            }});
        }}

        // Custom Map Icon
        const createIcon = (color) => L.divIcon({{
            className: 'custom-icon',
            html: `<div style="background-color: ${{color}}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.4);"></div>`,
            iconSize: [16, 16],
            iconAnchor: [8, 8]
        }});
        
        const iconNormal = createIcon('#343a40');
        const iconSelected = createIcon('#ff3b30');

        // Init Gu List
        const guList = [...new Set(rawLeads.map(l => l.gu))].sort();
        const guSelect = document.getElementById('gu-filter');
        guList.forEach(gu => {{
            const opt = document.createElement('option');
            opt.value = gu; opt.textContent = gu;
            guSelect.appendChild(opt);
        }});

        // Init Checkboxes
        const categories = [...new Set(rawLeads.map(l => l.category).filter(Boolean))].sort();
        const subcategories = [...new Set(rawLeads.map(l => l.subcategory).filter(Boolean))].sort();
        const segments = [...new Set(rawLeads.map(l => l.segment).filter(Boolean))].sort();

        function createCheckboxes(items, containerId, prefix) {{
            const container = document.getElementById(containerId);
            items.forEach((item, idx) => {{
                const id = `${{prefix}}-${{idx}}`;
                const div = document.createElement('div');
                div.className = 'checkbox-pill';
                div.innerHTML = `
                    <input type="checkbox" id="${{id}}" value="${{item}}" onchange="renderLeads()">
                    <label for="${{id}}">${{item}}</label>
                `;
                container.appendChild(div);
            }});
        }}
        createCheckboxes(categories, 'cat-checkboxes', 'cat');
        createCheckboxes(subcategories, 'subcat-checkboxes', 'subcat');
        createCheckboxes(segments, 'seg-checkboxes', 'seg');

        function getCheckedValues(containerId) {{
            const checked = document.querySelectorAll(`#${{containerId}} input:checked`);
            return Array.from(checked).map(cb => cb.value);
        }}

        function renderLeads() {{
            const search = document.getElementById('search-input').value.toLowerCase();
            const gu = document.getElementById('gu-filter').value;
            
            const checkedCats = getCheckedValues('cat-checkboxes');
            const checkedSubcats = getCheckedValues('subcat-checkboxes');
            const checkedSegs = getCheckedValues('seg-checkboxes');
            
            const filtered = rawLeads.filter(l => {{
                const matchesDay = currentDay === 0 || l.day === currentDay;
                const matchesSearch = l.name.toLowerCase().includes(search) || (l.keyword && l.keyword.toLowerCase().includes(search));
                const matchesGu = !gu || l.gu === gu;
                const matchesCat = checkedCats.length === 0 || checkedCats.includes(l.category);
                const matchesSubcat = checkedSubcats.length === 0 || checkedSubcats.includes(l.subcategory);
                const matchesSeg = checkedSegs.length === 0 || checkedSegs.includes(l.segment);
                const matchesRoute = !selectedRoute || l.sales_route === selectedRoute;
                
                return matchesDay && matchesSearch && matchesGu && matchesCat && matchesSubcat && matchesSeg && matchesRoute;
            }});

            const tbody = document.getElementById('leads-body');
            tbody.innerHTML = '';
            markersLayer.clearLayers();
            allMarkers = [];
            
            let bounds = L.latLngBounds();

            filtered.forEach((l, index) => {{
                // Render List
                const div = document.createElement('div');
                div.className = 'lead-item';
                div.innerHTML = `
                    <div class="lead-name">
                        <span>${{l.name}}</span>
                        <span class="tag">${{l.category}}</span>
                    </div>
                    <div class="lead-meta">
                        <span>${{l.gu}}</span> • <span>${{l.subcategory || '-'}}</span>
                    </div>
                    <div class="lead-meta" style="margin-top:0.35rem; gap:0.5rem;">
                        <span class="tag" style="background:#e9ecef; color:#333; font-size:0.65rem;">${{l.segment}}</span>
                        <span style="font-size:0.75rem; color:#aaa;">${{l.phone || 'No phone'}}</span>
                    </div>
                `;
                div.onclick = () => focusMap(l.lat, l.lng, index);
                tbody.appendChild(div);

                // Render Map Marker
                if(l.lat && l.lng) {{
                    const isSelected = routeStops.some(s => s.place_id === l.place_id);
                    const tooltipText = `[${{l.segment.split('.')[0]}}] ${{l.category}}, ${{l.subcategory || '-'}}, ${{l.name}}`;
                    const marker = L.marker([l.lat, l.lng], {{
                        icon: isSelected ? iconSelected : iconNormal,
                        place_id: l.place_id
                    }}).bindTooltip(tooltipText, {{
                        permanent: true,
                        direction: 'top',
                        className: 'custom-tooltip',
                        offset: [0, -8]
                    }}).bindPopup(`
                        <div class="popup-title">${{l.name}}</div>
                        <div class="popup-meta" style="font-weight:bold; color:var(--accent-primary);">${{l.segment}}</div>
                        <div class="popup-meta">${{l.address}}</div>
                        <div class="popup-meta">📞 ${{l.phone || '-'}}</div>
                        <button class="popup-btn" onclick="addToRoute('${{l.place_id}}')">Add to Route</button>
                    `);
                    
                    marker.on('mouseover', function() {{
                        const t = marker.getTooltip();
                        if (t && t._container) {{
                            t._container.style.opacity = '1';
                            t._container.style.visibility = 'visible';
                            t._container.style.zIndex = '9999';
                        }}
                    }});
                    marker.on('mouseout', function() {{
                        const t = marker.getTooltip();
                        if (t && t._container) {{
                            t._container.style.zIndex = '';
                        }}
                        setTimeout(manageTooltipCollisions, 50);
                    }});
                    
                    marker.addTo(markersLayer);
                    allMarkers.push({{data: l, marker: marker}});
                    bounds.extend([l.lat, l.lng]);
                }}
            }});

            document.getElementById('list-count').textContent = `${{filtered.length}} items`;
            updateStats(filtered);

            if(filtered.length > 0 && bounds.isValid()) {{
                map.fitBounds(bounds, {{padding: [50, 50]}});
            }}
            setTimeout(manageTooltipCollisions, 300);
        }}

        function focusMap(lat, lng, index) {{
            if(lat && lng) {{
                map.setView([lat, lng], 16);
                allMarkers[index].marker.openPopup();
            }}
        }}

        function updateStats(data) {{
            document.getElementById('stat-total').textContent = data.length;
            document.getElementById('stat-korean').textContent = data.filter(i => i.category === '한식').length;
            document.getElementById('stat-japanese').textContent = data.filter(i => i.category === '일식').length;
            
            const counts = {{}};
            data.forEach(i => {{ counts[i.gu] = (counts[i.gu] || 0) + 1; }});
            const top = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b, '-');
            document.getElementById('stat-top-gu').textContent = top;
        }}

        function selectDay(day) {{
            currentDay = day;
            document.querySelectorAll('.day-tab').forEach((el, idx) => {{
                el.classList.toggle('active', idx === day);
            }});
            renderLeads();
        }}

        // Route Planning
        window.addToRoute = function(placeId) {{
            if(routeStops.some(s => s.place_id === placeId)) return; // Already in route
            
            const place = rawLeads.find(l => l.place_id === placeId || l.place_id == placeId);
            if(place) {{
                routeStops.push(place);
                renderRoute();
                renderLeads(); // Update marker colors
            }}
        }};

        window.removeFromRoute = function(index) {{
            routeStops.splice(index, 1);
            renderRoute();
            renderLeads();
        }};

        window.clearRoute = function() {{
            routeStops = [];
            renderRoute();
            renderLeads();
        }};

        function renderRoute() {{
            const list = document.getElementById('route-list');
            document.getElementById('route-count').textContent = `${{routeStops.length}} stops`;
            
            if(routeStops.length === 0) {{
                list.innerHTML = `<div style="text-align:center; color:var(--text-secondary); margin-top: 2rem; font-size:0.85rem;">Select a marker on the map<br>to add it to your route.</div>`;
                routeLayer.clearLayers();
                return;
            }}

            list.innerHTML = '';
            const latlngs = [];

            routeStops.forEach((stop, idx) => {{
                const div = document.createElement('div');
                div.className = 'route-item';
                div.innerHTML = `
                    <div class="seq">${{idx + 1}}</div>
                    <div class="info">
                        <h4>${{stop.name}}</h4>
                        <p>${{stop.gu}}</p>
                    </div>
                    <button class="remove-btn" onclick="removeFromRoute(${{idx}})">&times;</button>
                `;
                list.appendChild(div);

                if(stop.lat && stop.lng) {{
                    latlngs.push([stop.lat, stop.lng]);
                }}
            }});

            // Draw line on map
            routeLayer.clearLayers();
            if(latlngs.length > 1) {{
                L.polyline(latlngs, {{color: '#000', weight: 3, dashArray: '5, 10', lineCap: 'round'}}).addTo(routeLayer);
            }}
        }}

        window.exportRoute = function() {{
            if(routeStops.length === 0) {{
                alert('No stops in route.');
                return;
            }}
            let text = "Restaurants Recruitment Route:\\n\\n";
            routeStops.forEach((s, idx) => {{
                text += `${{idx + 1}}. ${{s.name}} (${{s.address}} / ${{s.phone || '-'}})\\n`;
            }});
            navigator.clipboard.writeText(text).then(() => alert('Route copied to clipboard!'));
        }}

        window.resetSalesRoute = function() {{
            selectedRoute = null;
            document.querySelectorAll('.sales-route-btn').forEach(b => b.classList.remove('active'));
            renderLeads();
        }}

        function initSalesRoutes() {{
            const list = document.getElementById('sales-route-list');
            const routeNames = {json.dumps(route_list_names)};
            routeNames.forEach(name => {{
                const btn = document.createElement('div');
                btn.className = 'sales-route-btn';
                btn.textContent = name;
                btn.onclick = () => {{
                    if (selectedRoute === name) {{
                        selectedRoute = null;
                        btn.classList.remove('active');
                    }} else {{
                        document.querySelectorAll('.sales-route-btn').forEach(b => b.classList.remove('active'));
                        selectedRoute = name;
                        btn.classList.add('active');
                    }}
                    renderLeads();
                }};
                list.appendChild(btn);
            }});
        }}

        // Event Listeners
        document.getElementById('search-input').oninput = renderLeads;
        document.getElementById('gu-filter').onchange = renderLeads;
        document.getElementById('toggle-labels').onchange = function() {{
            const mapEl = document.getElementById('map');
            if(this.checked) {{
                mapEl.classList.remove('hide-labels');
            }} else {{
                mapEl.classList.add('hide-labels');
            }}
        }};

        // Clock
        setInterval(() => {{
            document.getElementById('current-time').textContent = new Date().toLocaleTimeString('en-US', {{ hour12: false }});
        }}, 1000);

        // Init
        window.onload = () => {{
            initMap();
            initSalesRoutes();
            renderLeads();
        }};
    </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated {html_path} with {len(data)} records.")
