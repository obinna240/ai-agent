from .base import ScraperBase
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import urllib.parse

class BookingScraper(ScraperBase):
    name = "booking"

    async def search(self, profile):
        dest = profile.get("travel_constraints", {}).get("destination_candidates", [""])[0]
        dates = profile.get("travel_constraints", {}).get("dates", {})
        depart = dates.get("depart", "")
        ret = dates.get("return", "")
        # booking uses ss param for destination; URL encode
        url = (
            f"https://www.booking.com/searchresults.html?"
            f"ss={urllib.parse.quote(dest)}&checkin={depart}&checkout={ret}&group_adults=1"
        )

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            try:
                await page.wait_for_selector("div[data-testid='property-card']", timeout=20000)
            except:
                pass
            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "lxml")
        results = []
        for card in soup.select("div[data-testid='property-card']")[:8]:
            name = card.select_one("div[data-testid='title']")
            price = card.select_one("span[data-testid='price-and-discounted-price']")
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
                "provider": "Booking.com",
                "price_gbp": price_val,
                "components": {"hotel": {"name": name.get_text(strip=True), "link": ("https://www.booking.com" + link.get("href") if link else None)}}
            })
        return results
