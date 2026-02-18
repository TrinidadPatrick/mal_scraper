from playwright.sync_api import sync_playwright
import csv

def get_top_animes(page):
    top_anime_lists = page.locator(".ranking-list").all()

    top_anime_titles = []

    for index, book in enumerate(top_anime_lists):
        title_container = book.locator('.title')
        title = title_container.locator('.anime_ranking_h3 a').inner_text()
        top_anime_titles.append({'title': title})
    
    return top_anime_titles

def run():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)    
        page = browser.new_page()

        print("Navigating to the MAL...")
        
        page.goto("https://myanimelist.net/topanime.php")
        page.locator('#accept-btn').click()
        results = []
        
        for i in range(20):
            result = get_top_animes(page)
            results.extend(result)
            next_btn_selector = 'a.link-blue-box.next'
            page.wait_for_selector(next_btn_selector)
            with page.expect_navigation():
                page.locator(next_btn_selector).first.click()
                
        with open('top_animes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title'])

            writer.writeheader()

            writer.writerows(test)

        print("Data scrapped")

def main():
    run()


if __name__ == "__main__":
    main()