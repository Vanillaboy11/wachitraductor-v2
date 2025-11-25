# Usar imagen base más ligera
FROM python:3.11-slim

# Instalar dependencias del sistema y limpiar en una sola capa
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configurar directorio de trabajo
WORKDIR /app

# Copiar solo requirements primero (para cache de Docker)
COPY requirements-simple.txt requirements.txt

# Instalar PyTorch CPU-only primero (mucho más ligero)
RUN pip install --no-cache-dir torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip \
    && find /usr/local/lib/python3.11 -name '*.pyc' -delete \
    && find /usr/local/lib/python3.11 -name '__pycache__' -delete \
    && find /usr/local/lib/python3.11 -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true

# Copiar solo archivos necesarios
COPY app_simple.py app.py
COPY config.json generation_config.json ./
COPY source.spm target.spm tokenizer_config.json special_tokens_map.json vocab.json ./
COPY model.safetensors ./

# Copiar script de inicio
COPY start.py ./

# Exponer puerto
EXPOSE 8000

# Variables de entorno optimizadas
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TORCH_NUM_THREADS=2 \
    PORT=8000 \
    OMP_NUM_THREADS=2

# Comando para ejecutar la aplicación usando el script de inicio
CMD ["python", "start.py"]
