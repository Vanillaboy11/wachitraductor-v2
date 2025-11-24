# 🚀 Guía Rápida de Inicio

## Inicio Rápido (Local)

```powershell
# 1. Instalar dependencias
pip install fastapi uvicorn torch transformers sentencepiece

# 2. Iniciar servidor
uvicorn app_simple:app --reload

# 3. Probar en el navegador
# http://localhost:8000/docs
```

## Con Docker

```powershell
docker build -f Dockerfile.simple -t translation-api .
docker run -p 8000:8000 translation-api
```

## Hostear en la Nube (GRATIS)

### Railway.app
1. Instala Railway CLI: `npm i -g @railway/cli`
2. `railway login`
3. `railway init`
4. `railway up`

### Render.com  
1. Conecta tu repositorio Git
2. Selecciona "Docker"
3. Dockerfile: `Dockerfile.simple`
4. Deploy automático ✅

### Fly.io
```powershell
# Instalar CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Deploy
fly launch
fly deploy
```

---

**Documentación completa:** Ver `README.md`
