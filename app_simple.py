"""
Servidor FastAPI ultra-ligero para servir modelo MarianMT
Optimizado para uso en móviles con mínima latencia
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Translation API",
    description="API de traducción optimizada para móviles",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde móviles
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos globales
model = None
tokenizer = None

class TranslationRequest(BaseModel):
    text: str
    max_length: int = 128  # Reducido para móviles
    
class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str = "en"
    target_language: str = "es"

def load_models(model_dir: str = "."):
    """Carga el modelo y tokenizer optimizado"""
    global model, tokenizer
    
    logger.info(f"Cargando modelo desde {model_dir}...")
    
    # Cargar modelo y tokenizer
    tokenizer = MarianTokenizer.from_pretrained(model_dir)
    model = MarianMTModel.from_pretrained(model_dir)
    
    # Optimizaciones para móviles
    model.eval()  # Modo evaluación
    torch.set_num_threads(2)  # Limitar threads
    
    # Opcional: Usar half precision para reducir memoria (solo en GPU)
    # if torch.cuda.is_available():
    #     model = model.half().cuda()
    
    logger.info("✅ Modelo cargado exitosamente")
    logger.info(f"   Parámetros: ~{sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")

def translate_text(text: str, max_length: int = 128) -> str:
    """
    Traduce texto usando el modelo MarianMT
    """
    # Tokenizar input
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    
    # Generar traducción con optimizaciones
    with torch.no_grad():
        translated = model.generate(
            **inputs,
            max_length=max_length,
            num_beams=2,  # Reducido de 4 para mayor velocidad
            early_stopping=True,
            do_sample=False  # Greedy decoding para consistencia
        )
    
    # Decodificar
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

@app.on_event("startup")
async def startup_event():
    """Cargar modelo al iniciar el servidor"""
    try:
        load_models()
    except Exception as e:
        logger.error(f"Error cargando modelo: {e}")
        raise

@app.get("/")
async def root():
    """Endpoint de salud"""
    return {
        "status": "online",
        "message": "Translation API is running",
        "model": "MarianMT en->es",
        "optimized_for": "mobile"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "models_loaded": model is not None
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Endpoint de traducción
    
    - **text**: Texto a traducir (inglés -> español)
    - **max_length**: Longitud máxima de la traducción (default: 128)
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    try:
        translated = translate_text(request.text, request.max_length)
        return TranslationResponse(
            translated_text=translated,
            source_language="en",
            target_language="es"
        )
    except Exception as e:
        logger.error(f"Error en traducción: {e}")
        raise HTTPException(status_code=500, detail=f"Error en traducción: {str(e)}")

@app.post("/translate/batch")
async def translate_batch(texts: list[str], max_length: int = 128):
    """
    Endpoint de traducción por lotes
    Optimizado para procesar múltiples textos de una vez
    """
    if not texts:
        raise HTTPException(status_code=400, detail="La lista de textos no puede estar vacía")
    
    try:
        # Filtrar textos vacíos
        valid_texts = [t for t in texts if t.strip()]
        
        if not valid_texts:
            raise HTTPException(status_code=400, detail="Todos los textos están vacíos")
        
        # Traducir por lotes para mayor eficiencia
        inputs = tokenizer(valid_texts, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        
        with torch.no_grad():
            translated = model.generate(
                **inputs,
                max_length=max_length,
                num_beams=2,
                early_stopping=True,
                do_sample=False
            )
        
        # Decodificar todos los resultados
        results = []
        for i, text in enumerate(valid_texts):
            translated_text = tokenizer.decode(translated[i], skip_special_tokens=True)
            results.append({
                "original": text,
                "translated": translated_text
            })
        
        return {"translations": results, "count": len(results)}
    
    except Exception as e:
        logger.error(f"Error en traducción por lotes: {e}")
        raise HTTPException(status_code=500, detail=f"Error en traducción: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
