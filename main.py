from scrapers.schedule_anime_scraper import scrape_scheduled_animes
from tools.validateNumber import is_valid_integer
from subprocess import call
from scrapers.seasonal_anime_scraper import scrape_seasonal_animes
from scrapers.characters_scraper import scrape_characters
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from browser_setup import get_browser_context
from scrapers.top_animes_scraper import scrape_top_animes
import json
from pathlib import Path
import asyncio
import sys


def save_to_json(data, filename):
    file_path = Path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


async def run():
    async with async_playwright() as playwright:
        page = await get_browser_context(playwright)

        # Apply stealth to the page
        stealth = Stealth()
        await stealth.apply_stealth_async(page)

        tasks = [
            ("output_json/top_animes/top_animes.json", "", "scrape_top_animes"),
            (
                "output_json/top_animes/top_airing_animes.json",
                "airing",
                "scrape_top_animes",
            ),
            (
                "output_json/top_animes/top_upcoming_animes.json",
                "upcoming",
                "scrape_top_animes",
            ),
            ("output_json/top_animes/top_tv_animes.json", "tv", "scrape_top_animes"),
            (
                "output_json/top_animes/top_movie_animes.json",
                "movie",
                "scrape_top_animes",
            ),
            (
                "output_json/recommended_animes/recommended_animes.json",
                "recommended",
                "scrape_recommended_animes",
            ),
            (
                "output_json/seasonal_animes/seasonal_animes.json",
                "seasonal",
                "scrape_seasonal_animes",
            ),
            (
                "output_json/scheduled_animes/scheduled_animes.json",
                "schedule",
                "scrape_scheduled_animes",
            ),
            (
                "output_json/characters/characters.json",
                "characters",
                "scrape_characters",
            ),
        ]
        func_name = sys.argv[1]
        for filename, type, function in tasks:
            if func_name == function:
                if func_name == "scrape_top_animes":
                    print(f"Scraping {type if type else 'top anime'} animes...")
                    pageLimit = sys.argv[2]
                    if not is_valid_integer(pageLimit):
                        print("Invalid page limit, returning...")
                        return
                    data = await scrape_top_animes(page, type, int(pageLimit))
                    save_to_json(data, filename)
                    print(f"Done scraped {type} animes...")

                elif func_name == "scrape_recommended_animes":
                    print(f"Scraping {type} animes...")

                elif func_name == "scrape_scheduled_animes":
                    print(f"Scraping {type} animes...")
                    data = await scrape_scheduled_animes(page, type)
                    save_to_json(data, filename)
                    print(f"Done scraped {type} animes...")

                elif func_name == "scrape_seasonal_animes":
                    print(f"Scraping {type} animes...")
                    year = sys.argv[2]
                    if not is_valid_integer(year):
                        print("Invalid year, returning...")
                        return
                    data = await scrape_seasonal_animes(page, year)
                    save_to_json(data, filename)
                    print(f"Done scraped {type} animes...")
                elif func_name == "scrape_characters":
                    print(f"Scraping anime/manga charactes")
                    pageLimit = sys.argv[2]
                    if not is_valid_integer(pageLimit):
                        print("Invalid page limit, returning...")
                        return
                    data = await scrape_characters(page, int(pageLimit))
                    save_to_json(data, filename)
                    print(f"Done scraped characters")
        # await page.pause()


async def main():
    await run()


if __name__ == "__main__":
    asyncio.run(main())
