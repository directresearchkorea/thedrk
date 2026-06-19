import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Naver search URL
        url = "https://search.naver.com/search.naver?query=돈카츠 배달 맛집 서울"
        await page.goto(url)
        await page.wait_for_timeout(3000)
        
        elements = await page.query_selector_all('li[data-laim-exp-id="nmb_res"]')
        results = []
        for el in elements:
            html = await el.evaluate("el => el.innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            
            # Find the first 'a' tag which usually contains the title
            a_tag = soup.find('a')
            if a_tag:
                # The text inside the a_tag without children is often the title
                texts = [s.strip() for s in a_tag.strings if s.strip()]
                name = texts[0] if texts else "Unknown"
                results.append({"name": name, "all_texts": texts})
                
        with open("debug_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
