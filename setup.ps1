# Script de instalación y conversión automatizada
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Setup y Conversión a ONNX" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "convert_to_onnx.py")) {
    Write-Host "Error: No se encuentra convert_to_onnx.py" -ForegroundColor Red
    Write-Host "Asegurate de ejecutar este script desde el directorio 'endpoint'" -ForegroundColor Red
    exit 1
}

# Paso 1: Instalar dependencias
Write-Host "[1/3] Instalando dependencias..." -ForegroundColor Yellow
pip install -q torch transformers onnx onnxruntime sentencepiece protobuf

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error instalando dependencias" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
Write-Host ""

# Paso 2: Convertir modelo a ONNX
Write-Host "[2/3] Convirtiendo modelo a ONNX..." -ForegroundColor Yellow
python convert_to_onnx.py --model_path . --output_path ./onnx_models

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error en la conversión" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Modelo convertido exitosamente" -ForegroundColor Green
Write-Host ""

# Paso 3: Mostrar siguiente paso
Write-Host "[3/3] Siguiente paso" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para iniciar el servidor:" -ForegroundColor Cyan
Write-Host "  pip install -r requirements-server.txt" -ForegroundColor White
Write-Host "  uvicorn app:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "O con Docker:" -ForegroundColor Cyan
Write-Host "  docker build -t translation-api ." -ForegroundColor White
Write-Host "  docker run -p 8000:8000 translation-api" -ForegroundColor White
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "Setup completado exitosamente!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
