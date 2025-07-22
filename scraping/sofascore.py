from playwright.sync_api import Page
from utils.logger import logger
import time


def buscar_jugador_sync(page: Page, nombre_apellidos: str) -> str:
    """
    Busca al jugador en SofaScore usando el buscador de la página y devuelve la URL de su página.
    """
    page.goto("https://www.sofascore.com/es/", timeout=60000)
    # Gestionar pop-up de cookies
    try:
        consent_button = page.query_selector('button:has-text("Consentir")')
        if consent_button:
            consent_button.click()
            logger.info("🍪 Consentimiento de cookies aceptado")
            time.sleep(1)
    except Exception as e:
        logger.warning(f"⚠️ No se pudo aceptar cookies: {e}")
    # Rellenar el buscador
    page.click('input#search-input')
    page.fill('input#search-input', nombre_apellidos)
    time.sleep(3)
    # Seleccionar primer resultado de jugador
    selector = 'a[href^="/es/football/player/"]'
    page.wait_for_selector(selector, timeout=10000)
    primer = page.query_selector_all(selector)[0]
    href = primer.get_attribute('href')
    url_completa = "https://www.sofascore.com" + href
    logger.info(f"🔍 Jugador encontrado: {url_completa}")
    return url_completa


def extraer_partidos_ultimos_sync(page: Page, nombre_apellidos: str, num_partidos: int = 10) -> list[dict]:
    """
    Extrae la fecha, el oponente y el valor (aria-valuenow) de los últimos partidos de un jugador en SofaScore.
    Devuelve una lista de diccionarios con keys: fecha, oponente, valor.
    Si no hay valor o no se puede parsear, retorna 0.
    """
    player_url = buscar_jugador_sync(page, nombre_apellidos)
    # Navegar a la página del jugador
    page.goto(player_url, timeout=60000)
    # Dar tiempo a la carga dinámica
    time.sleep(2)
    # Esperar a que aparezca la sección de partidos
    page.wait_for_selector('.player-matches-section', timeout=10000)
    section = page.query_selector('.player-matches-section')
    # Obtener todos los enlaces de partidos
    items = section.query_selector_all('a[data-id]')
    partidos = []
    for item in items[:num_partidos]:
        try:
            # Fecha: <div title="..."><bdi>01.01.2025</bdi></div>
            fecha_el = item.query_selector('div[title] bdi')
            fecha = fecha_el.text_content().strip() if fecha_el else None
            # Oponente: extraer todo el atributo title del div con "Resultado"
            oponente = None
            for div in item.query_selector_all('div[title]'):
                title = div.get_attribute('title')
                if title and title.startswith('Resultado'):
                    oponente = title
                    break
            # Valor: atributo aria-valuenow en el span o elemento [role="meter"]
            valor = 0.0
            meter = item.query_selector('[role="meter"]')
            if meter:
                val = meter.get_attribute('aria-valuenow')
                try:
                    valor = float(val)
                except:
                    valor = 0.0
            partidos.append({
                'fecha': fecha,
                'oponente': oponente,
                'valor': valor
            })
        except Exception as e:
            logger.warning(f"⚠️ Error extrayendo datos de partido: {e}")
    logger.info(f"✅ Extraídos {len(partidos)} partidos para {nombre_apellidos}")
    return partidos
