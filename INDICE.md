# 📋 Índice de Archivos del Proyecto

## 🎯 ARCHIVOS PRINCIPALES (Usar estos)

### Para Desarrollo y Deployment
- **`app_simple.py`** ⭐ - Servidor FastAPI optimizado para móviles
- **`requirements-simple.txt`** - Dependencias mínimas necesarias
- **`Dockerfile.simple`** - Contenedor Docker optimizado
- **`docker-compose.yml`** - Orquestación de contenedores

### Para Testing
- **`test_model_quick.py`** - Prueba rápida del modelo (sin servidor)
- **`test_api.py`** - Pruebas completas del API REST

## 📚 DOCUMENTACIÓN (Leer en este orden)

1. **`LEEME_PRIMERO.md`** ⭐⭐⭐ - **EMPEZAR AQUÍ** - Resumen ejecutivo
2. **`SOLUCION_FINAL.md`** ⭐⭐ - Guía completa de la solución
3. **`EJEMPLOS_MOVILES.md`** ⭐ - Código de integración para Android/iOS/React Native/Flutter
4. **`README.md`** - Documentación técnica detallada
5. **`QUICKSTART2.md`** - Inicio rápido alternativo

## 🔧 ARCHIVOS DE CONFIGURACIÓN

- **`requirements.txt`** - Dependencias completas (incluye ONNX)
- **`requirements-server.txt`** - Dependencias para servidor con ONNX
- **`.gitignore`** - Archivos a ignorar en Git

## 📦 ARCHIVOS DEL MODELO (Ya existentes)

Estos archivos ya están en tu carpeta y son necesarios:
- `config.json` - Configuración del modelo
- `generation_config.json` - Configuración de generación
- `model.safetensors` - Pesos del modelo (~300MB)
- `source.spm` - Tokenizer source (inglés)
- `target.spm` - Tokenizer target (español)
- `tokenizer_config.json` - Configuración del tokenizer
- `special_tokens_map.json` - Tokens especiales
- `vocab.json` - Vocabulario

## 🐳 DOCKER (Múltiples opciones)

- **`Dockerfile.simple`** ⭐ - USAR ESTE (más simple, PyTorch)
- `Dockerfile` - Versión estándar
- `Dockerfile.alpine` - Versión ultra-ligera Alpine
- `docker-compose.yml` - Configuración de compose

## 🧪 ARCHIVOS EXPERIMENTALES (Referencia)

Estos archivos son para referencia o desarrollo avanzado:

- `convert_to_onnx.py` - Script de conversión a ONNX (solo encoder)
- `app.py` - Versión con soporte ONNX/PyTorch híbrido
- `setup.ps1` - Script de setup automatizado para Windows
- `install_dependencies.bat` - Instalador de dependencias (batch)

## 📊 ESTRUCTURA RECOMENDADA

```
endpoint/
├── 📄 LEEME_PRIMERO.md          ← EMPEZAR AQUÍ
├── 📄 SOLUCION_FINAL.md          ← Guía completa
├── 📄 EJEMPLOS_MOVILES.md        ← Integración móviles
├── 
├── 🚀 app_simple.py              ← Servidor principal
├── 📋 requirements-simple.txt    ← Dependencias
├── 🐳 Dockerfile.simple          ← Docker
├── 
├── 🧪 test_model_quick.py        ← Prueba rápida
├── 🧪 test_api.py                ← Pruebas API
├── 
├── 🤖 model.safetensors          ← Modelo
├── ⚙️  config.json               ← Configuración
└── 📚 [otros archivos de modelo]
```

## 🎯 FLUJO DE TRABAJO RECOMENDADO

### 1. Primera Vez
```
LEEME_PRIMERO.md
    ↓
Instalar dependencias
    ↓
Probar: python test_model_quick.py
    ↓
Iniciar servidor: uvicorn app_simple:app --reload
    ↓
Probar: http://localhost:8000/docs
```

### 2. Deployment
```
SOLUCION_FINAL.md (sección Hosting)
    ↓
Elegir plataforma (Render/Railway/Fly.io)
    ↓
Usar Dockerfile.simple
    ↓
Deploy y obtener URL
```

### 3. Integración Móvil
```
EJEMPLOS_MOVILES.md
    ↓
Copiar código para tu plataforma
    ↓
Reemplazar YOUR_API_URL
    ↓
Probar en app
```

## 🗂️ ARCHIVOS POR CASO DE USO

### Solo quiero probar el modelo
- `test_model_quick.py`
- Instalar: `pip install torch transformers sentencepiece`

### Quiero un servidor local
- `app_simple.py`
- `requirements-simple.txt`
- Instalar: `pip install -r requirements-simple.txt`
- Ejecutar: `uvicorn app_simple:app --reload`

### Quiero deployar con Docker
- `Dockerfile.simple`
- `docker-compose.yml`
- Construir: `docker build -f Dockerfile.simple -t translation-api .`
- Ejecutar: `docker run -p 8000:8000 translation-api`

### Quiero integrar en móvil
- `EJEMPLOS_MOVILES.md` (tiene código para todas las plataformas)
- Primero necesitas hostear el API (ver caso anterior)

### Quiero experimentar con ONNX
- `convert_to_onnx.py`
- `app.py`
- `requirements.txt`
- Nota: La conversión completa no está funcionando, solo encoder

## 📌 NOTAS IMPORTANTES

1. **NO USES** los archivos en `checkpoint-2024/` - son archivos de entrenamiento
2. **USA** los archivos en la raíz de `endpoint/`
3. **PRIORIDAD**: `app_simple.py` > `app.py` (más simple y funciona mejor)
4. **DOCKER**: `Dockerfile.simple` > otros Dockerfiles

## ❓ FAQ

**¿Qué archivo ejecutar primero?**
→ `test_model_quick.py` para verificar que el modelo funciona

**¿Qué servidor usar?**
→ `app_simple.py` (es el más simple y estable)

**¿Qué Dockerfile usar?**
→ `Dockerfile.simple` (es el más probado)

**¿Dónde está el código para móviles?**
→ `EJEMPLOS_MOVILES.md` tiene código completo para Android/iOS/React Native/Flutter

**¿Cómo hostear gratis?**
→ Ver `SOLUCION_FINAL.md` sección "Hosting Gratuito"

---

**Guía de inicio rápido**: Ver `LEEME_PRIMERO.md`
