# Expensa House - Proyecto integrador

El proyecto combina una app Android, una API Python y componentes web para gestionar stock, lista de compras y presupuesto del hogar. La copia académica de Clase 7 documenta además la integración experimental de similitud semántica con E5.

## Experiencia documentada

El integrador comparó dos modelos preentrenados con once consultas y un catálogo de demostración. La inferencia local produjo salidas evaluables; la llamada remota encontró un límite de créditos. Los resultados y errores se explican en la notebook y los PDF revisados.

- [Carpeta del integrador](TP_Integrador/).
- [Notebook ejecutada](TP_Integrador/notebook/TP_Blanco_Griselda.ipynb).
- [Informe revisado](TP_Blanco_Griselda_revisado.pdf).
- [Presentación revisada en PDF](Expensa_House_Presentacion_revisada.pdf).

La documentación diferencia datos de demostración de precios reales y la ejecución local de un deploy público. La publicación final de la app y la presentación PPTX no están acreditadas como terminadas. Los PDF anteriores se conservan como versiones históricas.

## Relación con los demás componentes

La [web modular de producto](../expensa_house_web/) conserva una versión distinta del backend y del frontend. La actividad de entrenamiento y exportación está en [Clase 10](../clase_10/); es independiente de la inferencia preentrenada del integrador.

Repositorio: Seminario2026. Rama: `Proyecto_Integrador`.
