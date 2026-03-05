from browser_setup import wait_for_captcha
from playwright.async_api import Page
import time
import random
import asyncio

MAX_CONCURRENT_TABS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TABS)

async def getCharacterDetails(page: Page, url):
    
    async with semaphore:
        details_page = await page.context.new_page()
        
        try:
            await wait_for_captcha(page)
            await details_page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            name = await details_page.locator('h2.normal_header').inner_text() if await details_page.locator('h2.normal_header').count() > 0 else None
            japanese_name = await details_page.locator('h2.normal_header small').inner_text() if await details_page.locator('h2.normal_header small').count() > 0 else None
            
            image = await details_page.locator(f'img.portrait-225x350.lazyloaded').get_attribute('src')
            
            info_text = await details_page.locator("h2.normal_header").first.evaluate("""
            el => {
                let text = "";
                let node = el.nextSibling;

                while (node && node.nodeName !== "DIV") {
                    if (node.nodeType === Node.TEXT_NODE) {
                        text += node.textContent;
                    }
                    node = node.nextSibling;
                }

                return text;
            }
            """)
            
            data = {}

            lines = info_text.split("\n")

            for line in lines:
                line = line.strip()

                if line == "":
                    break

                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()
                    
            description = await details_page.locator("h2.normal_header").first.evaluate("""
            el => {
                let text = "";
                let node = el.nextSibling;

                while (node) {

                    if (node.nodeType === Node.TEXT_NODE) {
                        let line = node.textContent.trim();

                        // skip metadata like Height:, Birthday:, etc.
                        if (line && !line.includes(":")) {
                            text += line + " ";
                        }
                    }

                    // stop before next section
                    if (node.nodeType === Node.ELEMENT_NODE &&
                        node.classList &&
                        node.classList.contains("spoiler")) {
                        break;
                    }

                    node = node.nextSibling;
                }

                return text.trim();
            }
            """)
            
            return {
                "name" : {
                    "japanese_name" : japanese_name,
                    "english_name" : name
                },
                "image" : image,
                "info" : data,
                "description" : description
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
        finally:
            await details_page.close()


async def getCharacters(page: Page):
    character_list = []

    book = await page.locator("tr.ranking-list").all()

    for i in book:
        name = await i.locator(".people .information a").inner_text()
        url = await i.locator(".people .information a").get_attribute("href")

        character_list.append({"name": name, "url": url})
    
    tasks = [getCharacterDetails(page, char['url']) for char in character_list]
    results = await asyncio.gather(*tasks)

    return results


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
    return results
