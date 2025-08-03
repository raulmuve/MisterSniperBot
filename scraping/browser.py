# scraping/browser.py
import sys
import os
import asyncio
from playwright.sync_api import sync_playwright
from scraping.useragent import get_random_user_agent
from utils.session import get_storage_state_path  # NUEVO

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_browser():
    playwright = sync_playwright().start()
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    browser = playwright.chromium.launch(headless=headless)

    storage_state_path = get_storage_state_path()

    context_args = {
        "user_agent": get_random_user_agent(),
        "viewport": {"width": 1366, "height": 768},
        "locale": "es-ES",
        "timezone_id": "Europe/Madrid",
        "geolocation": {"longitude": -3.7038, "latitude": 40.4168},
        "permissions": ["geolocation"],
    }

    if os.path.exists(storage_state_path):
        context_args["storage_state"] = storage_state_path

    context = browser.new_context(**context_args)
    page = context.new_page()

    # ⚠️ Anti-bot fingerprints
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    """)

    return playwright, browser, page
