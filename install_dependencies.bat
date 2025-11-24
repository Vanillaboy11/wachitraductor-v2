@echo off
echo ====================================
echo Instalando dependencias necesarias
echo ====================================
echo.

echo Instalando PyTorch, Transformers y ONNX...
pip install torch transformers onnx onnxruntime sentencepiece protobuf

echo.
echo ====================================
echo Instalacion completada!
echo ====================================
echo.
echo Ahora puedes ejecutar:
echo   python convert_to_onnx.py
echo.
pause
