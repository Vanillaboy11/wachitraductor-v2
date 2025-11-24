# 🚀 Guía Rápida de Inicio

## Paso 1: Convertir a ONNX
```powershell
pip install -r requirements.txt
python convert_to_onnx.py
```

## Paso 2: Ejecutar servidor
```powershell
pip install -r requirements-server.txt
uvicorn app:app --reload
```

## Paso 3: Probar
```powershell
python test_api.py
```

O visita: http://localhost:8000/docs

---

**¿Quieres hostear en la nube?** Lee el README.md completo para opciones de Railway, Fly.io, y Render.
