from .base import ScraperBase
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

class ExpediaScraper(ScraperBase):
    name = "expedia"

    async def search(self, profile):
        dest = profile.get("travel_constraints", {}).get("destination_candidates", [""])[0]
        dates = profile.get("travel_constraints", {}).get("dates", {})
        depart = dates.get("depart", "")
        ret = dates.get("return", "")
        url = (
            f"https://www.expedia.co.uk/Hotel-Search?"
            f"destination={dest}&startDate={depart}&endDate={ret}&adults=1"
        )

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            # Wait for the property list or fallback to body
            try:
                await page.wait_for_selector("section[data-stid='property-list-results']", timeout=20000)
            except:
                pass
            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "lxml")
        results = []
        # Limit to first few entries to keep responses small in tests
        for card in soup.select("section[data-stid='property-list-results'] article")[:8]:
            name = card.select_one("h3")
            price = card.select_one("span[data-stid='content-hotel-lead-price']")
            link = card.select_one("a")
            if not (name and price):
                continue
            price_text = re.sub(r"[^\d.]", "", price.get_text())
            try:
                price_val = float(price_text)
            except:
                continue
            results.append({
                "type": "hotel",
                "provider": "Expedia",
                "price_gbp": price_val,
                "components": {"hotel": {"name": name.get_text(strip=True), "link": ("https://www.expedia.co.uk" + link.get("href") if link else None)}}
            })
        return results
