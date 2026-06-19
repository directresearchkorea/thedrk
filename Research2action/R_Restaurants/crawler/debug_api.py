import urllib.request
import json

place_id = "11592643"
url = f"https://map.naver.com/p/api/place/summary/{place_id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("Name:", data.get("name"))
        print("Address:", data.get("address"))
        print("Phone:", data.get("phone"))
        print("Hours:", data.get("bizHour", {}).get("info"))
        print("Days:", data.get("bizHour", {}).get("bizHours"))
except Exception as e:
    print(f"Error fetching: {e}")

# If v5 summary API works
url2 = f"https://map.naver.com/v5/api/sites/summary/{place_id}"
req2 = urllib.request.Request(url2, headers=headers)
try:
    with urllib.request.urlopen(req2) as response:
        data = json.loads(response.read().decode())
        print("V5 Name:", data.get("name"))
        print("V5 Address:", data.get("address"))
        print("V5 Phone:", data.get("phone"))
        print("V5 Hours:", data.get("bizhourInfo"))
except Exception as e:
    print(f"V5 Error fetching: {e}")
