# Checklist de entrega del TP Integrador

## ✅ 1. Estructura de carpetas y archivos
- `TP_Integrador/`
  - `app.py` ✅
  - `requirements.txt` ✅
  - `README.md` ✅ (revisar y completar)
  - `ofertas.csv` ✅ (datos de prueba)
  - `notebook/TP_Blanco_Griselda.ipynb` ✅ (presente en carpeta `Clase 7/notebook` y enlazado en README)
  - `tp_comparador/` (opcional, contiene notebooks auxiliares) ✅
  - `TP_Blanco_Griselda.pdf` 📄 (pendiente de subir)
  - `presentation.pptx` 📊 (pendiente de subir)
  - `.env` (contiene `HF_TOKEN` si se usa la API remota) – **añadir a `.gitignore`**
  - `.gitignore` (añadir si aun no existe) ✅

## ✅ 2. Código de `app.py`
- Importar `torch` (faltaba). ✅
- Uso de `InferenceClient` para Whisper y modelo remoto está correcto, pero se recomienda:
  - Manejar excepciones de red/ tokens.
  - Validar que `client_large.post` devuelve un dict con clave `embeddings` o `data` dependiendo del endpoint.
- La función `voice_flow` abre el archivo de audio con `open(audio_path, "rb")`; asegúrate de cerrar el file o usar `with`.
- Añadir comentarios docstring a cada función (ya están presentes).
- La llamada `demo.queue().launch(share=True)` está bien para demo; para despliegue productivo usar `share=False` y configurar en el servicio (Render, Fly, etc.).

## ✅ 3. `requirements.txt`
- Incluye todas las dependencias usadas:
  ```
  gradio>=4.0
  transformers>=4.40
  huggingface_hub>=0.23
  pandas>=2.2
  numpy>=1.26
  torch>=2.2
  python-dotenv>=1.0  # si usas .env
  ```
- Verificar que la versión de `torch` sea compatible con tu CPU/GPU.

## ✅ 4. `README.md`
- Completar los campos pendientes:
  - **URL pública de la web integrada** (si ya está desplegada).
  - **Enlace al repositorio**: `https://github.com/griseldablanco78-blip/Seminario2026/tree/Proyecto_Integrador`
  - Instrucciones de instalación y ejecución (ya existen, solo actualizar rutas si cambian).
  - Añadir sección *Cómo reproducir la notebook* con comando `jupyter notebook` o abrir en Colab.
  - Añadir licencia y créditos.
- Formatear tablas con markdown (las tablas actuales están bien).

## ✅ 5. Notebook (`TP_Blanco_Griselda.ipynb`)
- Verificar que contiene:
  - Comparación de **al menos 2 modelos** (e5‑small y MiniLM u otro) con **8 frases** (incluye 2 con ironía, otro idioma, jerga, texto corto).
  - Tabla de resultados con columnas: `frase`, `etiqueta`, `puntaje`, `¿acertó?` para cada modelo.
  - Llamados con **pipeline** y **InferenceClient**, con tiempos medidos (`time.time()` o `%time`).
  - Impresión de `type()` del retorno y acceso a datos.
  - Comentarios explicativos en celdas de texto.
- Si falta alguna de estas partes, añádelas.

## ✅ 6. Informe PDF (`TP_Blanco_Griselda.pdf`)
- Debe contener los apartados A‑F solicitados (problema, modelo, arquitectura, deploy, errores, límites, vocabulario).
- Incluir diagramas (puedes usar mermaid y exportar a PNG).
- Añadir en la última página los **links** a la app y al folder del TP.
- Revisar ortografía y consistencia de terminología.

## ✅ 7. Presentación PPTX (`presentation.pptx`)
- Diapositivas recomendadas (6‑10):
  1. Problema.
  2. Modelo elegido y por qué.
  3. Dónde vive el código y el modelo.
  4. Decisión de deploy y alternativas descartadas.
  5. Captura de la app funcionando + link.
  6. Error significativo y lección aprendida.
  7. Límites y próximo paso.
- Utilizar diseño limpio (colores armoniosos, tipografía `Inter` o `Roboto`).
- Exportar a PDF opcional para revisión.

## 📋 Próximos pasos
1. **Subir** los archivos pendientes (`TP_Blanco_Griselda.pdf` y `presentation.pptx`) a la carpeta `TP_Integrador` (o a `Clase 7` y enlazarlos desde README).
2. **Actualizar** el README con la URL pública de la demo (una vez que la despliegues en Render, Fly.io, etc.).
3. **Crear** `.gitignore` si aún no existe e incluir:
   ```
   .env
   __pycache__/
   *.pyc
   .venv/
   ```
4. **Probar** la app localmente con `python app.py` y confirmar que funciona sin errores.
5. **Publicar** la demo (ejemplo con Render):
   - Root Directory: `TP_Integrador`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - No token necesario.
6. **Añadir** los enlaces a la app y al repositorio al final del PDF y del README.

---
**Si encuentras algún punto que necesites corregir o tienes dudas sobre alguna sección, avísame y lo ajustamos antes de la entrega final.**
