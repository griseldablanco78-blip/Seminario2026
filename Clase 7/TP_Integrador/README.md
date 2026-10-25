# Integrador - Comparación semántica de productos

El trabajo examinó la recuperación de productos a partir de consultas en español y casos desafiantes. Se utilizaron modelos preentrenados de Hugging Face para inferencia, sin entrenamiento ni fine-tuning.

## Experimento realizado

Se compararon MiniLM multilingüe y E5 small con once consultas sobre un CSV de 12 registros de demostración. Las familias conocidas permitieron medir clasificación top 1 con umbral. El resultado global fue 4/11 para la referencia literal, 7/11 para MiniLM y 8/11 para E5. El score de similitud no fue interpretado como una probabilidad.

E5 recuperó los ocho positivos y aceptó los tres negativos; MiniLM rechazó los negativos y perdió cuatro positivos. La muestra no permite establecer un ganador general ni una calibración independiente.

La ejecución local utilizó pipeline de Transformers. El intento remoto con InferenceClient devolvió HTTP 402 por falta de créditos; no hay scores remotos comparables. Las salidas originales se conservaron en el notebook.

## Componentes y alcance

- [Notebook ejecutada](notebook/TP_Blanco_Griselda.ipynb): procedimiento, tablas y conclusiones.
- `app.py`: demo Gradio sobre CSV, con similitud E5 y voz mediante Whisper. Es un componente independiente de la web integrada.
- `ofertas.csv`: datos de demostración; no son ofertas vigentes.
- `requirements.txt`: dependencias declaradas de la demo.

La copia de Clase 7 contiene además la integración E5 de su API. La versión modular de producto está documentada en `expensa_house_web/`; no es idéntica a esa copia académica.

## Documentación y estado

[Informe revisado](../TP_Blanco_Griselda_revisado.pdf) · [Presentación revisada](../Expensa_House_Presentacion_revisada.pdf).

El código y la evidencia están en la rama [Proyecto_Integrador](https://github.com/griseldablanco78-blip/Seminario2026/tree/Proyecto_Integrador). El deploy público final y el archivo PPTX no están acreditados como completos. El trabajo documenta la experiencia disponible y sus límites.
