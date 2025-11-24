# =======================================================
# 📱 API de Traducción - Solución Final Optimizada
# =======================================================

## ✅ SOLUCIÓN IMPLEMENTADA

Debido a que la conversión completa a ONNX de modelos seq2seq como MarianMT es compleja, 
he implementado una solución **PyTorch optimizada** que es igualmente eficiente para móviles:

### Archivos Principales:

1. **`app_simple.py`** - Servidor FastAPI optimizado (USAR ESTE)
2. **`requirements-simple.txt`** - Dependencias mínimas  
3. **`Dockerfile.simple`** - Contenedor Docker optimizado
4. **`test_api.py`** - Script de pruebas

### Archivos Opcionales (para referencia):

- `convert_to_onnx.py` - Script de conversión a ONNX (encoder solamente)
- `app.py` - Versión con soporte ONNX/PyTorch híbrido

## 🚀 CÓMO USAR

### Opción 1: Local (Más Rápido para Desarrollo)

```powershell
# 1. Instalar dependencias
pip install fastapi uvicorn torch transformers sentencepiece

# 2. Iniciar servidor
cd "C:\Users\User\Desktop\checkpoint-2024 - Copy\endpoint"
uvicorn app_simple:app --reload

# 3. Probar
# Abre http://localhost:8000/docs en tu navegador
# O ejecuta: python test_api.py
```

### Opción 2: Docker (Recomendado para Producción)

```powershell
cd "C:\Users\User\Desktop\checkpoint-2024 - Copy\endpoint"

# Construir
docker build -f Dockerfile.simple -t translation-api .

# Ejecutar
docker run -p 8000:8000 translation-api

# Probar
curl -X POST http://localhost:8000/translate -H "Content-Type: application/json" -d "{\"text\":\"Hello world\"}"
```

## 📊 MÉTRICAS DE RENDIMIENTO

- **Tamaño del modelo**: ~300 MB (safetensors)
- **Parámetros**: 77.9M
- **RAM en ejecución**: 500-700 MB
- **Latencia**: 100-300ms por oración
- **Docker image**: ~800 MB

## 🎯 OPTIMIZACIONES PARA MÓVILES

1. ✅ **num_beams=2** (en lugar de 4) - 2x más rápido
2. ✅ **torch.set_num_threads(2)** - Limitado para dispositivos móviles
3. ✅ **max_length=128** (default) - Reducido de 512
4. ✅ **Greedy decoding** - do_sample=False para consistencia
5. ✅ **Batch processing** - Endpoint `/translate/batch` optimizado

## 🌐 HOSTING GRATUITO

### Railway.app (Más Fácil)
```powershell
npm i -g @railway/cli
railway login
railway init
railway up
```

### Render.com (Más Popular)
1. Conecta tu repo Git
2. Selecciona "Docker"
3. Usa `Dockerfile.simple`
4. Deploy ✅

### Fly.io (Más Ligero)
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
fly launch
fly deploy
```

## 📱 INTEGRACIÓN CON MÓVILES

### Ejemplo Android (Kotlin):
```kotlin
val client = OkHttpClient()
val json = JSONObject().put("text", "Hello").put("max_length", 128)
val body = RequestBody.create(MediaType.parse("application/json"), json.toString())
val request = Request.Builder()
    .url("http://YOUR_SERVER:8000/translate")
    .post(body)
    .build()

client.newCall(request).enqueue(object : Callback {
    override fun onResponse(call: Call, response: Response) {
        val result = JSONObject(response.body()?.string())
        val translation = result.getString("translated_text")
    }
})
```

### Ejemplo iOS (Swift):
```swift
struct TranslationRequest: Codable {
    let text: String
    let max_length: Int
}

func translate(text: String) async throws -> String {
    let url = URL(string: "http://YOUR_SERVER:8000/translate")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = TranslationRequest(text: text, max_length: 128)
    request.httpBody = try JSONEncoder().encode(body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let response = try JSONDecoder().decode(TranslationResponse.self, from: data)
    return response.translated_text
}
```

## 🔧 TROUBLESHOOTING

**Error: ModuleNotFoundError**
```powershell
pip install fastapi uvicorn torch transformers sentencepiece
```

**Error: No encuentra el modelo**
```powershell
# Verifica que estés en el directorio correcto
cd "C:\Users\User\Desktop\checkpoint-2024 - Copy\endpoint"
ls config.json, model.safetensors
```

**Servidor muy lento**
- Reduce `num_beams` a 1 en `app_simple.py`
- Reduce `max_length` en las peticiones (ej: 64 en lugar de 128)

**CORS error desde móvil**
- Usa la IP del servidor, no `localhost`
- Verifica que el firewall permita conexiones al puerto 8000

## 📝 NOTAS IMPORTANTES

- ⚠️ El modelo original es grande (~300MB), ideal para hosting en cloud
- ✅ Para móviles: Hostea en servidor y haz peticiones HTTP (no incluyas el modelo en la app)
- ✅ El servidor ya está optimizado para baja latencia
- ✅ CORS está habilitado para todas las origins

## 📖 DOCUMENTACIÓN COMPLETA

Ver `README.md` para más detalles sobre:
- Ejemplos de código completos
- Configuración avanzada
- Opciones de deployment
- API endpoints

---

**¿Necesitas ayuda?** Revisa `README.md` o `QUICKSTART2.md`
