from playwright.sync_api import Page
from utils.logger import logger
from scraping.login import hacer_login_sync
import os
from dotenv import load_dotenv
import time
import re

# Carga credenciales
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def extraer_mercado_sync(page: Page) -> list[dict]:
    """
    Realiza login en Mister y navega a la sección Market usando el menú del header.
    Devuelve una lista de dicts con:
      - id_jugador
      - nombre
      - precio_millones (float)
      - avatar
      - equipo_id
    """
    # Hacer click en la pestaña Market del header-menu
    selector = 'div.header-menu li[data-pag="market"] a'
    page.wait_for_selector(selector, timeout=10000)
    page.click(selector)
    logger.info("🔀 Navegando a Market desde header-menu")

     # 1. Esperar lista de elementos en venta
    page.wait_for_selector('ul#list-on-sale li div.player-row', timeout=10000)
    time.sleep(2)  # permitir render dinámico

    items = page.query_selector_all('ul#list-on-sale li div.player-row')
    mercado = []
    for el in items:
        try:
            # Nombre: obtener <a> dentro de div.player-row con data-title
            link = el.query_selector('a[data-title]')
            nombre_attr = link.get_attribute('data-title') if link else None
            nombre = nombre_attr.strip() if nombre_attr else None

            # Valor: buscar <span class="euro">€</span> y extraer texto posterior
            valor = 0.0
            info_div = el.query_selector('div.info')
            if info_div:
                texto = info_div.text_content() or ''
                match = re.search(r'€\s*([\d.,]+)', texto)
                if match:
                    val_str = match.group(1).replace('.', '').replace(',', '.')
                    try:
                        valor = float(val_str)
                    except:
                        valor = 0.0

            mercado.append({'nombre': nombre, 'valor': valor})
        except Exception as e:
            logger.warning(f"⚠️ Error extrayendo jugador de mercado: {e}")

    logger.info(f"✅ Extraídos {len(mercado)} jugadores en mercado")
    return mercado
