# Clase 5 - Deploy de una app en Python

## Objetivo
Aprender dónde y cómo publicar una aplicación Python con Gradio, y cómo preparar una app para deploy en Render.

## Requisitos
- Python 3.9 o superior
- pip
- Cuenta en GitHub
- Cuenta en Render

## Instalación
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución local
```powershell
python app.py
```
Luego abrir en el navegador la URL que muestre Gradio, normalmente:

http://127.0.0.1:7860

## Importante para Render
La app usa la variable de entorno `PORT` para que Render pueda asignar el puerto correcto:

```python
server_port=int(os.environ.get("PORT", 7860))
```

## Qué hace la app
- Tiene un campo para escribir el nombre
- Tiene un botón para saludar
- Muestra el resultado en pantalla
- Usa `gr.Blocks`

## Deploy en Render
1. Crear cuenta en Render
2. Crear un Web Service
3. Conectar el repositorio de GitHub
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Esperar a que termine el deploy
6. Usar la URL pública que te da Render

## Archivos relevantes
- `app.py`: aplicación principal con Gradio
- `requirements.txt`: dependencias necesarias
