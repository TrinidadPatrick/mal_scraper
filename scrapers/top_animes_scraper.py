import csv
from playwright.sync_api import Page
from tools.parser.top_animes_data_parser import parse

def get_top_animes(page: Page):
    top_anime_lists = page.locator(".ranking-list").all()

    top_animes = []

    for index, book in enumerate(top_anime_lists):
        parsed_data = parse(book)
        
        top_animes.append(parsed_data)
    
    return top_animes

def scrape_top_animes(page, type):
    page.goto(f"https://myanimelist.net/topanime.php?type={type}")
    
    if page.locator('#accept-btn').is_visible():
        page.locator('#accept-btn').click()
        
    results = []

    # Only get animes on page 1
    for i in range(1):
        
        result = get_top_animes(page)
        results.extend(result)
        
        next_btn_selector = 'a.link-blue-box.next'
        next_btn = page.locator('a.link-blue-box.next').first
        if(next_btn.is_visible()):
            with page.expect_navigation():
                next_btn.first.click()
        else:
            break
        
    return results