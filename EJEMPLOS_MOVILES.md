# 📱 Ejemplos de Integración con Móviles

## 🔧 Configuración Inicial

Una vez que hayas hosteado tu API (ver LEEME_PRIMERO.md), tendrás una URL como:
- Local: `http://localhost:8000`
- Render: `https://translation-api-xxxx.onrender.com`
- Railway: `https://translation-api-production.up.railway.app`
- Fly.io: `https://translation-api.fly.dev`

Reemplaza `YOUR_API_URL` en los ejemplos con tu URL.

---

## 📱 Android (Kotlin)

### 1. Agregar dependencia en `build.gradle`:
```gradle
dependencies {
    implementation 'com.squareup.okhttp3:okhttp:4.11.0'
    implementation 'org.json:json:20230227'
}
```

### 2. Clase de Traducción:
```kotlin
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class TranslationService {
    private val client = OkHttpClient()
    private val apiUrl = "YOUR_API_URL/translate"
    private val JSON = "application/json; charset=utf-8".toMediaType()
    
    suspend fun translate(text: String, maxLength: Int = 128): String {
        return withContext(Dispatchers.IO) {
            val json = JSONObject().apply {
                put("text", text)
                put("max_length", maxLength)
            }
            
            val body = json.toString().toRequestBody(JSON)
            val request = Request.Builder()
                .url(apiUrl)
                .post(body)
                .build()
            
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    throw Exception("Error: ${response.code}")
                }
                
                val responseBody = response.body?.string()
                val result = JSONObject(responseBody)
                result.getString("translated_text")
            }
        }
    }
}
```

### 3. Uso en Activity/Fragment:
```kotlin
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private val translationService = TranslationService()
    
    fun translateText(text: String) {
        lifecycleScope.launch {
            try {
                val translation = translationService.translate(text)
                // Actualizar UI con la traducción
                textViewResult.text = translation
            } catch (e: Exception) {
                // Manejar error
                Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
```

### 4. Permisos en `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

## 🍎 iOS (Swift)

### 1. Modelo de Datos:
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
```

### 2. Servicio de Traducción:
```swift
class TranslationService {
    private let apiURL = "YOUR_API_URL/translate"
    
    func translate(_ text: String, maxLength: Int = 128) async throws -> String {
        guard let url = URL(string: apiURL) else {
            throw TranslationError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = TranslationRequest(text: text, max_length: maxLength)
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw TranslationError.serverError
        }
        
        let result = try JSONDecoder().decode(TranslationResponse.self, from: data)
        return result.translated_text
    }
}

enum TranslationError: Error {
    case invalidURL
    case serverError
}
```

### 3. Uso en SwiftUI:
```swift
import SwiftUI

struct ContentView: View {
    @State private var inputText = ""
    @State private var translatedText = ""
    @State private var isTranslating = false
    
    private let translationService = TranslationService()
    
    var body: some View {
        VStack(spacing: 20) {
            TextField("Enter text in English", text: $inputText)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            Button("Translate") {
                Task {
                    await translateText()
                }
            }
            .disabled(isTranslating || inputText.isEmpty)
            
            if isTranslating {
                ProgressView()
            } else if !translatedText.isEmpty {
                Text(translatedText)
                    .padding()
            }
        }
        .padding()
    }
    
    func translateText() async {
        isTranslating = true
        defer { isTranslating = false }
        
        do {
            translatedText = try await translationService.translate(inputText)
        } catch {
            translatedText = "Error: \(error.localizedDescription)"
        }
    }
}
```

---

## ⚛️ React Native

### 1. Instalación:
```bash
npm install axios
```

### 2. Servicio de Traducción:
```javascript
import axios from 'axios';

const API_URL = 'YOUR_API_URL';

export const translateText = async (text, maxLength = 128) => {
  try {
    const response = await axios.post(`${API_URL}/translate`, {
      text: text,
      max_length: maxLength
    });
    
    return response.data.translated_text;
  } catch (error) {
    console.error('Translation error:', error);
    throw error;
  }
};

export const translateBatch = async (texts, maxLength = 128) => {
  try {
    const response = await axios.post(`${API_URL}/translate/batch`, texts, {
      params: { max_length: maxLength }
    });
    
    return response.data.translations;
  } catch (error) {
    console.error('Batch translation error:', error);
    throw error;
  }
};
```

### 3. Componente React:
```javascript
import React, { useState } from 'react';
import { View, TextInput, Button, Text, ActivityIndicator } from 'react-native';
import { translateText } from './translationService';

const TranslationScreen = () => {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;
    
    setIsTranslating(true);
    try {
      const translation = await translateText(inputText);
      setTranslatedText(translation);
    } catch (error) {
      setTranslatedText('Error: ' + error.message);
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput
        placeholder="Enter text in English"
        value={inputText}
        onChangeText={setInputText}
        style={{ borderWidth: 1, padding: 10, marginBottom: 10 }}
      />
      
      <Button 
        title="Translate" 
        onPress={handleTranslate}
        disabled={isTranslating || !inputText.trim()}
      />
      
      {isTranslating && <ActivityIndicator style={{ marginTop: 20 }} />}
      
      {!isTranslating && translatedText && (
        <Text style={{ marginTop: 20, fontSize: 16 }}>
          {translatedText}
        </Text>
      )}
    </View>
  );
};

export default TranslationScreen;
```

---

## 🎯 Flutter (Dart)

### 1. Agregar dependencia en `pubspec.yaml`:
```yaml
dependencies:
  http: ^1.1.0
```

### 2. Modelo de Datos:
```dart
class TranslationRequest {
  final String text;
  final int maxLength;

  TranslationRequest({required this.text, this.maxLength = 128});

  Map<String, dynamic> toJson() => {
    'text': text,
    'max_length': maxLength,
  };
}

class TranslationResponse {
  final String translatedText;
  final String sourceLanguage;
  final String targetLanguage;

  TranslationResponse({
    required this.translatedText,
    required this.sourceLanguage,
    required this.targetLanguage,
  });

  factory TranslationResponse.fromJson(Map<String, dynamic> json) {
    return TranslationResponse(
      translatedText: json['translated_text'],
      sourceLanguage: json['source_language'],
      targetLanguage: json['target_language'],
    );
  }
}
```

### 3. Servicio de Traducción:
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class TranslationService {
  static const String apiUrl = 'YOUR_API_URL';

  Future<String> translate(String text, {int maxLength = 128}) async {
    try {
      final request = TranslationRequest(text: text, maxLength: maxLength);
      
      final response = await http.post(
        Uri.parse('$apiUrl/translate'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        final translationResponse = TranslationResponse.fromJson(
          json.decode(response.body)
        );
        return translationResponse.translatedText;
      } else {
        throw Exception('Translation failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error translating text: $e');
    }
  }
}
```

### 4. Widget Flutter:
```dart
import 'package:flutter/material.dart';

class TranslationScreen extends StatefulWidget {
  @override
  _TranslationScreenState createState() => _TranslationScreenState();
}

class _TranslationScreenState extends State<TranslationScreen> {
  final TextEditingController _controller = TextEditingController();
  final TranslationService _service = TranslationService();
  
  String _translatedText = '';
  bool _isTranslating = false;

  void _translate() async {
    if (_controller.text.isEmpty) return;
    
    setState(() {
      _isTranslating = true;
      _translatedText = '';
    });

    try {
      final translation = await _service.translate(_controller.text);
      setState(() {
        _translatedText = translation;
      });
    } catch (e) {
      setState(() {
        _translatedText = 'Error: $e';
      });
    } finally {
      setState(() {
        _isTranslating = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Translation')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: 'Enter text in English',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isTranslating ? null : _translate,
              child: Text('Translate'),
            ),
            SizedBox(height: 16),
            if (_isTranslating)
              CircularProgressIndicator()
            else if (_translatedText.isNotEmpty)
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _translatedText,
                  style: TextStyle(fontSize: 16),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
```

---

## 🌐 JavaScript Puro (Web)

```javascript
async function translate(text, maxLength = 128) {
  const response = await fetch('YOUR_API_URL/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      max_length: maxLength
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.translated_text;
}

// Uso
document.getElementById('translateBtn').addEventListener('click', async () => {
  const inputText = document.getElementById('inputText').value;
  const resultDiv = document.getElementById('result');
  
  try {
    resultDiv.textContent = 'Translating...';
    const translation = await translate(inputText);
    resultDiv.textContent = translation;
  } catch (error) {
    resultDiv.textContent = 'Error: ' + error.message;
  }
});
```

---

## 💡 CONSEJOS DE OPTIMIZACIÓN

### 1. Caché Local
```javascript
// React Native / JavaScript
const translationCache = new Map();

async function translateWithCache(text) {
  if (translationCache.has(text)) {
    return translationCache.get(text);
  }
  
  const translation = await translateText(text);
  translationCache.set(text, translation);
  return translation;
}
```

### 2. Debouncing (para inputs en tiempo real)
```javascript
import { debounce } from 'lodash';

const debouncedTranslate = debounce(async (text) => {
  const translation = await translateText(text);
  setTranslation(translation);
}, 500); // Espera 500ms después de que el usuario deje de escribir
```

### 3. Manejo de Errores Robusto
```javascript
async function translateWithRetry(text, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await translateText(text);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

---

## 🎯 TESTING

### Probar tu API desde la terminal:

```powershell
# Windows PowerShell
$body = @{
    text = "Hello world"
    max_length = 128
} | ConvertTo-Json

Invoke-RestMethod -Uri "YOUR_API_URL/translate" -Method Post -Body $body -ContentType "application/json"
```

```bash
# macOS/Linux
curl -X POST "YOUR_API_URL/translate" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","max_length":128}'
```

---

**¿Necesitas más ayuda?** Revisa `LEEME_PRIMERO.md` para deployment en la nube.
