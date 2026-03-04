from playwright.async_api import Page
from tools.validateNumber import is_valid_integer

async def getAnimeDetails(page: Page):
    title = await page.locator('.title-name strong').inner_text() if await page.locator('.title-name strong').count() > 0 else None
    title_english = await page.locator('.title-english').inner_text() if await page.locator('.title-english').count() > 0 else None
    
    score = await page.locator('div.score-label').inner_text()
    
    member_element_selector = ".fl-l.score"
    
    after_content = await page.evaluate(f"""
    (selector) => {{
        const element = document.querySelector(selector);
        if (!element) return null;
        
        const style = window.getComputedStyle(element, '::after');
        
        return style.getPropertyValue('content');
    }}
    """, member_element_selector)
    
    users = after_content.strip('"').strip("'").split(" ")[0].replace(",","")
    
    rank = await page.locator('span.numbers.ranked strong').inner_text()
    popularity = await page.locator('span.numbers.popularity strong').inner_text()
    members = await page.locator('span.numbers.members strong').inner_text()
    
    season = await page.locator('span.information.season a').inner_text() if await page.locator('span.information.season a').count() > 0 else None
    type = await page.locator('span.information.type a').inner_text() if await page.locator('span.information.type a').count() > 0 else None
    studio = await page.locator('span.information.studio.author').inner_text() if await page.locator('span.information.studio.author').count() > 0 else None
    
    synopsis = await page.locator('p[itemprop="description"]').inner_text() if await page.locator('p[itemprop="description"]').count() > 0 else None
    
    infos = await page.locator('div.spaceit_pad').all()
    
    info_dict = {}
    for i in infos:
        value = await i.inner_text()
        splitted = value.split(": ", 1)
        if len(splitted) == 2:
            key = splitted[0].strip()
            val = splitted[1].strip()
            info_dict[key] = val
    
    print(info_dict['Episodes'])
        
    return {
        "title" : {
            "title_japanese" : title,
            "title_english" : title_english
        },
        "score" : score,
        "scored_by" : int(users) if is_valid_integer(users) else 0,
        "rank" : int(rank.replace("#","")),
        "popularity" : int(popularity.replace("#","")),
        "members" : int(members.replace(",","")),
        
        "season" : season,
        "type" : type,
        "studio" : studio,
        
        "synopsis" : synopsis
        
    }