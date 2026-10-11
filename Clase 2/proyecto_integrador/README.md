# Proyecto integrador - Clase 2

Aplicación básica en Gradio para practicar la creación y organización de un proyecto propio. La app pide un nombre y muestra un saludo.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

Desde esta carpeta, crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
python app.py
```

Abrir en el navegador la dirección local que indique Gradio, normalmente:

http://127.0.0.1:7860

## Archivos

- `app.py`: aplicación de saludo hecha con Gradio.
- `requirements.txt`: dependencias necesarias.
- `.gitignore`: archivos locales que Git no debe subir, como el entorno virtual.
