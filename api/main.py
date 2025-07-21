from fastapi import FastAPI
import asyncio
from scraping.login import hacer_login
from scraping.saldo import extraer_saldo
import json
import logging

app = FastAPI()

@app.get("/saldo")
async def obtener_saldo():
    try:
        browser, page, email = await hacer_login()
        datos = await extraer_saldo(page, email)
        await browser.close()
        return datos
    except Exception as e:
        logging.error(f"❌ Error al procesar /saldo: {e}")
        return {"error": str(e)}
