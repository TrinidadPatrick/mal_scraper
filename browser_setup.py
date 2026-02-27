from playwright.async_api import async_playwright
from pathlib import Path
import asyncio

USER_DATA_DIR = str(Path(__file__).parent / "browser_data")

async def get_browser_context(playwright):
    context = await playwright.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
        locale="en-US",
        timezone_id="America/New_York",
        args=[
            "--disable-blink-features=AutomationControlled",
        ]
    )
    
    page = context.pages[0] if context.pages else await context.new_page()
    return page

async def wait_for_captcha(page, timeout=120):
    """
    Detects a Cloudflare human verification page and waits for the user
    to solve it manually before continuing. Returns True if a CAPTCHA
    was detected and solved, False if no CAPTCHA was found.
    """
    try:
        captcha_detected = await page.locator("text=Let's confirm you are human").is_visible(timeout=2000)
        
        if not captcha_detected:
            captcha_detected = await page.locator("text=Human Verification").is_visible(timeout=1000)
        
        if captcha_detected:
            print("CAPTCHA appeared. Please solve it manually in the browser...")
            
            try:
                await page.wait_for_selector(
                    "text=Let's confirm you are human",
                    state="hidden",
                    timeout=timeout * 1000
                )
                print("CAPTCHA solved. Resuming scraping...")
                await asyncio.sleep(2)  # Brief pause after solving
                return True
            except Exception:
                try:
                    await page.wait_for_selector(
                        "text=Human Verification",
                        state="hidden",
                        timeout=timeout * 1000
                    )
                    print("APTCHA solved. Resuming scraping...")
                    await asyncio.sleep(2)
                    return True
                except Exception:
                    print("CAPTCHA was not solved within the time limit.")
                    return False
    except Exception:
        pass
    
    return False