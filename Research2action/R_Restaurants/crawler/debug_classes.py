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
        for i, el in enumerate(elements):
            html = await el.evaluate("el => el.innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            
            # Find the title (usually the largest text or specifically classed)
            # Let's find all text elements and their classes
            texts = [(tag.name, tag.get('class'), tag.text.strip()) for tag in soup.find_all(string=False) if tag.text.strip() and not tag.find_all(recursive=False)]
            # We want to identify name, address, phone.
            print(f"Item {i+1}:")
            for t in texts:
                print(f"  {t}")
            print("-" * 40)
            if i > 2:
                break
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
