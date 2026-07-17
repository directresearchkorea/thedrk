import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def run():
    place_id = "11592643"
    url = f"https://pcmap.place.naver.com/restaurant/{place_id}/home"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(2000)
        
        # Click on the "영업시간 더보기" button if it exists to expand hours
        try:
            expand_btn = await page.query_selector('a.gKP9i') # The expand arrow or similar, we might need a generic click
            if expand_btn:
                await expand_btn.click()
                await page.wait_for_timeout(500)
        except:
            pass
            
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        
        # Find all text to see what classes are mapped to address, phone, hours
        # Address is usually in span.LDgIH
        address_el = soup.select_one('span.LDgIH')
        address = address_el.text if address_el else ""
        
        # Phone is usually in span.xlx7Q
        phone_el = soup.select_one('span.xlx7Q')
        phone = phone_el.text if phone_el else ""
        
        # Hours is usually in div.U7pYf or span.A_cdD
        # Let's just find everything with text "영업시간" or "휴무"
        texts = [s.strip() for s in soup.strings if s.strip()]
        
        print("Address:", address)
        print("Phone:", phone)
        print("Texts around hours/holidays:")
        for i, t in enumerate(texts):
            if "영업" in t or "휴" in t or ":" in t:
                print(f"[{i}] {t}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
