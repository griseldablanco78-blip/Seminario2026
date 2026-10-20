# Expensa House

MVP Android en Kotlin + Jetpack Compose para administrar los gastos y el inventario del hogar.

## Incluye

- Presupuesto mensual con progreso de gastos.
- Inventario de mercaderia nueva y en uso.
- Alerta visual cuando queda la ultima unidad.
- Lista de compras con pendientes marcables.
- Sugerencia de compra con IA simulada para el MVP.
- Ofertas de supermercados ubicadas en Balvanera, CABA.
- Alta rapida de productos desde Inventario.

## Abrir

Abrir la carpeta en Android Studio y ejecutar la configuracion `app` en un emulador o dispositivo con Android 8.0 o superior. Android Studio descargara las dependencias de Gradle durante la sincronizacion.

## Proximo corte tecnico

1. Persistencia local con Room y movimientos de stock.
2. Notificaciones con WorkManager para reposicion.
3. API de ofertas por supermercado y geolocalizacion.
4. Servicio de IA para leer consumo historico y optimizar el presupuesto.
5. Cuenta familiar y sincronizacion segura.

## Plan web y EDA

La base Room actual es local al telefono y no puede ser leida directamente por una pagina web. La integracion propuesta es Android -> API Python -> dashboard Streamlit. El plan completo de sincronizacion, dataset historico, modelos, voz, imagenes y avatar esta en [PLAN_PROYECTO.md](PLAN_PROYECTO.md).

Para el trabajo practico se recomienda comenzar exportando los datos de Room y registrando movimientos de stock. El inventario actual sirve como estado inicial, pero no alcanza por si solo para entrenar un modelo predictivo: hace falta conservar fechas, cantidades y tipos de movimiento.

## Probar la sincronizacion local Android-Web

La API FastAPI es el puente entre Room y la pagina web. En el primer inicio, si Room esta vacia, Android descarga el estado inicial del servidor. Luego, cada cambio guardado en Android se envia a la API; el boton de sincronizacion de la app tambien permite reenviar el estado manualmente. La pagina web muestra los cambios al recargar o al pulsar su boton 🔄; no usa actualizacion push en tiempo real.

1. En PowerShell, desde la carpeta del repositorio `Seminario2026`, entrar a `Clase 7`:

   ```powershell
   Set-Location -LiteralPath '.\Clase 7'
   ```

2. Crear el entorno virtual e instalar las dependencias (la creacion se hace una sola vez):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
   ```

3. Levantar el servidor desde la carpeta `Clase 7`:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn web.api:app --reload --host 0.0.0.0 --port 8001
   ```

   Dejar esa terminal abierta mientras se usa la aplicacion. Abrir `http://127.0.0.1:8001/` en el navegador de la PC.

### Probar Whisper y la deteccion de intenciones E5

El endpoint recibe audio WebM: Whisper lo procesa con FFmpeg y la alternativa de Google lo convierte a WAV usando FFmpeg. Instalalo una sola vez desde PowerShell y luego cerrá y reabrí la terminal:

```powershell
winget install Gyan.FFmpeg
ffmpeg -version
```

Para habilitar Whisper y la detección experimental de intenciones del chatbot, definí estas variables **antes de iniciar Uvicorn** en la misma terminal:

```powershell
$env:USE_WHISPER = "1"
$env:USE_E5_INTENT = "1"
.\.venv\Scripts\python.exe -m uvicorn web.api:app --reload --host 0.0.0.0 --port 8001
```

Después de iniciar el servidor, en `http://127.0.0.1:8001/docs` probá `POST /api/voice/transcribe` subiendo un audio breve en español. La respuesta indica `"engine": "whisper"` si Whisper lo transcribió o `"engine": "google"` si se usó la alternativa. La primera inferencia descarga los pesos de `openai/whisper-tiny`. Para volver al comportamiento por defecto, cambiá las variables a `"0"` y reiniciá Uvicorn.

El script de calibración de intenciones se ejecuta desde `Clase 7` con:

```powershell
.\.venv\Scripts\python.exe .\web\calibrar_intencion.py
```

El umbral E5 está configurado conservadoramente en `0.88`: en la muestra de calibración local no activó ninguna de 8 frases negativas, pero dejó sin detectar 3 de 11 positivas. Es una prueba pequeña, no una garantía. Cuando el navegador lo permite, el botón del micrófono graba con `MediaRecorder` y envía el audio a este endpoint; si no está disponible, conserva Web Speech API como alternativa. Con `USE_WHISPER="1"` el servidor intenta Whisper primero.

4. Para sincronizar desde el emulador de Android Studio, agregar esta propiedad al archivo local `local.properties` de `Clase 7`:

   ```properties
   expensa.apiBaseUrl=http://10.0.2.2:8001/
   ```

   Para probar con un telefono fisico en la misma red Wi-Fi, reemplazar `10.0.2.2` por la direccion IPv4 local de la PC. Conservar la barra final. Volver a sincronizar Gradle y ejecutar la variante `debug`.

La variante `debug` permite HTTP para esta prueba local. `0.0.0.0` permite que otros dispositivos de la red alcancen el servidor; para usarlo en Internet hacen falta HTTPS, autenticacion y almacenamiento adecuado.
