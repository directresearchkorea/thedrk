import asyncio
import json
import logging
import os
import csv
import re
import random
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Setup logging
log_dir = Path(__file__).resolve().parents[1] / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_dir / "crawl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Load keyword mapping
keywords_path = Path(__file__).resolve().parents[1] / "crawler" / "keywords.json"
with open(keywords_path, "r", encoding="utf-8") as f:
    keyword_data = json.load(f)

async def fetch_naver(keyword: str):
    return f"https://search.naver.com/search.naver?query={keyword}"

async def parse_page(page):
    try:
        await page.wait_for_selector('li[data-laim-exp-id="nmb_res"]', timeout=3000)
    except Exception:
        return []

    items = await page.query_selector_all('li[data-laim-exp-id="nmb_res"]')
    results = []
    for item in items:
        try:
            place_id = await item.get_attribute("data-nmb_res-doc-id")
            name_el = await item.query_selector('span.TYC97') # Common name class
            name = await name_el.inner_text() if name_el else ""
            if not name:
                # Fallback text extraction
                name = await item.evaluate('el => el.innerText.split("\\n")[0]')
            
            if place_id:
                results.append({"place_id": place_id, "name": name.strip()})
        except Exception:
            continue
    return results

async def scroll_to_bottom(page, max_pages: int = 2):
    for _ in range(max_pages):
        await page.evaluate("window.scrollBy(0, 1000)")
        await asyncio.sleep(1)

async def crawl_category(browser, category, subcategory, keyword):
    context = await browser.new_context()
    page = await context.new_page()
    try:
        search_url = await fetch_naver(keyword)
        await page.goto(search_url, wait_until="domcontentloaded")
        await scroll_to_bottom(page)
        items = await parse_page(page)
        for item in items:
            item["category"] = category
            item["subcategory"] = subcategory
            item["keyword"] = keyword
        return items
    finally:
        await context.close()

async def fetch_details(browser, item, semaphore):
    async with semaphore:
        place_id = item.get("place_id")
        url = f"https://pcmap.place.naver.com/restaurant/{place_id}/home"
        context = await browser.new_context()
        page = await context.new_page()
        try:
            # Add a common User-Agent to look like a real user
            await context.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
            
            # Stealth: Small random delay before starting
            await asyncio.sleep(random.uniform(1.0, 3.0))
            
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Wait for content
            try:
                await page.wait_for_selector('text="주소"', timeout=10000)
            except:
                pass
            
            await page.wait_for_timeout(random.uniform(500, 1500))
            
            full_text = await page.inner_text("body")
            
            # 1. JSON-LD Fallback
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")
            ld_json = soup.find("script", type="application/ld+json")
            if ld_json:
                try:
                    data = json.loads(ld_json.string)
                    meta = next((obj for obj in data if obj.get("@type") == "Restaurant"), data[0] if data else {}) if isinstance(data, list) else data
                    if isinstance(meta, dict):
                        item["address"] = meta.get("address", {}).get("streetAddress", item.get("address", ""))
                        item["phone"] = meta.get("telephone", item.get("phone", ""))
                except: pass

            # 2. Precision Extraction (Label-based)
            if not item.get("address") or item.get("address") == "N/A":
                addr_match = re.search(r"주소\s*\n?\s*(서울.*)", full_text)
                if addr_match:
                    item["address"] = addr_match.group(1).split("\n")[0].strip()
            
            if not item.get("phone") or item.get("phone") == "N/A":
                phone_match = re.search(r"전화번호\s*\n?\s*(\d{2,4}-\d{3,4}-\d{4})", full_text)
                if phone_match:
                    item["phone"] = phone_match.group(1).strip()
                else:
                    gen_phone = re.search(r"(\d{2,4}-\d{3,4}-\d{4})", full_text)
                    if gen_phone: item["phone"] = gen_phone.group(1).strip()

            if not item.get("hours") or item.get("hours") == "N/A":
                hours_match = re.search(r"영업시간\s*\n?(.*?)(?:\n\n|\n[가-힣]{2,} :|정보수정|전화번호|$)", full_text, re.S)
                if hours_match: item["hours"] = hours_match.group(1).replace("\n", " ").strip()[:150]

            logging.info(f"Details for {item['name']}: {item.get('address', 'N/A')[:30]} | {item.get('phone', 'N/A')}")
        except Exception as e:
            logging.error(f"Error fetching details for {place_id}: {e}")
        finally:
            await context.close()

async def main():
    all_results = []
    csv_path = Path(__file__).resolve().parents[1] / "data" / "restaurants_new.csv"
    
    # Check if we should resume from existing CSV
    existing_records = []
    if csv_path.exists():
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                existing_records = list(reader)
            logging.info(f"Found existing CSV with {len(existing_records)} records.")
        except Exception as e:
            logging.error(f"Error reading existing CSV: {e}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Determine items to process
        items_to_fetch = []
        
        if existing_records:
            # Mode: Resume and fill missing data
            logging.info("Resuming: Filling missing addresses for existing records...")
            for rec in existing_records:
                if not rec.get("address") or rec.get("address") == "N/A":
                    items_to_fetch.append(rec)
            unique_records = existing_records
        else:
            # Mode: Full Crawl
            for cat in keyword_data.get("categories", []):
                cat_name = cat.get("name")
                for sub in cat.get("subcategories", []):
                    sub_name = sub.get("name")
                    for kw in sub.get("keywords", []):
                        logging.info(f"Crawling: {cat_name} / {sub_name} / {kw}")
                        try:
                            res = await crawl_category(browser, cat_name, sub_name, kw)
                            all_results.extend(res)
                        except Exception as e:
                            logging.error(f"Error crawling {kw}: {e}")

            seen = set()
            # Pre-populate seen list with existing database to prevent wasted API hits on duplicates
            final_db_path = Path(__file__).resolve().parents[1] / "data" / "restaurants_final.csv"
            if final_db_path.exists():
                try:
                    with open(final_db_path, "r", encoding="utf-8-sig") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            seen.add(row.get("place_id"))
                    logging.info(f"Pre-seeded 'seen' tracking with {len(seen)} existing places to bypass.")
                except Exception as e:
                    logging.error(f"Failed to load existing seeds: {e}")

            unique_records = []
            for r in all_results:
                if r["place_id"] not in seen:
                    seen.add(r["place_id"])
                    unique_records.append(r)
            
            if len(unique_records) > 1000:
                unique_records = unique_records[:1000]
            items_to_fetch = unique_records

        logging.info(f"Items to fetch details for: {len(items_to_fetch)}")
        
        # Step 2: Fetch details with concurrency (Chunked for periodic save)
        if items_to_fetch:
            chunk_size = 50
            for i in range(0, len(items_to_fetch), chunk_size):
                chunk = items_to_fetch[i : i + chunk_size]
                chunk_index = i // chunk_size + 48
                logging.info(f"Processing chunk {chunk_index} ({len(chunk)} items)...")
                
                semaphore = asyncio.Semaphore(1)
                await asyncio.gather(*[fetch_details(browser, rec, semaphore) for rec in chunk])
                
                # Save Chunk to a separate file
                chunk_csv_path = csv_path.with_name(f"restaurants_{chunk_index}.csv")
                save_csv(chunk_csv_path, chunk)
                logging.info(f"Chunk Save: Chunk {chunk_index} saved to {chunk_csv_path}")

        await browser.close()

def save_csv(csv_path, records):
    data_dir = csv_path.parent
    data_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = ["place_id", "category", "subcategory", "keyword", "name", "address", "phone", "hours"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    asyncio.run(main())
