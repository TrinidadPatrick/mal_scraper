from browser_setup import wait_for_captcha
from playwright.async_api import Page
import time
import random
import asyncio


async def getCharacters(page: Page):
    character_list = []

    book = await page.locator("tr.ranking-list").all()

    for i in book:
        name = await i.locator(".people .information a").inner_text()
        url = await i.locator(".people .information a").get_attribute("href")

        character_list.append({"name": name, "url": url})

    return []


async def scrape_characters(page: Page, pageLimit: int):
    start_time = time.perf_counter()

    await page.goto(
        f"https://myanimelist.net/character.php", wait_until="domcontentloaded"
    )

    await wait_for_captcha(page)

    if await page.locator("#accept-btn").is_visible():
        await page.locator("#accept-btn").click()

    results = []

    for i in range(pageLimit):
        print(f"scraping characters page # {i + 1}")
        result = await getCharacters(page)
        results.extend(result)

        next_btn = page.locator("a.link-blue-box.next").first
        if await next_btn.is_visible():
            async with page.expect_navigation():
                await next_btn.click()

            await wait_for_captcha(page)

            delay = random.uniform(1.5, 4.0)
            await asyncio.sleep(delay)
        else:
            break
