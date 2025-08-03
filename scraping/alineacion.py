from playwright.sync_api import Page
from utils.logger import logger
from utils.nombres import normalizar_nombre
import re

POSICIONES = {
    "1": "POR",
    "2": "DEF",
    "3": "MED",
    "4": "DEL"
}

def ir_a_equipo(page: Page) -> None:
    try:
        page.wait_for_selector('li[data-pag="team"] a.navbar-switch-tab', timeout=5000)
        page.click('li[data-pag="team"] a.navbar-switch-tab')
        page.wait_for_selector(".team__lineup, ul.player-list.player-list--secondary.list-team", timeout=5000)
        logger.info("✅ Página de equipo cargada correctamente")
    except Exception as e:
        logger.warning(f"⚠️ No se pudo acceder a la página de equipo: {e}")

def extraer_alineacion_sync(page: Page) -> list[dict]:
    ir_a_equipo(page)
    jugadores = []
    elementos = page.query_selector_all("button.lineup-player")
    for el in elementos:
        try:
            nombre = el.query_selector(".name").text_content().strip()
            posicion = el.get_attribute("data-position")
            id_jugador = el.get_attribute("data-id_player")
            puntos = el.query_selector(".points").text_content().strip()
            avatar = el.query_selector(".player-avatar img").get_attribute("src")
            equipo_img = el.query_selector(".team-logo").get_attribute("src")
            equipo_id = int(equipo_img.split("/teams/")[-1].split(".")[0])
            jugadores.append({
                "nombre": nombre,
                "posicion": POSICIONES.get(posicion, posicion),
                "id_jugador": int(id_jugador),
                "puntos": int(puntos),
                "equipo_id": equipo_id,
                "avatar": avatar
            })
        except Exception as inner:
            logger.warning(f"⚠️ Error procesando un jugador alineado: {inner}")
    logger.info(f"✅ Extraídos {len(jugadores)} jugadores alineados")
    return jugadores

def extraer_plantilla_sync(page: Page) -> list[dict]:
    ir_a_equipo(page)
    plantilla = []
    selector = 'ul.player-list.player-list--secondary.list-team li'
    try:
        page.wait_for_selector(selector, timeout=5000)
        items = page.query_selector_all(selector)
        for li in items:
            try:
                raw_id = li.get_attribute('id')
                id_jugador = int(raw_id.split('-')[-1])

                a = li.query_selector('a.player')
                link = a.get_attribute('href')

                nombre_raw = link.split('/')[-1].replace('-', ' ').title()
                if '.' in nombre_raw.split(' ')[0]:
                    nombre = normalizar_nombre(nombre_raw, link)
                else:
                    nombre = nombre_raw

                pos = li.query_selector('.player-position').get_attribute('data-position')
                posicion = POSICIONES.get(pos, pos)

                raw_valor = li.query_selector('.underName').text_content()
                match = re.search(r'[\d.,]+', raw_valor)
                if match:
                    valor_str = match.group(0).replace('.', '').replace(',', '.')
                    valor = float(valor_str)
                else:
                    valor = None

                avg_text = li.query_selector('.streak-wrapper .avg').text_content().strip()
                promedio = float(avg_text.replace(',', '.'))

                rival_img = li.query_selector('.rival img')
                equipo_rival = int(rival_img.get_attribute('src').split('/teams/')[-1].split('.')[0]) if rival_img else None

                avatar = li.query_selector('.player-avatar img').get_attribute('src')

                plantilla.append({
                    'id_jugador': id_jugador,
                    'nombre': nombre,
                    'posicion': posicion,
                    'valor': valor,
                    'promedio': promedio,
                    'equipo_rival_id': equipo_rival,
                    'avatar': avatar,
                    'link': link
                })
            except Exception as ex:
                logger.warning(f"⚠️ Error procesando jugador de plantilla: {ex}")
        logger.info(f"✅ Extraída plantilla completa: {len(plantilla)} jugadores")
    except Exception as e:
        logger.error(f"❌ No se encontró la lista de plantilla: {e}")
    return plantilla
