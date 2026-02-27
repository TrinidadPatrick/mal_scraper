import csv
from playwright.async_api import Page
from browser_setup import wait_for_captcha
from tools.parser.top_animes_data_parser import parse
import asyncio
import random
import time

async def get_top_animes(page: Page):
    top_animes = await page.evaluate(r"""
        () => {
            const results = [];
            const rows = document.querySelectorAll('.ranking-list');
            
            rows.forEach((book, index) => {
                try {
                    // 1. Title
                    const title = book.querySelector('.title .anime_ranking_h3 a')?.innerText.trim();
                    
                    // 2. Score
                    const score = book.querySelector('.score .score-label')?.innerText.trim();
                    
                    // 3. Information String (Handling the split logic)
                    const infoText = book.querySelector('.detail .information')?.innerText.trim() || "";
                    const detailsArray = infoText.split('\\n');
                    
                    // Logic mirroring your Python parser:
                    // Example format: "TV (12 eps) \n Oct 2022 - Dec 2022 \n 1,234,567 members"
                    
                    const firstLine = detailsArray[0] || "";
                    const type = firstLine.split(' ')[0];
                    const episodes = firstLine.split(' ')[1]?.replace("(", "").replace(")", "");
                    
                    const members = detailsArray[2]?.split(' ')[0] || "0";
                    
                    const airLine = detailsArray[1] || "";
                    const parts = airLine.split(' - ');
                    const air = {
                        aired_from: parts[0]?.trim() || null,
                        aired_to: parts[1]?.trim() || null
                    };

                    results.push({
                        title,
                        type,
                        episodes,
                        air,
                        members,
                        score
                    });
                } catch (e) {
                    console.error(`Error parsing index ${index}:`, e);
                }
            });
            return results;
        }
    """)
    
    top_animes = [anime for anime in top_animes if anime]
    
    return top_animes

async def scrape_top_animes(page, type):
    await page.goto(f"https://myanimelist.net/topanime.php?type={type}", wait_until="domcontentloaded")
    
    await wait_for_captcha(page)
    
    try:
        await page.wait_for_selector('.ranking-list', timeout=15000)
    except Exception:
        print(f'Could not find ranking list for {type}, skipping...')
        return []
    
    if await page.locator('#accept-btn').is_visible():
        await page.locator('#accept-btn').click()
        
    results = []

    start_time = time.perf_counter()
    # Only get 10 pages
    for i in range(10):
        print(f'scraping {type} anime page # {i + 1}')
        result = await get_top_animes(page)
        results.extend(result)
        
        next_btn = page.locator('a.link-blue-box.next').first
        if await next_btn.is_visible():
            async with page.expect_navigation():
                await next_btn.click()
            
            await wait_for_captcha(page)
            
            delay = random.uniform(1.5, 4.0)
            await asyncio.sleep(delay)
        else:
            break
        
        
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time for scraping {type} anime: {elapsed_time:.4f} seconds")
        
    return results