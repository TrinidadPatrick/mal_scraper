from tools.get_year_range import get_year_range
from tools.parser.seasonal_anime_data_parser import parse
from playwright.sync_api import Page
import time

def get_seasonal_animes(page: Page):
    seasonal_anime_lists = page.locator(".seasonal-anime").all()
    print(f"Found {len(seasonal_anime_lists)} items")
    seasonal_animes = []

    for index, book in enumerate(seasonal_anime_lists):
        print(f"Scraping anime # {index + 1}....")
        parsed_data = parse(book)
        
        seasonal_animes.append(parsed_data)
    
    return seasonal_animes

def scrape_seasonal_animes(page: Page, type):
    seasons = ['winter', 'spring', 'summer', 'fall']
    years = get_year_range(2025)
    
    results = []
    for year in years:
        for season in seasons:
            page.goto(f"https://myanimelist.net/anime/season/{year}/{season}")
            
            if page.locator('#accept-btn').is_visible():
                page.locator('#accept-btn').click()
            
            kidsBtn = page.locator('.btn-show-kids.crossed')
            
            # uncheck hide kids
            if kidsBtn.is_visible():
                kidsBtn.click()
            
            # Uncheck hide r18
            showR18Btn = page.locator('.btn-show-r18.crossed')
            if showR18Btn.is_visible():
                showR18Btn.click()
            
            
            result = get_seasonal_animes(page)
            
            results.append({'year' : year, 'season' : season, 'data' : result})
            
    return results
    
    return