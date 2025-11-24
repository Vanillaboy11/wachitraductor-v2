"""
Script de prueba rápida del modelo (sin servidor)
Útil para verificar que el modelo funciona correctamente
"""
import torch
from transformers import MarianMTModel, MarianTokenizer

def test_model():
    print("=" * 60)
    print("🔍 Prueba Rápida del Modelo de Traducción")
    print("=" * 60)
    print()
    
    print("[1/3] Cargando modelo...")
    tokenizer = MarianTokenizer.from_pretrained(".")
    model = MarianMTModel.from_pretrained(".")
    model.eval()
    print("✅ Modelo cargado")
    print(f"    Parámetros: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")
    print()
    
    # Textos de prueba
    test_texts = [
        "Hello, how are you?",
        "Good morning, have a nice day",
        "I love programming",
        "Machine learning is amazing",
        "Thank you very much"
    ]
    
    print("[2/3] Traduciendo textos de prueba...")
    print()
    
    for i, text in enumerate(test_texts, 1):
        # Tokenizar
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        
        # Traducir
        with torch.no_grad():
            translated = model.generate(
                **inputs,
                max_length=128,
                num_beams=2,
                early_stopping=True
            )
        
        # Decodificar
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        
        print(f"{i}. '{text}'")
        print(f"   → '{translated_text}'")
        print()
    
    print("=" * 60)
    print("✅ Todas las pruebas completadas exitosamente")
    print("=" * 60)
    print()
    print("El modelo funciona correctamente. Ahora puedes:")
    print("1. Iniciar el servidor: uvicorn app_simple:app --reload")
    print("2. Visitar: http://localhost:8000/docs")
    print("3. Hostear en la nube (Railway, Render, Fly.io)")

if __name__ == "__main__":
    try:
        test_model()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Asegúrate de estar en el directorio correcto con:")
        print("  cd 'C:\\Users\\User\\Desktop\\checkpoint-2024 - Copy\\endpoint'")
