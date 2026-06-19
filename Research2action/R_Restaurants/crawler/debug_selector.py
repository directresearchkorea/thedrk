import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Naver search URL
        url = "https://search.naver.com/search.naver?query=돈카츠 배달 맛집 서울"
        await page.goto(url)
        await page.wait_for_timeout(3000)
        
        elements = await page.query_selector_all('li[data-laim-exp-id="nmb_res"]')
        print(f"Found {len(elements)} items")
        if elements:
            html = await elements[0].evaluate("el => el.innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            print(soup.prettify())
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
