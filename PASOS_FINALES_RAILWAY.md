# 🚀 INSTRUCCIONES FINALES - Deploy a Railway

## Tu proyecto está casi listo! 

Railway está vinculado pero necesitamos subir el código a GitHub porque el modelo es muy grande para subirlo directamente.

## Pasos Finales (5 minutos):

### 1️⃣ Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. Repository name: `wachitraductor-v2` (o el nombre que prefieras)
3. **Importante**: Selecciona **Privado** si no quieres que sea público
4. **NO** marques "Initialize with README"
5. Click "Create repository"

### 2️⃣ Subir tu Código

GitHub te mostrará instrucciones. Usa estas:

```powershell
cd "C:\Users\User\Desktop\checkpoint-2024 - Copy\endpoint"

# Conectar con tu repositorio (reemplaza TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/wachitraductor-v2.git

# Cambiar a rama main
git branch -M main

# Subir código
git push -u origin main
```

**Nota**: GitHub puede pedirte credenciales. Usa tu usuario y un [Personal Access Token](https://github.com/settings/tokens) como contraseña.

### 3️⃣ Conectar Railway con GitHub

1. Ve al dashboard de Railway: https://railway.com/project/3abfa16e-0ac2-4b50-98c8-372844f3ff15
2. Click en tu servicio o click "+ New"
3. Selecciona "GitHub Repo"
4. Autoriza Railway a acceder a GitHub (si no lo has hecho)
5. Selecciona tu repositorio `wachitraductor-v2`
6. Railway detectará automáticamente el `Dockerfile.simple`
7. Click "Deploy"

### 4️⃣ Configurar Dominio

Una vez que el deploy esté completo (tarda 3-5 minutos):

1. En el dashboard de Railway, ve a "Settings"
2. En la sección "Networking", click "Generate Domain"
3. ¡Listo! Tendrás una URL como: `https://wachitraductor-v2-production.up.railway.app`

### 5️⃣ Probar tu API

```powershell
# Reemplaza TU-URL con tu URL de Railway
curl https://TU-URL.up.railway.app/health
```

O visita:
```
https://TU-URL.up.railway.app/docs
```

## 🎯 Resumen de Comandos

```powershell
# 1. Conectar con GitHub
git remote add origin https://github.com/TU-USUARIO/wachitraductor-v2.git
git branch -M main
git push -u origin main

# 2. Ver proyecto en Railway
railway open

# 3. Ver logs (después de conectar GitHub)
railway logs
```

## 💰 Costos Estimados

- **Plan gratuito de Railway**: $5 USD/mes incluidos
- **Tu API**: Consumirá ~$3-5 USD/mes
- **Resultado**: ¡Gratis el primer mes! 🎉

## ❓ Problemas Comunes

**Error al hacer push a GitHub**
```powershell
# Genera un Personal Access Token en: https://github.com/settings/tokens
# Úsalo como contraseña cuando GitHub lo pida
```

**Railway no detecta el Dockerfile**
- Ve a Settings → Build en Railway
- Cambia "Builder" a "Dockerfile"
- Dockerfile Path: `Dockerfile.simple`

**Deploy falla por memoria**
- Es normal, el modelo es grande
- Railway puede tardar 5-10 minutos en el primer deploy
- Verifica los logs en Railway dashboard

## 📝 Siguiente Paso

Una vez que tengas tu URL de Railway:
1. Úsala en tu app móvil (ver `EJEMPLOS_MOVILES.md`)
2. Reemplaza `YOUR_API_URL` con tu URL real

---

## 🎓 Estado Actual

✅ Railway CLI instalado  
✅ Autenticado como: varela.hito@gmail.com  
✅ Proyecto creado: wachitraductor v2  
✅ Git inicializado  
✅ Commit realizado  
⏳ Falta: Subir a GitHub y conectar con Railway

**Próximo comando**: 
```powershell
git remote add origin https://github.com/TU-USUARIO/wachitraductor-v2.git
git push -u origin main
```

---

¿Necesitas ayuda con GitHub? Ve a https://github.com/new para crear el repo.
