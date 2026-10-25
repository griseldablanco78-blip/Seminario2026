# Clase 10 - Del dataset al modelo exportado

Griselda Blanco - Seminario de Actualización, IFTS N.º 18. Material de base de Cynthia M. Villagra.

## Archivos

- `Clase_10_Blanco_Griselda.ipynb`: notebook técnicamente ejecutado, con salidas reales de scikit-learn, PyTorch y Keras.
- `modelos_exportados/`: pipeline joblib, state_dict, Keras y modelo completo PyTorch con sus scalers.
- `resultados_ejecucion.json`: métricas reales y versiones del entorno.
- `requirements.txt`: dependencias para repetirlo. Keras 3 utiliza PyTorch como backend.

## Actividad elegida

**Modelo completo de PyTorch**: exportación, recarga sin volver a entrenar y comparación de predicciones. Se usa `weights_only=False` exclusivamente sobre el archivo generado por la propia notebook. Los archivos pickle/joblib no deben abrirse si provienen de desconocidos. La notebook desarrolla las cuatro preguntas con documentación oficial. La inscripción en la planilla del aula la realiza la estudiante.

## Ejecutar

En Colab, subir la notebook y ejecutar primero `%pip install -r requirements.txt` si se subió también ese archivo. Otra opción es instalar numpy, pandas, matplotlib, scikit-learn, torch, keras y joblib en la primera celda. Reiniciar el entorno si lo pide la instalación. La variable `KERAS_BACKEND=torch` se establece antes de importar Keras.

Los dos errores intencionales se conservan. SGD sin escalar puede devolver valores enormes en lugar de lanzar una excepción según la versión; eso también es un fallo del resultado. El regresor sin scaler puede cargar correctamente y predecir mal.

## Resultado técnico observado

La prueba de recarga del modelo completo devolvió la misma predicción, sin nuevo entrenamiento. Consultar RMSE, R² y versiones en el JSON; son datos sintéticos de viviendas, no una herramienta de tasación.

## Pendiente personal antes de entregar

Las estimaciones y celdas «Tu respuesta» están expresamente pendientes. No fueron completadas como si Griselda hubiera anticipado resultados. Escribir las predicciones personales, revisar la investigación con palabras propias y repetir las celdas correspondientes antes de entregar. El notebook se ejecutó con asistencia de IA para preparar y comprobar el código; se declara esta asistencia y no se presenta como actividad personal terminada.

Fuentes: https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html y https://keras.io/getting_started/.
