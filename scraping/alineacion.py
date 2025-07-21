from playwright.async_api import Page
from utils.logger import logger

POSICIONES = {
    "1": "POR",
    "2": "DEF",
    "3": "MED",
    "4": "DEL"
}

def ir_a_equipo(page: Page) -> None:
    """Navega hasta la página de 'Equipo' haciendo clic en el icono correspondiente de la cabecera."""
    try:
        page.wait_for_selector('button[data-sw="team"]', timeout=5000)
        page.click('button[data-sw="team"]')
        page.wait_for_selector(".team__lineup", timeout=5000)
        logger.info("✅ Página de equipo cargada correctamente")
    except Exception as e:
        logger.warning(f"⚠️ No se pudo acceder a la página de equipo: {e}")


def extraer_alineacion(page: Page) -> list[dict]:
    """Extrae los jugadores alineados en el equipo titular."""
    ir_a_equipo(page)

    jugadores = []
    elementos = page.query_selector_all("button.lineup-player")

    for el in elementos:
        nombre = el.query_selector_eval(".name", "el => el.textContent.trim()")
        posicion = el.get_attribute("data-position")
        id_jugador = el.get_attribute("data-id_player")
        puntos = el.query_selector_eval(".points", "el => el.textContent.trim()")
        avatar = el.query_selector_eval(".player-avatar img", "el => el.src")
        equipo_img = el.query_selector_eval(".team-logo", "el => el.src")

        equipo_id = equipo_img.split("/teams/")[-1].split(".")[0]

        jugadores.append({
            "nombre": nombre,
            "posicion": POSICIONES.get(posicion, posicion),
            "id_jugador": int(id_jugador),
            "puntos": int(puntos),
            "equipo_id": int(equipo_id),
            "avatar": avatar
        })

    logger.info(f"✅ Extraídos {len(jugadores)} jugadores alineados")
    return jugadores
