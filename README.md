# ⚽ MISTERSNIPERBOT

Proyecto en Python moderno que automatiza el acceso y scraping de información de [https://mister.mundodeportivo.com](https://mister.mundodeportivo.com), utilizando **Playwright** para navegación automatizada y **FastAPI** para exponer una API web.

---

## 🚀 ¿Qué hace?

- Realiza login automático (o reutiliza cookies de sesión si están activas)
- Extrae:
  - Saldo actual del usuario (ej: `17,2M`)
  - Alineación actual de jugadores
  - Plantilla completa, incluyendo nombre completo y rival
- Devuelve una respuesta estructurada en JSON
- Expone toda la información a través de un servidor FastAPI con múltiples endpoints

---

## 📁 Estructura del proyecto

```
MISTERSNIPERBOT/
├── scraping/
│   ├── browser.py              ← Inicializa navegador con Playwright
│   ├── login.py                ← Login tradicional con email/password
│   ├── saldo.py                ← Extrae saldo del usuario
│   ├── alineacion.py           ← Extrae alineación y plantilla
│   ├── mercado.py              ← Extrae mercado de fichajes
│   ├── sofascore.py            ← Extrae últimos puntos de un jugador
│   └── useragent.py            ← Genera user-agent aleatorio
│
├── utils/
│   ├── logger.py               ← Logger centralizado
│   ├── normalizador.py         ← Función para normalizar nombres completos
│   └── session.py              ← Gestión de cookies persistentes (login automático)
│
├── api/
│   └── main.py                 ← Servidor FastAPI con endpoints públicos
│
├── session/
│   └── cookies.json            ← Cookies persistentes entre sesiones
│
├── .env                        ← Configuración privada (email, password)
├── requirements.txt
├── Dockerfile
├── setup.sh
├── start.bat
└── README.md
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

### 4. Consultar datos

```http
GET http://localhost:8000/saldo
GET http://localhost:8000/mercado
GET http://localhost:8000/puntos?nombre=raul-garcia-de-haro
```

---

## 🐳 Ejecución con Docker (modo recomendado)

### 1. Construir imagen

```bash
docker build -t misterscraper .
```

### 2. Ejecutar contenedor con hot-reload de código

```bash
docker run --env-file .env -p 8000:8000 -v %cd%:/app misterscraper
```

✅ Así puedes editar archivos `.py` desde Windows y el contenedor los usa sin reconstrucción.

---

## 🔐 Archivo `.env`

Configura tus credenciales:

```
EMAIL=tuusuario@correo.com
PASSWORD=tucontraseña
HEADLESS=true
```

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
  "texto_original": "17,2M",
  "alineacion": [...],
  "plantilla": [...]
}
```

---


## 🧼 Autor

Proyecto desarrollado y mantenido por **Raúl Muñoz**.