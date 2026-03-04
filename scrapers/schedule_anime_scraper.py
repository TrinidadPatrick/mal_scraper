from tools.get_year_range import get_year_range
from tools.parser.seasonal_anime_data_parser import parse
from tools.parser.anime_details_parser import getAnimeDetails
import browser_setup
from playwright.async_api import Page
from browser_setup import wait_for_captcha
import asyncio
import random
import time


async def get_scheduled_animes(page: Page):

    seasonal_animes = await page.evaluate("""
        () => {
            const results = [];
            const lists = document.querySelectorAll('.seasonal-anime-list');
            
            lists.forEach(list => {
                const animeType = list.querySelector('.anime-header')?.innerText.trim() || 'Unknown';
                const animeCards = list.querySelectorAll('.seasonal-anime');
                
                animeCards.forEach((book, index) => {
                    
                    try {
                        const image = book.querySelector('.image img')?.getAttribute('src');
                        const image2 = book.querySelector('.image img')?.getAttribute('data-src');
                        
                        const url = book.querySelector('.h2_anime_title a').getAttribute('href')
                        console.log(url)
                        
                        const title = book.querySelector('.title .link-title')?.innerText.trim();
                        
                        const infoItems = Array.from(book.querySelectorAll('.prodsrc .info .item'))
                            .map(span => span.innerText.trim().replace(/\\\\n/g, ' '));
                        
                        const properties = Array.from(book.querySelectorAll('.properties > .property')).map(prop => ({
                            name: prop.querySelector('.caption')?.innerText.trim(),
                            values: Array.from(prop.querySelectorAll('.item')).map(i => i.innerText.trim())
                        }));

                        const genres = Array.from(book.querySelectorAll('.genre')).map(item => {
                            const link = item.querySelector('a');
                            const href = link?.getAttribute('href') || "";
                            return {
                                genre: link?.innerText.trim(),
                                mal_id: href.split("/")[3] || null
                            };
                        });

                        const members = book.querySelector('.member')?.innerText.trim();
                        const score = book.querySelector('.score.score-label')?.innerText.trim();
                        const malIdRoot = book.querySelector('.genres')?.getAttribute('id');

                        results.push({
                            type: animeType,
                            image : image || image2,
                            title,
                            url,
                            mal_id: malIdRoot,
                            genres,
                            properties,
                            info: infoItems,
                            members,
                            score
                        });
                    } catch (e) {
                        console.error(`Error parsing index ${index}:`, e);
                    }
                });
            });
            return results;
        }
    """)
    
    
    for i, anime in enumerate(seasonal_animes):
        print(f"Scraping details for anime #{i + 1}: {anime['title']}")
        detail_page = await page.context.new_page()
        await detail_page.goto(anime['url'])
        
        details = await getAnimeDetails(detail_page)
        
        seasonal_animes[i]['full'] = details
        
        delay = random.uniform(1, 1.5)
        await asyncio.sleep(delay)
        
        await detail_page.close()
    return seasonal_animes


async def scrape_scheduled_animes(page: Page, type):

    start_time = time.perf_counter()

    await page.goto(
        f"https://myanimelist.net/anime/season/schedule", wait_until="domcontentloaded"
    )
    

    await wait_for_captcha(page)

    try:
        await page.wait_for_selector(".seasonal-anime-list", timeout=15000)
    except Exception:
        print(f"Could not find anime list, skipping...")

    if await page.locator("#accept-btn").is_visible():
        await page.locator("#accept-btn").click()

    kidsBtn = page.locator(".btn-show-kids.crossed")

    # uncheck hide kids
    if await kidsBtn.is_visible():
        await kidsBtn.click()

    # Uncheck hide r18
    showR18Btn = page.locator(".btn-show-r18.crossed")
    if await showR18Btn.is_visible():
        await showR18Btn.click()

    result = await get_scheduled_animes(page)

    print(f"Scraped {len(result)} anime for this season")

    delay = random.uniform(1.5, 4.0)
    await asyncio.sleep(delay)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time for scraping seasonal animes: {elapsed_time:.4f} seconds")

    return result
