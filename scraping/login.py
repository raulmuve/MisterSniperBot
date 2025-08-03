# scraping/login.py
from playwright.sync_api import Page
from utils.logger import logger
from utils.storage import save_storage_state

def hacer_login_sync(page: Page, email: str, password: str) -> None:
    page.goto(
        "https://mister.mundodeportivo.com/new-onboarding/auth/email/sign-in?email=admin@raulmuve.com"
    )
    try:
        page.click("text=Aceptar y continuar", timeout=3000)
    except:
        pass

    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_timeout(5000)

    # Guardar sesión
    save_storage_state(page.context)

    logger.info("✅ Login completado")
