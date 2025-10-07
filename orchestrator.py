import asyncio
from scrapers.expedia import ExpediaScraper
from scrapers.booking import BookingScraper
from scrapers.autotrader import AutoTraderScraper
from app.scoring import score_deal

SCRAPERS = [ExpediaScraper(), BookingScraper(), AutoTraderScraper()]

async def run_all_scrapers(profile):
    tasks = [scraper.search(profile) for scraper in SCRAPERS]
    nested = await asyncio.gather(*tasks, return_exceptions=False)
    all_deals = [d for lst in nested for d in lst]
    scored = [score_deal(profile, d) for d in all_deals]
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)
    return scored[:20]
