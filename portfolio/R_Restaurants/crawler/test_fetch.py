import asyncio
from playwright.async_api import async_playwright
import re

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = "https://pcmap.place.naver.com/restaurant/1034438046/home"
        print(f"Fetching {url}...")
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        text = await page.inner_text("body")
        
        # Save to file with UTF-8
        with open("page_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        print("Text saved to page_text.txt")
        
        # Try to find address pattern
        # Pattern: 서울 ... (구) ... (동) ...
        match = re.search(r"(서울\s+[가-힣]+구\s+[가-힣0-9\s-]+)", text)
        if match:
            print(f"Found Address: {match.group(1)}")
        else:
            print("Address pattern NOT found")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())
