# Imagen base oficial de Python 3.12 slim
FROM python:3.12-slim

# Evitar bytecode y buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY . .

# Instalar dependencias del sistema necesarias para ejecutar Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libxkbcommon0 \
    libxfixes3 \
    libcairo2 \
    libpango-1.0-0 \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python y Playwright
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && playwright install

# Exponer el puerto donde corre FastAPI
EXPOSE 8000

# Comando de inicio: ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
