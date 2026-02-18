from playwright.sync_api import sync_playwright
import csv

def run():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)    
        page = browser.new_page()

        print("Navigating to the MAL...")
        page.goto("https://myanimelist.net/topanime.php")

        top_anime_lists = page.locator(".ranking-list").all()

        top_anime_titles = []

        for index, book in enumerate(top_anime_lists):
            title_container = book.locator('.title')
            title = title_container.locator('.anime_ranking_h3 a').inner_text()
            top_anime_titles.append({'title': title})
        # print(top_anime_titles)
        if(len(top_anime_titles) > 0):
            with open('top_animes.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['title'])

                writer.writeheader()

                writer.writerows(top_anime_titles)


def main():
    run()


if __name__ == "__main__":
    main()