from playwright.sync_api import sync_playwright

def get_browser_context(playwright):
    browser = playwright.chromium.launch(headless=False)
    return browser.new_page()