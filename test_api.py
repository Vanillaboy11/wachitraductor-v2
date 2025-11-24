"""
Script para probar la API de traducción
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test del endpoint de salud"""
    print("🔍 Probando health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_single_translation():
    """Test de traducción única"""
    print("🔍 Probando traducción única...")
    
    data = {
        "text": "Hello, how are you today?",
        "max_length": 512
    }
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/translate", json=data)
    elapsed = time.time() - start
    
    print(f"Status: {response.status_code}")
    print(f"Tiempo: {elapsed:.2f}s")
    result = response.json()
    print(f"Original: {data['text']}")
    print(f"Traducido: {result['translated_text']}\n")

def test_batch_translation():
    """Test de traducción por lotes"""
    print("🔍 Probando traducción por lotes...")
    
    texts = [
        "Hello world",
        "Good morning",
        "Thank you very much",
        "How are you?",
        "I love programming"
    ]
    
    start = time.time()
    response = requests.post(
        f"{BASE_URL}/translate/batch",
        params={"max_length": 512},
        json=texts
    )
    elapsed = time.time() - start
    
    print(f"Status: {response.status_code}")
    print(f"Tiempo total: {elapsed:.2f}s")
    print(f"Tiempo promedio: {elapsed/len(texts):.2f}s por texto")
    
    result = response.json()
    print(f"\nTraducciones ({result['count']}):")
    for item in result['translations']:
        print(f"  '{item['original']}' → '{item['translated']}'")
    print()

def test_long_text():
    """Test con texto largo"""
    print("🔍 Probando con texto largo...")
    
    long_text = """
    Machine learning is a subset of artificial intelligence that focuses on 
    the development of algorithms and statistical models that enable computers 
    to improve their performance on a specific task through experience.
    """
    
    data = {
        "text": long_text.strip(),
        "max_length": 512
    }
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/translate", json=data)
    elapsed = time.time() - start
    
    print(f"Status: {response.status_code}")
    print(f"Tiempo: {elapsed:.2f}s")
    result = response.json()
    print(f"Original ({len(long_text)} chars):")
    print(f"  {data['text'][:100]}...")
    print(f"Traducido ({len(result['translated_text'])} chars):")
    print(f"  {result['translated_text']}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Pruebas de API de Traducción")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_single_translation()
        test_batch_translation()
        test_long_text()
        
        print("=" * 60)
        print("✅ Todas las pruebas completadas")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose en", BASE_URL)
    except Exception as e:
        print(f"❌ Error: {e}")
