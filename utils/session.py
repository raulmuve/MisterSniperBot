import os
from playwright.sync_api import sync_playwright
from scraping.useragent import get_random_user_agent
from scraping.login import hacer_login_sync
from utils.logger import logger
from dotenv import load_dotenv
from utils.storage import save_storage_state, get_storage_state_path

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def cargar_contexto_con_cookies():
    playwright = sync_playwright().start()
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    browser = playwright.chromium.launch(headless=headless)

    # Contexto con o sin storage_state según exista la cookie
    context = browser.new_context(
        user_agent=get_random_user_agent(),
        viewport={"width": 1366, "height": 768},
        locale="es-ES",
        timezone_id="Europe/Madrid",
        geolocation={"longitude": -3.7038, "latitude": 40.4168},
        permissions=["geolocation"],
        storage_state=get_storage_state_path() if os.path.exists(get_storage_state_path()) else None
    )

    page = context.new_page()

    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    """)

    try:
        # Ir a una URL pública, no directamente al team
        page.goto("https://mister.mundodeportivo.com/market", timeout=10000)
        logger.debug(f"🌐 URL actual tras cookie: {page.url}")
        page.screenshot(path="debug_cookie.png")

        if page.locator("div.balance-real-current").is_visible(timeout=10000):
            logger.info("✅ Cookie válida, acceso sin login")
            return playwright, browser, page

        logger.warning("⚠️ Cookie inválida o expirada. Rehaciendo login...")

    except Exception as e:
        logger.warning(f"⚠️ No se pudo usar la cookie, forzando login: {e}")

    # Si falla la cookie o es inválida → Login manual
    context = browser.new_context(
        user_agent=get_random_user_agent(),
        viewport={"width": 1366, "height": 768},
        locale="es-ES",
        timezone_id="Europe/Madrid",
        geolocation={"longitude": -3.7038, "latitude": 40.4168},
        permissions=["geolocation"]
    )

    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    """)

    # Login manual
    hacer_login_sync(page, EMAIL, PASSWORD)
    save_storage_state(context)

    return playwright, browser, page
