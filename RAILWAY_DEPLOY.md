# 🚂 Desplegar en Railway - Guía Paso a Paso

## Opción 1: Desde GitHub (Recomendado - 5 minutos)

### Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Crea un nuevo repositorio (público o privado)
3. **NO** inicialices con README

### Paso 2: Subir tu Código

```powershell
# Navegar a tu carpeta
cd "C:\Users\User\Desktop\checkpoint-2024 - Copy\endpoint"

# Inicializar Git (si no lo has hecho)
git init

# Agregar archivos
git add .

# Hacer commit
git commit -m "Initial commit - Translation API"

# Conectar con GitHub (reemplaza TU-USUARIO y TU-REPO)
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git

# Subir código
git branch -M main
git push -u origin main
```

### Paso 3: Desplegar en Railway

1. Ve a https://railway.app
2. Click en **"Start a New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway para acceder a GitHub
5. Selecciona tu repositorio
6. Railway detectará automáticamente el `Dockerfile.simple`
7. Click **"Deploy"**

### Paso 4: Configurar Variables (Opcional)

En el dashboard de Railway:
- Click en tu proyecto
- Ve a la pestaña **"Variables"**
- Agrega si necesitas:
  - `TORCH_NUM_THREADS=2`
  - `MAX_LENGTH=128`

### Paso 5: Obtener tu URL

1. En el dashboard, ve a **"Settings"**
2. Sección **"Domains"**
3. Click **"Generate Domain"**
4. ¡Listo! Tu API estará en: `https://tu-proyecto.up.railway.app`

---

## Opción 2: Desde CLI de Railway (Más Rápido - 2 minutos)

### Paso 1: Instalar Railway CLI

```powershell
# Con npm (si tienes Node.js instalado)
npm i -g @railway/cli

# O descargar directamente desde:
# https://railway.app/cli
```

### Paso 2: Login y Deploy

```powershell
# Navegar a tu carpeta
cd "C:\Users\User\Desktop\checkpoint-2024 - Copy\endpoint"

# Login en Railway
railway login

# Inicializar proyecto
railway init

# Vincular o crear nuevo proyecto
# Selecciona "Create new project"

# Hacer deploy
railway up

# Agregar dominio público
railway domain
```

¡Eso es todo! En 2-3 minutos tu API estará online.

---

## Opción 3: Sin Git (Desde la Web)

1. Comprime tu carpeta `endpoint` en un ZIP
2. Ve a https://railway.app
3. Click **"Start a New Project"**
4. Selecciona **"Empty Project"**
5. Click en **"+ New"** → **"Service"**
6. Selecciona **"Docker Image"** o **"GitHub Repo"**
7. Sube tu código

---

## 🔍 Verificar Deployment

Una vez desplegado, prueba tu API:

```powershell
# Reemplaza TU-URL con tu URL de Railway
$body = @{
    text = "Hello world"
    max_length = 128
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://TU-URL.up.railway.app/translate" -Method Post -Body $body -ContentType "application/json"
```

O visita en el navegador:
```
https://TU-URL.up.railway.app/docs
```

---

## 📊 Monitoreo

En el dashboard de Railway podrás ver:
- **Logs** en tiempo real
- **Métricas** de uso (CPU, RAM)
- **Deploy history**
- **Variables de entorno**

---

## 💰 Costos

Railway ofrece:
- **$5 USD gratis** cada mes
- Después: ~$5-10 USD/mes dependiendo del uso
- Tu modelo (~500-700 MB RAM) debería caber en el plan gratuito

---

## 🐛 Troubleshooting

### Error: "Build failed"
1. Verifica que `Dockerfile.simple` esté en la raíz
2. Asegúrate de que todos los archivos del modelo estén subidos
3. Revisa los logs en Railway dashboard

### Error: "Out of memory"
1. El modelo es grande, puede tardar en cargar
2. Railway puede necesitar unos minutos para asignar recursos
3. Verifica los logs: debería decir "✅ Modelo cargado exitosamente"

### Error: "Application failed to start"
1. Verifica que la variable `PORT` esté configurada
2. Railway usa puerto dinámico, el `Dockerfile.simple` ya está configurado
3. Revisa los logs de inicio

### La API responde lento la primera vez
- Es normal: el modelo tarda en cargarse (~30-60 segundos)
- Las siguientes peticiones serán rápidas (100-300ms)

---

## 🎯 Próximos Pasos

Una vez desplegado:

1. **Copia tu URL** de Railway
2. **Úsala en tu app móvil** (ver `EJEMPLOS_MOVILES.md`)
3. **Prueba con Postman** o desde el navegador en `/docs`

Ejemplo de URL final:
```
https://translation-api-production.up.railway.app
```

Reemplaza `YOUR_API_URL` en todos los ejemplos de código con esta URL.

---

## 📝 Comandos Útiles de Railway CLI

```powershell
# Ver logs en vivo
railway logs

# Ver estado
railway status

# Abrir dashboard
railway open

# Ver variables
railway variables

# Agregar variable
railway variables set KEY=VALUE

# Conectar a shell del contenedor
railway shell

# Re-deploy
railway up
```

---

## 🔐 Seguridad (Opcional)

Si quieres agregar autenticación:

1. Agrega una API key en variables de Railway:
   ```
   API_KEY=tu_clave_secreta_aqui
   ```

2. Modifica `app_simple.py` para verificar la key en el header

Pero para empezar, puedes dejarlo sin autenticación.

---

**¿Listo?** Ejecuta: `railway login` y luego `railway up` 🚀
