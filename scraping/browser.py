# scraping/browser.py
import sys
import asyncio
from playwright.sync_api import sync_playwright
from scraping.useragent import get_random_user_agent
import os

# Solución para Windows: usar SelectorEventLoopPolicy para subprocessos
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_browser():
    playwright = sync_playwright().start()
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context(
        user_agent=get_random_user_agent(),
        viewport={"width": 1366, "height": 768},
        locale="es-ES"
    )
    page = context.new_page()
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return playwright, browser, page
