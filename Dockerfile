# Imagen base ligera con Python
FROM python:3.11-slim

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY app.py .
COPY onnx_models/ ./onnx_models/
COPY source.spm target.spm tokenizer_config.json special_tokens_map.json vocab.json ./

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV WORKERS=1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
