import asyncio
from playwright.async_api import async_playwright

async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://search.naver.com/search.naver?query=돈카츠 배달 맛집 서울")
        await page.wait_for_selector(".place_section")
        
        html = await page.content()
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug())
