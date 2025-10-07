from .base import ScraperBase
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

class AutoTraderScraper(ScraperBase):
    name = "autotrader"

    async def search(self, profile):
        budget = profile.get("preferences", {}).get("max_car_price", 20000)
        url = f"https://www.autotrader.co.uk/car-search?price-to={int(budget)}&sort=relevance"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            try:
                await page.wait_for_selector("li.search-page__result", timeout=20000)
            except:
                pass
            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "lxml")
        results = []
        for card in soup.select("li.search-page__result")[:8]:
            name = card.select_one("h3")
            price = card.select_one("div.vehicle-price")
            link = card.select_one("a.js-click-handler")
            if not (name and price):
                continue
            price_text = re.sub(r"[^\d.]", "", price.get_text())
            try:
                price_val = float(price_text)
            except:
                continue
            results.append({
                "type": "car_sale",
                "provider": "AutoTrader",
                "price_gbp": price_val,
                "components": {"car": {"name": name.get_text(strip=True), "link": ("https://www.autotrader.co.uk" + link.get("href") if link else None)}}
            })
        return results
