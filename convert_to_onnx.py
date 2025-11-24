"""
Script para convertir el modelo MarianMT a ONNX optimizado para móviles
"""
import torch
from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType
import argparse

def convert_to_onnx(model_path, output_path, quantize=True):
    """
    Convierte el modelo a ONNX y lo optimiza para móviles
    
    Args:
        model_path: Ruta al modelo
        output_path: Ruta para guardar el modelo ONNX
        quantize: Si se debe cuantizar el modelo (recomendado para móviles)
    """
    print(f"Cargando modelo desde {model_path}...")
    model = MarianMTModel.from_pretrained(model_path)
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    
    # Poner modelo en modo evaluación
    model.eval()
    
    # Crear inputs de ejemplo
    sample_text = "Hello, how are you?"
    inputs = tokenizer(sample_text, return_tensors="pt", padding=True)
    
    # Preparar inputs para ONNX
    encoder_inputs = {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"]
    }
    
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Exportar encoder
    encoder_path = output_dir / "encoder_model.onnx"
    print(f"\nExportando encoder a {encoder_path}...")
    
    with torch.no_grad():
        torch.onnx.export(
            model.get_encoder(),
            (inputs["input_ids"], inputs["attention_mask"]),
            str(encoder_path),
            input_names=["input_ids", "attention_mask"],
            output_names=["last_hidden_state"],
            dynamic_axes={
                "input_ids": {0: "batch", 1: "sequence"},
                "attention_mask": {0: "batch", 1: "sequence"},
                "last_hidden_state": {0: "batch", 1: "sequence"}
            },
            opset_version=14,
            do_constant_folding=True
        )
    
    # Exportar modelo completo (encoder + decoder juntos es más simple)
    full_model_path = output_dir / "model.onnx"
    print(f"Exportando modelo completo a {full_model_path}...")
    
    # Crear inputs de ejemplo
    with torch.no_grad():
        torch.onnx.export(
            model,
            (inputs["input_ids"], inputs["attention_mask"]),
            str(full_model_path),
            input_names=["input_ids", "attention_mask"],
            output_names=["output"],
            dynamic_axes={
                "input_ids": {0: "batch", 1: "sequence"},
                "attention_mask": {0: "batch", 1: "sequence"},
                "output": {0: "batch", 1: "sequence"}
            },
            opset_version=14,
            do_constant_folding=True
        )
    
    print("\n✓ Modelo ONNX exportado exitosamente")
    
    # Cuantizar modelo para reducir tamaño (INT8)
    if quantize:
        print("\nCuantizando modelo para optimización móvil...")
        
        # Cuantizar encoder
        encoder_quant_path = output_dir / "encoder_model_quantized.onnx"
        quantize_dynamic(
            str(encoder_path),
            str(encoder_quant_path),
            weight_type=QuantType.QUInt8
        )
        print(f"✓ Encoder cuantizado: {encoder_quant_path}")
        
        # Cuantizar modelo completo
        full_model_quant_path = output_dir / "model_quantized.onnx"
        quantize_dynamic(
            str(full_model_path),
            str(full_model_quant_path),
            weight_type=QuantType.QUInt8
        )
        print(f"✓ Modelo completo cuantizado: {full_model_quant_path}")
        
        # Mostrar tamaños
        print("\n📊 Tamaños de archivos:")
        print(f"Encoder original: {encoder_path.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"Encoder cuantizado: {encoder_quant_path.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"Modelo completo original: {full_model_path.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"Modelo completo cuantizado: {full_model_quant_path.stat().st_size / 1024 / 1024:.2f} MB")

    
    print(f"\n✅ Conversión completada! Archivos en: {output_dir}")
    return output_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convertir modelo MarianMT a ONNX")
    parser.add_argument("--model_path", type=str, default=".", help="Ruta al modelo")
    parser.add_argument("--output_path", type=str, default="./onnx_models", help="Ruta de salida")
    parser.add_argument("--no-quantize", action="store_true", help="No cuantizar modelos")
    
    args = parser.parse_args()
    
    convert_to_onnx(args.model_path, args.output_path, quantize=not args.no_quantize)
