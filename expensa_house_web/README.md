# Expensa House - web de producto

Copia revisable del backend modular FastAPI y del frontend que se prueban en la PC, actualizada el 25/10/2026. No reemplaza el experimento E5 de `Clase 7/TP_Integrador`: este comparador usa reglas y ofertas guardadas. No se publican datos reales del hogar, cuentas, contraseñas ni tickets.

## Ejecutar en Windows

Desde esta carpeta:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/crear_administradora.py
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8002
```

Abrir http://127.0.0.1:8002/. La primera administradora se crea en la ventana local. El registro público no otorga permisos automáticamente. Los datos iniciales del código son demostrativos: reemplazarlos por datos propios antes de usar para decisiones de compra. El OCR requiere Tesseract instalado; ver la documentación del proyecto principal para la configuración.

## Cambios comprobados

- Acceso rediseñado; cambiar contraseña se encuentra en el login y exige la actual.
- La modificación revoca todas las sesiones y no inicia una sesión nueva automáticamente.
- Navegación adaptable y Boti House animado, con estado de consulta y opciones funcionales.
- Equivalencias entre litros, ml, cc, kg y g; aviso si no hay precio o tamaño confirmado.
- Editor de ofertas guardadas para corregir nombre y precio y subir una fotografía real.
- Fotos procesadas como JPEG sin metadatos originales y protegidas por sesión/permisos.
- 39 pruebas del backend aprobadas en el entorno de desarrollo.

Si no hay foto, se informa; si falta precio, no se inventa. Ratoneando necesita una API autorizada configurada. No se incorporó scraping ni un proveedor nuevo.

## Firebase y despliegue

Ver [propuesta de Firebase](deploy/FIREBASE.md). No está conectado ni desplegado. Hosting puede servir el frontend, Authentication puede gestionar identidades y el backend necesita un entorno Python y almacenamiento durable. No cargar cuentas SQLite, `.env`, fotos familiares ni tickets a GitHub.

## Validación

Para pruebas: instalar `httpx` y ejecutar `python -m unittest discover -s tests -v`. La notebook del integrador y la Clase 10 son entregas diferentes de esta web de producto.
