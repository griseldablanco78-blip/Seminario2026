# Documento Funcional: Proyecto Expensa House (IA, Datos y Web)

## 1. Introducción
El proyecto "Expensa House" busca optimizar la gestión de stock y gastos familiares mediante el análisis de datos (EDA), desarrollo web, y la integración de modelos de Machine Learning y una interfaz conversacional (chatbot) llamada **Boti House**.

## 2. Obtención y Preprocesamiento del Dataset
Se desarrolló un script en Python (`data/generar_dataset.py`) para simular un dataset de consumo de supermercado "sucio", permitiendo aplicar técnicas de limpieza de datos reales:
- **Limpieza:** Se trataron valores nulos (NaN) imputando precios con la mediana por producto.
- **Outliers:** Se corrigieron cantidades negativas y precios anómalos usando el Rango Intercuartílico (IQR).
- **Tipos de Datos:** Estandarización de fechas y capitalización de texto.
- **Duplicados:** Eliminación de registros repetidos.

El dataset final limpio se guardó en `inventario_movimientos_limpio.csv`.

## 3. Análisis Exploratorio de Datos (EDA) e Hipótesis
Se plantearon y validaron 3 hipótesis mediante visualizaciones (implementadas en el Dashboard de Streamlit):
1. **Frecuencia de Reposición:** Las categorías básicas (ej. Lácteos, Limpieza) concentran la mayor cantidad de compras y consumo, validando que el esfuerzo de automatización debe centrarse ahí.
2. **Productos Críticos y Gasto:** Un pequeño número de productos concentra el gasto mensual. Es vital monitorear sus precios y predecir cuándo se quedarán sin stock para comprar en oferta.
3. **Consumo por Día:** Se identificaron picos de consumo en días específicos de la semana, lo cual alimenta nuestro modelo predictivo.

## 4. Integración Web y API
- **FastAPI (`web/api.py`):** Actúa como el puente (backend) que permite la sincronización de datos con la aplicación móvil (Android). Recibe movimientos y provee el stock actualizado a otras plataformas.
- **Streamlit (`web/app_streamlit.py`):** Un dashboard interactivo que expone las visualizaciones del EDA y funciona como interfaz web principal del sistema para el usuario final.

## 5. Machine Learning (Modelo Predictivo)
Se desarrolló un script de entrenamiento (`modelos/modelo_prediccion.py`) utilizando el algoritmo **Random Forest Classifier**:
- **Objetivo:** Predecir qué productos necesitarán reposición (stock <= 2) en base a su historial de consumos y gastos.
- **Justificación del modelo:** Random Forest es robusto ante outliers, maneja bien relaciones no lineales y es menos propenso al sobreajuste (overfitting) que un árbol de decisión simple (Decision Tree). XGBoost era otra alternativa válida, pero Random Forest requiere menos ajuste de hiperparámetros inicial para un buen MVP.
- **Desempeño:** El modelo inicial obtuvo una exactitud (Accuracy) de aproximadamente **83%**.

## 6. IA Conversacional: Boti House
Se delineó la estructura base para el chatbot "Boti House" dentro del dashboard web. Este chatbot integra las capacidades para que un usuario consulte el inventario y listas de compra mediante procesamiento de lenguaje natural (NLP) e integración de audio (Texto a Voz y Voz a Texto).

## 7. Próximos Pasos y Escalabilidad
1. Conectar los endpoints de FastAPI directamente en el código Kotlin de la aplicación Android.
2. Implementar los modelos de Whisper/SpeechRecognition en Boti House para la interacción por voz.
3. Desplegar el sistema en la nube (ej. AWS, Heroku o Render).
