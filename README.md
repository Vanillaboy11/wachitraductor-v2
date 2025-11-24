# 📱 API de Traducción Optimizada para Móviles

Servidor de traducción ultra-ligero usando PyTorch optimizado, diseñado para aplicaciones móviles.

## 🚀 Características

- ✅ Modelo MarianMT (inglés → español) optimizado
- ✅ API REST ligera con FastAPI
- ✅ Optimizado para baja latencia (2 threads, num_beams=2)
- ✅ Docker containerizado (~800 MB)
- ✅ CORS habilitado para móviles
- ✅ Procesamiento por lotes eficiente

## 📦 Instalación

### Opción Rápida: Usar el servidor simple (Recomendado)

```powershell
# Instalar dependencias
pip install -r requirements-simple.txt

# Iniciar servidor
uvicorn app_simple:app --host 0.0.0.0 --port 8000
```

### Con Docker (Recomendado para producción)

```powershell
# Construir imagen
docker build -f Dockerfile.simple -t translation-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 translation-api

# O con docker-compose
docker-compose up -d
```

## 🔌 Uso de la API

### Endpoint principal: Traducir texto

```bash
POST http://localhost:8000/translate
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "max_length": 512
}
```

Respuesta:
```json
{
  "translated_text": "Hola, ¿cómo estás?",
  "source_language": "en",
  "target_language": "es"
}
```

### Traducción por lotes

```bash
POST http://localhost:8000/translate/batch?max_length=512
Content-Type: application/json

["Hello world", "Good morning", "Thank you"]
```

### Health check

```bash
GET http://localhost:8000/health
```

### Documentación interactiva

Una vez iniciado el servidor, visita:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📱 Integración con móviles

### Android (Kotlin/Java)

```kotlin
import okhttp3.*
import org.json.JSONObject

val client = OkHttpClient()
val url = "http://YOUR_SERVER:8000/translate"

val json = JSONObject().apply {
    put("text", "Hello world")
    put("max_length", 512)
}

val body = RequestBody.create(
    MediaType.parse("application/json"),
    json.toString()
)

val request = Request.Builder()
    .url(url)
    .post(body)
    .build()

client.newCall(request).enqueue(object : Callback {
    override fun onResponse(call: Call, response: Response) {
        val result = JSONObject(response.body()?.string())
        val translation = result.getString("translated_text")
        // Usar traducción
    }
})
```

### iOS (Swift)

```swift
import Foundation

struct TranslationRequest: Codable {
    let text: String
    let max_length: Int
}

struct TranslationResponse: Codable {
    let translated_text: String
    let source_language: String
    let target_language: String
}

func translate(text: String) async throws -> String {
    let url = URL(string: "http://YOUR_SERVER:8000/translate")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = TranslationRequest(text: text, max_length: 512)
    request.httpBody = try JSONEncoder().encode(body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let response = try JSONDecoder().decode(TranslationResponse.self, from: data)
    
    return response.translated_text
}
```

### React Native / Flutter

```javascript
// React Native
async function translate(text) {
  const response = await fetch('http://YOUR_SERVER:8000/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      max_length: 512
    })
  });
  
  const result = await response.json();
  return result.translated_text;
}
```

## 🎯 Optimizaciones para Producción

### 1. Hosting en la nube

**Railway.app** (gratuito para empezar):
```powershell
# Instalar Railway CLI
npm i -g @railway/cli

# Desplegar
railway login
railway init
railway up
```

**Fly.io** (muy ligero):
```powershell
# Instalar Fly CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Desplegar
fly launch
fly deploy
```

**Render.com** (fácil):
- Conecta tu repositorio Git
- Selecciona "Docker"
- Despliega automáticamente

### 2. Optimizaciones adicionales

```python
# En app.py, puedes agregar caché:
from functools import lru_cache

@lru_cache(maxsize=1000)
def translate_text_cached(text: str, max_length: int = 512):
    return translate_text(text, max_length)
```

### 3. Reducir latencia

- Usar modelos cuantizados (`use_quantized=True`)
- Limitar `max_length` según tus necesidades
- Usar un CDN/proxy cerca de tus usuarios
- Implementar caché de traducciones comunes

## 📊 Tamaños aproximados

- Modelo original (safetensors): ~300 MB
- Docker image: ~800 MB
- Memoria RAM en ejecución: ~500-700 MB
- Latencia promedio: 100-300ms por oración

## 🎯 Optimizaciones Implementadas

1. **Reducción de beams**: `num_beams=2` (vs 4) para 2x más rápido
2. **Threads limitados**: `torch.set_num_threads(2)` para móviles
3. **Greedy decoding**: `do_sample=False` para mayor velocidad
4. **Max length reducido**: 128 tokens por defecto (ajustable)
5. **Procesamiento por lotes**: endpoint `/translate/batch` optimizado

## 🔧 Troubleshooting

### No encuentra el modelo
Asegúrate de estar en el directorio `endpoint` y que los archivos del modelo estén presentes:
```powershell
ls config.json, model.safetensors, tokenizer_config.json
```

### Memoria insuficiente
Reduce `max_length` en las peticiones o ajusta `num_beams=1` en `app_simple.py`

### Error en móviles: CORS
El servidor ya tiene CORS habilitado. Si aún tienes problemas, verifica que estés usando la URL correcta (no `localhost` desde móvil, usa la IP de tu servidor).

## 📝 Licencia

Este proyecto usa el modelo MarianMT de Hugging Face, sujeto a sus licencias respectivas.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o pull request.

---

**¿Necesitas ayuda?** Abre un issue en el repositorio.
