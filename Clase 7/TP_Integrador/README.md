# TP integrador: modelos de Hugging Face para Expensa House

**URL pública de la web integrada:** pendiente de confirmar.

La aplicación que se quiere conservar es la web principal de Expensa House, con interfaz FastAPI/HTML y los datos manuales sincronizados con la app. En esta carpeta hay además un **prototipo experimental independiente en Gradio** para probar modelos de Hugging Face; no reemplaza la web principal, no usa sus datos sincronizados y no debe presentarse como la versión web integrada.

> **Datos de demostración:** `ofertas.csv` contiene ejemplos inventados exclusivamente para probar el experimento. No son ofertas actuales ni datos reales del stock de Expensa House; no presentes esos precios como reales. El comparador de la web principal utiliza las ofertas manuales sincronizadas desde la app.

## 1. Problema y elección del modelo

El problema acotado es reconocer que una consulta y un nombre de producto pueden referirse al mismo artículo aunque usen distintas palabras o abreviaturas. Una búsqueda literal por palabras sirve como línea base, pero no entiende paráfrasis.

La búsqueda en Hugging Face se hizo con la tarea **Sentence Similarity**, la biblioteca **Transformers** y modelos de tamaño pequeño. La lectura de las fichas exige aclarar que el metadato `library_name` de los dos seleccionados declara `sentence-transformers`; sus fichas, sin embargo, muestran cómo usarlos mediante Transformers. La búsqueda/filtro y el valor exacto de `library_name` no son lo mismo.

| Modelo | Parámetros y características declaradas | Uso en este TP |
|---|---|---|
| [`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 117.653.760 valores F32 según los metadatos `safetensors` del Hub; 12 capas; embeddings de 384 dimensiones; español declarado; licencia Apache-2.0. | Candidato de comparación en la notebook. |
| [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small) | 117.653.760 valores F32 según los metadatos `safetensors` del Hub; 12 capas; embeddings de 384 dimensiones; 100 idiomas, incluido español; licencia MIT. | Integrado en el comparador de la web principal y también usado en la demo Gradio; antepone `query:` a la consulta y `passage:` a cada oferta, como recomienda su model card. |

Ambos tienen unos 118 millones de parámetros: son “small” frente a modelos grandes, pero no diminutos y su inferencia local puede requerir tiempo y memoria. La dimensión de 384 es el tamaño del vector de salida, no el número de parámetros. En La ejecución local de VS Code, con 11 consultas y `ofertas.csv`, la línea base literal acertó 1/11, MiniLM 7/11 y E5 8/11 con umbral 0,50. E5 acertó todos los positivos, pero clasificó como coincidencias los tres negativos; MiniLM tuvo menos falsos positivos, aunque también más falsos negativos. Es una muestra mínima con datos de demostración, por lo que no se declara un ganador. La notebook conserva las tablas completas. Su método de pooling es una simplificación didáctica; la web y la demo Gradio usan pooling enmascarado.

### Modelos para las tres problemáticas del proyecto

La web principal de Expensa House **ya tiene su propia interfaz y sincroniza los datos manuales de la app**. E5 ya está conectado al comparador de esa web. Los otros modelos de la tabla son candidatos, no integraciones terminadas.

| Problemática | Lo que ya tiene la web principal | Modelo del Hub adecuado y estado |
|---|---|---|
| Comparar ofertas | Busca exclusivamente entre las ofertas manuales sincronizadas. E5 puntúa y ordena las ofertas que además superan el filtro de palabras clave; no modifica ni inventa precios. | Integrado: [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small), `sentence-similarity`, 117.653.760 parámetros, `library_name: sentence-transformers` y receta compatible con Transformers. La notebook lo contrasta con MiniLM. |
| Pasar voz a texto | El buscador tiene botón de voz mediante Web Speech API; el endpoint servidor existente usa reconocimiento de Google. Ninguno de los dos flujos actuales usa un modelo HF. | [`openai/whisper-tiny`](https://huggingface.co/openai/whisper-tiny): `automatic-speech-recognition`, 37.760.640 parámetros, biblioteca Transformers, español declarado y licencia Apache-2.0. Está usado en la demo Gradio separada, no en la web principal. Se puede conectar al endpoint, teniendo en cuenta los recursos que necesita. |
| Chatbot | Boti ya saluda, ofrece opciones y consulta los datos guardados mediante reglas; no usa un LLM. | Candidato, no integrado: [`Qwen/Qwen2.5-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct), `text-generation`, 494.032.768 parámetros, biblioteca Transformers, soporte de español declarado y licencia Apache-2.0. Para respuestas sobre datos reales, habría que pasarle el contexto obtenido por el código y no permitir que invente precios o stock. |

Para cumplir la parte experimental del TP, alcanza con elegir **un problema**. Se eligió el comparador: E5 ya está integrado a la web y la notebook contrasta E5 y MiniLM con las mismas consultas. La notebook usa deliberadamente el CSV pequeño etiquetado para la evaluación reproducible; no lo confunde con las ofertas reales del hogar. En la web, E5 solo ordena ofertas con una coincidencia de más de la mitad de las palabras clave consultadas; el score semántico no demuestra que dos variantes sean idénticas. Esta regla conservadora reduce resultados falsos como “aceite de oliva” ante “aceite de girasol”, pero puede dejar afuera sinónimos con palabras distintas. Whisper y Qwen siguen siendo candidatos para las otras problemáticas, no integraciones terminadas.

La API principal carga E5 de forma diferida al comparar una consulta con ofertas compatibles. La primera búsqueda necesita Internet para descargar los pesos; después los reutiliza desde la caché local y no requiere `HF_TOKEN`. Si faltan dependencias o el modelo no se puede descargar, la API responde con un error 503 explicativo; la interfaz muestra ese mensaje.

**Interfaz pedida por la consigna:** la web de Expensa House está hecha con FastAPI y HTML/JavaScript propio, no con Gradio ni Streamlit. La demo Gradio de `TP_Integrador/app.py` sí usa Gradio, pero es independiente y trabaja con datos inventados. No presentarla como si estuviera conectada a la web. Si el curso exige literalmente Gradio o Streamlit, hay que confirmar si aceptan la interfaz propia o agregar una interfaz de ese framework conectada a los datos de Expensa House.

## 2. Estructura

```text
TP_Integrador/
├── app.py
├── ofertas.csv
├── requirements.txt
├── README.md
├── notebook/
│   └── TP_Blanco_Griselda.ipynb
└── tp_comparador/
    └── tp_comparador.ipynb
```

La columna `familia` sirve para evaluar si el mejor producto recuperado pertenece a la categoría esperada. Las columnas `fecha_relevamiento` y `fuente` permiten documentar de dónde salen los precios.

## 3. Ejecutar la demo experimental de Gradio en Windows

Estos comandos levantan únicamente la demo de esta carpeta, **no la web principal sincronizada**. No son el comando para iniciar la web de Expensa House:

Abrí PowerShell en la carpeta raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m pip install -r TP_Integrador\requirements.txt
.\.venv\Scripts\python.exe TP_Integrador\app.py
```

Si no existe `.venv`, crealo primero desde PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r TP_Integrador\requirements.txt
```

La app local **no necesita `HF_TOKEN` ni créditos de inferencia**. Descarga los pesos públicos del Hub la primera vez y ejecuta los modelos en el equipo. El token que se usó para probar la API solo sirve para esa prueba remota; no lo incluyas en la app ni en Git. Abrí `http://127.0.0.1:7860` (no uses `0.0.0.0` como URL del navegador) y probá, por ejemplo, “leche entera”, “yerba mate” y “detergente para vajilla”.

Podés escribir en el cuadro o grabar/subir audio en español. La transcripción corre localmente con [`openai/whisper-tiny`](https://huggingface.co/openai/whisper-tiny). Gradio le pasa la señal de audio al modelo directamente, sin requerir FFmpeg. La búsqueda usa [`intfloat/multilingual-e5-small`](https://huggingface.co/intfloat/multilingual-e5-small), también local, con pooling enmascarado y prefijo `query:` que recomienda la model card. Los pesos se descargan del Hub al primer uso. Se muestran las cinco ofertas con mayor score semántico; también se muestra el precio por 100 g/ml. El score mide similitud, no es una probabilidad ni garantiza que el producto sea equivalente: verificá tipo, marca y cantidad antes de comparar precios.

Para dictar desde el navegador, permití el acceso al micrófono cuando lo solicite. En local, usá `http://127.0.0.1:7860`. Si falla el dictado, revisá los permisos del micrófono; también podés subir un audio o seguir usando la entrada escrita. La primera inferencia de voz descargará Whisper y puede demorar.

## 4. Ejecutar la notebook

Abrí `notebook/TP_Blanco_Griselda.ipynb` en Colab o Jupyter. Si usás Colab, subí `ofertas.csv` cuando la notebook lo pida. La primera celda instala las dependencias de experimentación.

La notebook compara los dos modelos con **las mismas consultas y los mismos productos**:

1. Una búsqueda literal como línea base.
2. `transformers.pipeline("feature-extraction")` local. La notebook promedia los vectores de tokens y calcula similitud coseno para obtener scores comparables.
3. Intento de `InferenceClient.sentence_similarity` remoto. Requiere token, disponibilidad del proveedor y créditos; registrá los errores de ejecución, no los reemplaces por scores inventados.
4. Tiempo, score top 1 y clasificación con un umbral inicial. La notebook guardada registra resultados locales sobre 11 consultas didácticas; no calcula precisión top 2. La prueba remota con `InferenceClient` no devolvió puntajes: Hugging Face respondió HTTP 402 (`Payment Required`) por falta de créditos.

El intento remoto requiere un token de Hugging Face y que el proveedor tenga disponible el modelo y capacidad de inferencia para tu cuenta. En la prueba de este proyecto, `InferenceClient` devolvió HTTP 402 (`Payment Required`): la cuenta no tenía créditos restantes y no se obtuvieron puntajes remotos. La notebook registra ese error y las consultas no ejecutadas. En VS Code, creá un archivo `.env` **local** dentro de `TP_Integrador/` (junto a `app.py`) con esta línea:

```text
HF_TOKEN=hf_pegá_tu_token_acá
```

La notebook carga ese archivo con `python-dotenv`. El `.gitignore` de `Clase 7` ya excluye `.env`; verificá igualmente con `git status` que no esté preparado para subir. No pegues el token en la notebook, el README ni un mensaje. En Colab podés guardar el secreto como `HF_TOKEN` en la sección Secrets. La app de Gradio no depende de la API remota: corre inferencia local.

Corré todas las celdas y guardá las tablas realmente obtenidas. No uses los pocos ejemplos artificiales como garantía de calidad para todos los productos ni como precios reales. Para evaluar Expensa House, reemplazá o separá claramente esos ejemplos de las ofertas manuales observadas.

## 5. Publicar la demo experimental (no la web integrada)

La siguiente configuración, si se usa, publica solo la demo de Gradio basada en `ofertas.csv`. **No publica ni sincroniza la web principal de Expensa House.** La URL que resulte no se debe presentar como la aplicación conectada a los datos reales. E5 ya se integró al comparador de la API principal; falta publicar esa web integrada y confirmar su URL pública. En la demo, el **código** vive en este repositorio, los **pesos** en Hugging Face y la inferencia corre dentro del proceso que aloja Gradio; no requiere créditos ni token para inferir. El servidor necesita memoria suficiente para PyTorch, E5 y Whisper.

1. Subí la carpeta `TP_Integrador/` a una rama de GitHub.
2. En Render, creá un **Web Service** conectado a ese repositorio y elegí la rama.
3. Configurá:

   | Campo | Valor |
   |---|---|
   | Root Directory | `TP_Integrador` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `python app.py` |
   | Environment Variable | No se requiere `HF_TOKEN` para la app |

4. Verificá que el plan del servidor tenga memoria y CPU suficientes: los modelos se descargan y corren dentro de la instancia. El primer arranque y la primera transcripción tardan más.
5. Esperá el despliegue y probá la URL pública. Copiala en el encabezado de este README y en el informe. No configures ni publiques un token para la app local.

## 6. Informe y presentación

Usá los resultados de la notebook para justificar las decisiones, no resultados supuestos:

- **Necesidad y alcance:** quién buscaría ofertas y qué resuelve la similitud semántica frente a una búsqueda literal.
- **Elección del modelo:** tarea, idiomas, parámetros, model cards, resultados comparativos y límites; incluir que la prueba local fue pequeña.
- **Arquitectura experimental:** código de la demo en Git; pesos en el Hub; inferencia local con Transformers; interfaz Gradio si se despliega esa demo. Aclarar que no es la arquitectura de la web integrada.
- **Arquitectura de Expensa House:** conservar la interfaz y la API existentes, usar las ofertas manuales sincronizadas como fuente y ejecutar E5 localmente en la API para ordenar ofertas compatibles por palabras clave. Falta publicar la web integrada y validar el comportamiento con un conjunto representativo de ofertas manuales.
- **Datos:** origen, fecha de relevamiento, unidad de comparación y limitación de que el CSV no se actualiza solo.
- **Evaluación:** consultas, clasificaciones, scores y tiempos obtenidos al ejecutar la notebook; registrar explícitamente cualquier error de `InferenceClient`. No afirmar precisión top 2: la notebook actual calcula una clasificación top 1 con umbral.
- **Publicación:** URL pública, configuración del servicio, recursos necesarios y por qué la inferencia es local.
- **Mejoras:** conseguir datos actualizados con permiso, ampliar ejemplos y probar el sistema con usuarios.

En esta carpeta todavía no están el informe PDF ni la presentación PPTX, y no hay una URL pública confirmada de la web integrada. Para completar la entrega, ejecutá y guardá la notebook, publicá la web integrada, añadí su enlace público real y prepará `TP_Apellido_Nombre.pdf` y `TP_Apellido_Nombre.pptx` con tu nombre. No uses como enlace de la web integrada una publicación de la demo independiente. El PDF del aula requiere iniciar sesión, así que compará los entregables con la consigna completa del curso antes de subirlos.
