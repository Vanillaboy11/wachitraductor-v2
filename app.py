"""
Servidor FastAPI ultra-ligero para servir modelos ONNX
Optimizado para uso en móviles con mínima latencia
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np
from transformers import MarianTokenizer, MarianMTModel
from pathlib import Path
import logging
import torch

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Translation API",
    description="API de traducción optimizada para móviles usando ONNX",
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
model_session = None
tokenizer = None
use_onnx = True

class TranslationRequest(BaseModel):
    text: str
    max_length: int = 512
    
class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str = "en"
    target_language: str = "es"

def load_models(model_dir: str = "./onnx_models", use_quantized: bool = True, fallback_to_pytorch: bool = True):
    """Carga los modelos ONNX y el tokenizer"""
    global model_session, tokenizer, use_onnx
    
    model_path = Path(model_dir)
    
    # Determinar qué modelo usar
    if use_quantized:
        model_file = "model_quantized.onnx"
    else:
        model_file = "model.onnx"
    
    onnx_model_path = model_path / model_file
    
    try:
        logger.info(f"Intentando cargar modelo ONNX desde {onnx_model_path}")
        
        # Configurar opciones de sesión para optimización
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.intra_op_num_threads = 2  # Limitar threads para móviles
        
        # Cargar modelo ONNX
        model_session = ort.InferenceSession(str(onnx_model_path), sess_options)
        use_onnx = True
        
        logger.info("✅ Modelo ONNX cargado exitosamente")
        
    except Exception as e:
        if fallback_to_pytorch:
            logger.warning(f"No se pudo cargar modelo ONNX: {e}")
            logger.info("Usando modelo PyTorch como fallback...")
            
            # Cargar tokenizer desde el directorio padre
            tokenizer_path = model_path.parent if model_path.name == "onnx_models" else model_path
            
            # Cargar modelo PyTorch
            model_session = MarianMTModel.from_pretrained(str(tokenizer_path))
            model_session.eval()
            use_onnx = False
            
            logger.info("✅ Modelo PyTorch cargado exitosamente")
        else:
            raise
    
    # Cargar tokenizer
    tokenizer_path = model_path.parent if model_path.name == "onnx_models" else model_path
    tokenizer = MarianTokenizer.from_pretrained(str(tokenizer_path))
    
    logger.info(f"✅ Tokenizer cargado desde {tokenizer_path}")

def translate_text(text: str, max_length: int = 512) -> str:
    """
    Traduce texto usando ONNX o PyTorch
    """
    if use_onnx:
        # Usar modelo ONNX
        inputs = tokenizer(text, return_tensors="np", padding=True, truncation=True, max_length=max_length)
        
        # Ejecutar modelo ONNX
        outputs = model_session.run(
            None,
            {
                "input_ids": inputs["input_ids"].astype(np.int64),
                "attention_mask": inputs["attention_mask"].astype(np.int64)
            }
        )
        
        # El output es una tupla, tomar el primer elemento (logits)
        output_ids = outputs[0]
        
        # Decodificar - tomar el token con mayor probabilidad para cada posición
        if len(output_ids.shape) == 3:  # (batch, seq, vocab)
            predicted_ids = np.argmax(output_ids[0], axis=-1)
        else:
            predicted_ids = output_ids[0]
        
        translated_text = tokenizer.decode(predicted_ids, skip_special_tokens=True)
        
    else:
        # Usar modelo PyTorch
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        
        with torch.no_grad():
            outputs = model_session.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                early_stopping=True
            )
        
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return translated_text

@app.on_event("startup")
async def startup_event():
    """Cargar modelos al iniciar el servidor"""
    try:
        load_models(use_quantized=True, fallback_to_pytorch=True)
    except Exception as e:
        logger.error(f"Error cargando modelos: {e}")
        raise

@app.get("/")
async def root():
    """Endpoint de salud"""
    return {
        "status": "online",
        "message": "Translation API is running",
        "model": "MarianMT en->es",
        "optimized_for": "mobile",
        "using_onnx": use_onnx
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "models_loaded": model_session is not None,
        "using_onnx": use_onnx
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Endpoint de traducción
    
    - **text**: Texto a traducir (inglés -> español)
    - **max_length**: Longitud máxima de la traducción (default: 512)
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
async def translate_batch(texts: list[str], max_length: int = 512):
    """
    Endpoint de traducción por lotes
    """
    if not texts:
        raise HTTPException(status_code=400, detail="La lista de textos no puede estar vacía")
    
    try:
        results = []
        for text in texts:
            if text.strip():
                translated = translate_text(text, max_length)
                results.append({
                    "original": text,
                    "translated": translated
                })
        return {"translations": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Error en traducción por lotes: {e}")
        raise HTTPException(status_code=500, detail=f"Error en traducción: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
