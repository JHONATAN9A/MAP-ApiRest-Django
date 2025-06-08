FROM python:3.11-slim

# Instalar dependencias del sistema para GeoDjango
RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin \
    python3-dev libgdal-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear y activar el entorno de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --upgrade pip \
 && pip install -r requirements.txt


# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Puerto expuesto para Railway
EXPOSE 8080

# Comando de ejecución
CMD ["gunicorn", "prueba_tecnica.wsgi:application", "--bind", "0.0.0.0:8080"]