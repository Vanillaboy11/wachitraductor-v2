#!/usr/bin/env python
import os
import sys

# Obtener el puerto de la variable de entorno
port = os.environ.get("PORT", "8000")

# Ejecutar uvicorn con el puerto correcto
os.execvp("uvicorn", ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", port, "--workers", "1"])
