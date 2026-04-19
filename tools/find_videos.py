import asyncio
from playwright.async_api import async_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.thedrk.com/post/feelings-in-focus-how-drk-turns-emotion-videography-into-2025-s-research-edge', wait_until='networkidle')
        
        videos = await page.evaluate('''() => {
            let iframes = Array.from(document.querySelectorAll('iframe'));
            let videoTags = Array.from(document.querySelectorAll('video'));
            let wixVideos = Array.from(document.querySelectorAll('wix-video'));
            let links = Array.from(document.querySelectorAll('a')).map(a => a.href).filter(href => href.includes('youtu'));
            
            return {
                iframes: iframes.map(f => f.src),
                videos: videoTags.map(v => v.src),
                wixVideos: wixVideos.length,
                links: links
            };
        }''')
        
        print("Videos found:")
        print(videos)
        
        await browser.close()

asyncio.run(main())
