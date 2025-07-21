@echo off
echo 🔧 Iniciando MisterScraper en Windows...

REM Crear entorno virtual si no existe
if not exist venv (
    echo 📦 Creando entorno virtual...
    python -m venv venv
) else (
    echo ✅ Entorno virtual ya existe.
)

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar dependencias
echo 📚 Instalando dependencias desde requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Instalar navegadores de Playwright
echo 🌐 Instalando navegadores de Playwright...
playwright install

REM Iniciar servidor FastAPI
echo 🚀 Levantando servidor API en http://localhost:8000 ...
uvicorn main:app --reload

echo.
echo ✅ Servidor finalizado.
pause
