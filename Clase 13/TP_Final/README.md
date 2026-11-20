# Jardín de Datos: Iris

En este trabajo entrené un clasificador que recibe cuatro medidas de una flor y estima cuál de las tres especies de Iris se parece más a ellas.

## Decisiones técnicas

- **Elegí Iris**, incluido en scikit-learn, para no depender de una descarga externa. Tiene cuatro medidas numéricas y tres especies.
- **Permito decimales dentro de los rangos observados en Iris** (sépalo: 4,3–7,9 y 2,0–4,4 cm; pétalo: 1,0–6,9 y 0,1–2,5 cm). Esos límites se muestran en la web y se validan también en la API; no obligo a avanzar en saltos fijos porque las medidas son continuas.
- **Elegí regresión logística con `StandardScaler`** porque es un clasificador multiclase que puedo explicar y devuelve probabilidades estimadas. La pipeline aplica el mismo escalado al entrenar y al predecir.
- **Usé scikit-learn y `joblib`** para entrenar y guardar el modelo, como pide la consigna.
- **Usé FastAPI y Pydantic** para exponer y validar las rutas. FastAPI genera `/docs` y `/openapi.json` a partir del código.
- **Usé HTML, CSS y JavaScript** para construir el formulario y los gráficos sin sumar otro framework de frontend.
- **Elegí Vercel para el sitio y Render para la API** porque ya conozco Vercel y Render puede ejecutar el backend FastAPI como servicio web. Configuré CORS con los dos dominios de Vercel usados por el proyecto.

## Estructura

```text
TP_Final/
├── app/
│   ├── backend/
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── app.js
│   │   ├── config.js            # URL de la API
│   │   └── iris_data.js         # puntos para el gráfico; se genera desde el notebook
│   └── modelo/
│       └── modelo.joblib        # se genera desde el notebook
└── notebook/
    └── entrenamiento.ipynb
```

## Entrenar el modelo

Abrí y ejecutá todas las celdas de `notebook/entrenamiento.ipynb`. El notebook guarda el modelo y el pequeño archivo de datos que usa el gráfico del frontend.

Con una división estratificada de 75 % para entrenamiento y 25 % para prueba obtuve **accuracy 0,921** y **F1 macro 0,923**. La matriz de confusión mostró que confundí tres flores de prueba entre versicolor y virginica; clasifiqué correctamente las 12 setosa reservadas. El conjunto es pequeño, por eso presento estos valores como una evaluación didáctica y no como una garantía para otras flores. El gráfico compara los promedios de las cuatro medidas por especie con las medidas ingresadas; no es una regresión porque la especie es una categoría.

## Ejecutar localmente

Desde `TP_Final/app/backend`, creá un entorno con Python 3.12, 3.13 o 3.14, instalá las dependencias y arrancá la API:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

La API queda en `http://127.0.0.1:8000`; la documentación interactiva, en `/docs`.

En otra terminal, desde `TP_Final/app/frontend`, serví la web:

```powershell
py -3.14 -m http.server 5500
```

Abrí `http://127.0.0.1:5500`. Servir el HTML por HTTP evita problemas del navegador al abrirlo directamente como `file://`.

## Contrato de la API

### `GET /health`

Respuesta `200`:

```json
{"estado":"ok"}
```

### `POST /predecir`

Entrada válida:

```json
{
  "sepal_length_cm": 5.1,
  "sepal_width_cm": 3.5,
  "petal_length_cm": 1.4,
  "petal_width_cm": 0.2
}
```

Respuesta `200` (las cifras dependen del modelo entrenado):

```json
{
  "especie": "setosa",
  "probabilidades": {
    "setosa": 0.9811,
    "versicolor": 0.0189,
    "virginica": 0.0
  }
}
```

Los campos faltantes, tipos incorrectos y medidas fuera del rango observado se rechazan con `422`. Durante mis pruebas locales, la entrada sin `petal_width_cm`, la entrada con `"petal_width_cm": "mucho"` y una medida de sépalo de `8.0 cm` devolvieron `422`. Un decimal válido de `5.15 cm` fue aceptado. También comprobé que una ruta inexistente responde `404`, que usar `GET` en `/predecir` responde `405` y que la preflight CORS local responde `200`. No observé una respuesta `500` en las pruebas realizadas.

## Publicación

- Frontend: [Jardín de Datos en Vercel](https://jardin-de-datos-iris.vercel.app/), servido como sitio estático.
- API en Render: [estado](https://jardin-de-datos-api.onrender.com/health), [Swagger](https://jardin-de-datos-api.onrender.com/docs) y [OpenAPI](https://jardin-de-datos-api.onrender.com/openapi.json).
- El frontend apunta a `https://jardin-de-datos-api.onrender.com`. La variable `FRONTEND_ORIGINS` permite los dos dominios del proyecto. En desarrollo también habilito `localhost:5500` y `127.0.0.1:5500`.
- Probé en Render `GET /health` (200) y `POST /predecir` con medidas válidas (200, especie y probabilidades). La instancia gratuita puede suspenderse por inactividad y demorar al despertar.

La web abre públicamente sin iniciar sesión. Comprobé desde el formulario que se conecta con la API de Render y muestra la predicción con sus probabilidades.

## Errores reales y cómo los resolví

1. **El navegador rechazaba decimales del formulario.** Detecté que el formulario tenía `min="0.01"` y `step="0.1"`. La validación nativa indicaba `stepMismatch` aunque el valor estuviera dentro del rango visible, así que no se enviaba el `fetch`. Corregí los límites por medida y usé `step="any"`; después un decimal como `5.15` llegó a la API y fue aceptado.
2. **La API no arrancaba con el Python predeterminado.** El registro completo fue `C:\Python315\python.exe: No module named uvicorn`. El comando usó Python 3.15, que no tenía las dependencias instaladas. Comprobé el entorno Python 3.14 del proyecto y arranqué Uvicorn con ese intérprete; la ruta `/health` respondió `200`.

En las pruebas de contrato también diferencié las validaciones esperadas `4xx` de un error inesperado `5xx`. No observé una respuesta `500`.

El README explica cómo ejecutar mi proyecto; no reemplaza el informe PDF que presentaré en el aula virtual.
