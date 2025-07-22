# scraping/saldo.py
import logging
from playwright.sync_api import Page

def extraer_saldo_sync(page: Page, email: str) -> dict:
    try:
        texto = page.inner_text("div.balance-real-current")
        millones = float(texto.replace("M", "").replace(",", ".").strip())
        return {
            "usuario": email,
            "saldo_millones": millones,
            "texto_original": texto
        }
    except Exception as e:
        logging.error(f"❌ Error extrayendo saldo: {e}")
        return {
            "usuario": email,
            "saldo_millones": None,
            "texto_original": None,
            "error": str(e)
        }
