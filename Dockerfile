FROM python:3.9-slim

# Actualiza la lista de paquetes e instala dependencias necesarias para OpenCV, YOLO, etc.
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libglib2.0-dev \
    libsm6 \
    libxrender1 \
    libxext6 \
    libopenblas-dev \
    libomp-dev \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Define variables de entorno para Matplotlib y Ultralytics
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV ULTRALYTICS_HOME=/tmp/ultralytics

# Crea los directorios de configuración en /tmp y ajusta sus permisos para que sean escribibles
RUN mkdir -p /tmp/matplotlib /tmp/ultralytics && \
    chmod -R 777 /tmp/matplotlib /tmp/ultralytics

WORKDIR /app

# Copia el archivo de requisitos y luego instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# (Opcional) Agrega un healthcheck para que la plataforma verifique que la aplicación responde
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]



