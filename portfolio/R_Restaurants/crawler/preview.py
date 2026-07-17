import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

async def fetch_details(browser, item):
    place_id = item.get("place_id")
    url = f"https://pcmap.place.naver.com/restaurant/{place_id}/home"
    context = await browser.new_context()
    page = await context.new_page()
    try:
        await page.goto(url)
        await page.wait_for_timeout(2000)
        
        try:
            expand_btn = await page.query_selector('a.gKP9i')
            if expand_btn:
                await expand_btn.click()
                await page.wait_for_timeout(500)
        except:
            pass

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        
        address = ""
        phone = ""
        hours = ""
        
        texts = [s.strip() for s in soup.strings if s.strip()]
        for t in texts:
            if not address and "서울" in t and ("구" in t or "동" in t):
                address = t
            if not phone and ("02-" in t or "0507-" in t or "010-" in t):
                phone = t
                
        hours_list = []
        capture = False
        for t in texts:
            if t == "영업시간":
                capture = True
                continue
            if capture:
                if t in ["접기", "전화번호", "홈페이지", "설명", "편의"]:
                    break
                hours_list.append(t)
        if hours_list:
            hours = " ".join(hours_list[:10])

        item["address"] = address
        item["phone"] = phone
        item["hours"] = hours
    except Exception as e:
        pass
    finally:
        await context.close()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        keyword = "강남구 돈카츠 배달 맛집"
        await page.goto(f"https://search.naver.com/search.naver?query={keyword}")
        await page.wait_for_timeout(3000)
        
        elements = await page.query_selector_all('li[data-laim-exp-id="nmb_res"]')
        items = []
        for el in elements[:5]:
            place_id = await el.get_attribute("data-nmb_res-doc-id")
            html = await el.evaluate("el => el.innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            texts = [s.strip() for s in soup.strings if s.strip()]
            if texts and place_id:
                items.append({"place_id": place_id, "name": texts[0], "category": "일식", "subcategory": "돈카츠", "keyword": keyword})
        
        for item in items:
            await fetch_details(browser, item)
            
        with open("data/preview.json", "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
