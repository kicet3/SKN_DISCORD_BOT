from playwright.async_api import async_playwright
import re
import asyncio

async def get_img(lunch_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(lunch_url)
        
        try:
            # .wrap_webview 요소가 나타날 때까지 최대 10초 대기
            await page.wait_for_selector('.wrap_webview', timeout=30000)
            # .wrap_fit_thumb 요소들을 모두 선택
            post_items = await page.query_selector_all('.wrap_fit_thumb')
            img_urls = []
            for div in post_items:
                style = await div.get_attribute("style")
                match = re.search(r'url\(["\']?(.*?)["\']?\)', style)
                if match:
                    img_urls.append(match.group(1))
            return img_urls[0] if img_urls else None
        except Exception as e:
            print(e)
        finally:
            await browser.close()

