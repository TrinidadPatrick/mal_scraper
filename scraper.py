from playwright.sync_api import sync_playwright
from browser_setup import get_browser_context
from scrapers.top_animes_scraper import scrape_top_animes
import json
from pathlib import Path

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def run():
    with sync_playwright() as playwright:
        page =  get_browser_context(playwright)
        
        tasks = [
            ('output_json/top_animes/top_animes.json', ''),
            ('output_json/top_animes/top_airing_animes.json', 'airing'),
            ('output_json/top_animes/top_upcoming_animes.json', 'upcoming'),
            ('output_json/top_animes/top_tv_animes.json', 'tv'),
            ('output_json/top_animes/top_movie_animes.json', 'movie'),
        ]
        
        for filename, type in tasks:
            print(f'Scraping {type} animes...')
            data = scrape_top_animes(page, type)
            file_path = Path(filename)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            save_to_csv(data, file_path)
            print(f'Done scraped {type} animes...')
        
def main():
    run()


if __name__ == "__main__":
    main()