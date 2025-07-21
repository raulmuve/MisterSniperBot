# ⚽ MISTERSNIPERBOT

Proyecto Python moderno para automatizar el login y scraping del saldo en [https://mister.mundodeportivo.com](https://mister.mundodeportivo.com), usando **Playwright** y exponiendo un **endpoint HTTP (`/saldo`)** con **FastAPI**.

---

## 🚀 ¿Qué hace?

- Hace login automático con tu cuenta del Míster
- Extrae tu saldo actual (ej: `17,2M`)
- Devuelve un JSON con:
  - Tu email
  - Saldo numérico en millones (float)
  - Texto original del saldo
- Expone todo a través de un servidor FastAPI (`/saldo`)
- Puede ejecutarse:
  - En local (Windows, con navegador visible o headless)
  - En Docker (Linux o Windows, headless y montado en caliente)

---

## 📁 Estructura del proyecto

```
MISTERSNIPERBOT/
├── scraping/
│   ├── browser.py
│   ├── login.py
│   ├── saldo.py
│   └── useragent.py
│
├── utils/
│   └── logger.py
│
├── api/
│   └── main.py             ← Servidor FastAPI con endpoint `/saldo`
│
├── .env                    ← Tus credenciales
├── requirements.txt
├── Dockerfile
├── setup.sh
├── start.bat
├── main.py                 ← (opcional, ejecución directa)
└── README.md               ← Este documento
```

---

## 🧪 Ejecución local (Windows)

### 1. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
playwright install
```

### 3. Ejecutar servidor local FastAPI

```bash
uvicorn api.main:app --reload
```

### 4. Consultar saldo

Abre en tu navegador o desde Postman:

```
http://localhost:8000/saldo
```

---

## 🐳 Ejecución con Docker (modo recomendado)

### 1. Construir imagen (solo una vez)

```bash
docker build -t misterscraper .
```

### 2. Ejecutar contenedor con código en caliente

```bash
docker run --env-file .env -p 8000:8000 -v %cd%:/app misterscraper
```

✅ Así puedes editar archivos `.py` desde Windows y el contenedor los usa **sin tener que reconstruir la imagen**.

---

## 📦 Endpoint `/saldo`

```http
GET http://localhost:8000/saldo
```

### ✅ Respuesta JSON

```json
{
  "usuario": "tuemail@dominio.com",
  "saldo_millones": 17.2,
  "texto_original": "17,2M"
}
```

---

## 🔐 Archivo `.env`

Configura tus credenciales:

```
EMAIL=tuusuario@correo.com
PASSWORD=tucontraseña
HEADLESS=true
```

> Si estás en Windows y quieres ver el navegador, pon `HEADLESS=false`

---

## 🔇 Silencio a errores basura

Este proyecto **filtra permanentemente** los errores molestos de Windows/asyncio como:

- `RuntimeError: Event loop is closed`
- `ValueError: I/O operation on closed pipe`

Ya no te volverán a tocar los huevos.

---

## ✅ Tecnologías usadas

| Tecnología     | Uso                                    |
|----------------|----------------------------------------|
| Playwright     | Automatización de navegador (login + scraping) |
| FastAPI        | Servidor web ultrarrápido para exponer `/saldo` |
| Uvicorn        | Servidor ASGI moderno para FastAPI     |
| Fake UserAgent | Rotación de user-agents para no ser detectado |
| Python-dotenv  | Carga de credenciales desde `.env`     |
| Docker         | Ejecución portable y aislada           |

---

## 🧠 Posibles mejoras futuras

- Scraping del mercado de fichajes
- Scraping de alineación y puntos por jornada
- Envío de alertas por Telegram
- Panel web para visualizar estadísticas
- Scheduling con cron o Celery

---

## 🧼 Autor

Bot creado y mantenido con odio por **Yoguiito**.  
No se aceptan sugerencias blanditas. Solo mejoras reales.
