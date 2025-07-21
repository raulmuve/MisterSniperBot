import os
from dotenv import load_dotenv
from scraping.browser import get_browser

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

async def hacer_login():
    browser, page = await get_browser()
    await page.goto("https://mister.mundodeportivo.com/new-onboarding/auth/email/sign-in?email=admin@raulmuve.com")

    # Aceptar cookies
    try:
        await page.click("text=Aceptar y continuar", timeout=3000)
    except:
        pass

    await page.fill('input[type="email"]', EMAIL)
    await page.fill('input[type="password"]', PASSWORD)
    await page.click('button[type="submit"]')
    await page.wait_for_timeout(5000)

    return browser, page, EMAIL  # <- devolvemos el navegador abierto
