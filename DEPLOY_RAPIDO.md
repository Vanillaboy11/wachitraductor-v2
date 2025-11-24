# 🚀 DEPLOY RÁPIDO EN RAILWAY

## Método Más Rápido (2 minutos)

```powershell
# 1. Login en Railway
railway login

# 2. Crear nuevo proyecto
railway init

# 3. Deploy
railway up

# 4. Agregar dominio público
railway domain

# 5. Ver logs
railway logs
```

¡Eso es todo! Tu API estará online en 2-3 minutos.

## Obtener tu URL

Después de `railway domain`, obtendrás una URL como:
```
https://translation-api-production-xxxx.up.railway.app
```

## Probar tu API

```powershell
# Reemplaza TU-URL con tu URL de Railway
curl https://TU-URL.up.railway.app/health
```

O visita:
```
https://TU-URL.up.railway.app/docs
```

## Ver Dashboard

```powershell
railway open
```

---

**Problemas?** Lee `RAILWAY_DEPLOY.md` para guía completa.
