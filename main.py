from scrapers.seasonal_anime_scraper import scrape_seasonal_animes
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from browser_setup import get_browser_context
from scrapers.top_animes_scraper import scrape_top_animes
import json
from pathlib import Path
import asyncio

def save_to_json(data, filename):
    file_path = Path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

async def run():
    async with async_playwright() as playwright:
        page = await get_browser_context(playwright)
        
        # Apply stealth to the page
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        tasks = [
            ('output_json/top_animes/top_animes.json', '', 'scrape_top_animes'),
            ('output_json/top_animes/top_airing_animes.json', 'airing', 'scrape_top_animes'),
            ('output_json/top_animes/top_upcoming_animes.json', 'upcoming', 'scrape_top_animes'),
            ('output_json/top_animes/top_tv_animes.json', 'tv', 'scrape_top_animes'),
            ('output_json/top_animes/top_movie_animes.json', 'movie', 'scrape_top_animes'),
            
            ('output_json/recommended_animes/recommended_animes.json', 'recommended', 'scrape_recommended_animes'),
            
            ('output_json/seasonal_animes/seasonal_animes.json', 'seasonal', 'scrape_seasonal_animes'),
        ]
        
        for filename, type, function in tasks:
            match function:
                case 'scrape_top_animes':
                    print(f'Scraping {type} animes...')
                    data = await scrape_top_animes(page, type)
                    save_to_json(data, filename)
                    print(f'Done scraped {type} animes...')
                case 'scrape_recommended_animes':
                    print(f'Scraping {type} animes...')
                case 'scrape_seasonal_animes':
                    print(f'Scraping {type} animes...')
                    data = await scrape_seasonal_animes(page, type)
                    save_to_json(data, filename)
                    print(f'Done scraped {type} animes...')

async def main():
    await run()


if __name__ == "__main__":
    asyncio.run(main())