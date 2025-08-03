from fastapi import FastAPI
from fastapi.responses import JSONResponse
from scraping.browser import get_browser
from scraping.login import hacer_login_sync
from scraping.saldo import extraer_saldo_sync
from scraping.alineacion import extraer_alineacion_sync, extraer_plantilla_sync
from scraping.sofascore import extraer_partidos_ultimos_sync
from scraping.mercado import extraer_mercado_sync
from utils.logger import logger

from dotenv import load_dotenv
import os
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()

@app.get("/saldo")
def obtener_saldo():
    playwright, browser, page = get_browser()
    try:
        # Siempre ir al dashboard tras abrir el navegador
        page.goto("https://mister.mundodeportivo.com/market", timeout=10000)
        
        # Solo hacer login si no está ya logueado
        if "login" in page.url or "sign-in" in page.url:
            hacer_login_sync(page, EMAIL, PASSWORD)

        # Ahora sí: extraer todo
        saldo_info = extraer_saldo_sync(page, EMAIL)
        alineacion = extraer_alineacion_sync(page)
        plantilla = extraer_plantilla_sync(page)

        return JSONResponse(content={
            "usuario": EMAIL,
            "saldo_millones": saldo_info["saldo_millones"],
            "texto_original": saldo_info["texto_original"],
            "alineacion": alineacion,
            "plantilla": plantilla
        })
    except Exception as e:
        logger.error(f"❌ Error en /saldo: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        browser.close()
        playwright.stop()

@app.get("/puntos")
def obtener_puntos(nombre: str):
    playwright, browser, page = get_browser()
    try:
        partidos = extraer_partidos_ultimos_sync(page, nombre, 10)
        return JSONResponse(content={
            "jugador": nombre,
            "ultimos_partidos": partidos
        })
    except Exception as e:
        logger.error(f"❌ Error en /puntos: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        browser.close()
        playwright.stop()


@app.get("/mercado")
def obtener_mercado():
    playwright, browser, page = get_browser()
    try:
        hacer_login_sync(page, EMAIL, PASSWORD)
        mercado = extraer_mercado_sync(page)
        return JSONResponse(content={"mercado": mercado})
    except Exception as e:
        logger.error(f"❌ Error en /mercado: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        browser.close()
        playwright.stop()
