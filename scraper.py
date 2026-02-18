from playwright.sync_api import sync_playwright
from browser_setup import get_browser_context
from scrapers.top_animes_scraper import scrape
import json

def save_to_csv(data, filename):
    print(data[0].keys())
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def run():
    with sync_playwright() as playwright:
        page =  get_browser_context(playwright)
        
        data = scrape(page)
        
        save_to_csv(data, 'top_animes.json')
        
def main():
    run()


if __name__ == "__main__":
    main()