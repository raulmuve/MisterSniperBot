from fastapi import FastAPI
from fastapi.responses import JSONResponse
from scraping.browser import get_browser
from scraping.login import hacer_login
from scraping.saldo import extraer_saldo
from scraping.alineacion import extraer_alineacion
from utils.logger import logger
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

app = FastAPI()

@app.get("/sald")
def obtener_saldo():
    navegador = get_browser()
    context = navegador.new_context()
    page = context.new_page()

    try:
        hacer_login(page, EMAIL, PASSWORD)
        saldo_info = extraer_saldo(page)
        alineacion = extraer_alineacion(page)

        respuesta = {
            "usuari": EMAIL,
            "saldo_millones": saldo_info["valor"],
            "texto_original": saldo_info["texto"],
            "alineacion": alineacion
        }
        return JSONResponse(content=respuesta)

    except Exception as e:
        logger.error(f"❌ Error en /saldo: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        context.close()
        navegador.close()
