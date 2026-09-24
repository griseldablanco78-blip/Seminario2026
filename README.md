# Seminario2026
# Seminario de Actualización

Este proyecto consiste en una aplicación web sencilla desarrollada con Gradio que recibe un nombre del usuario y devuelve un saludo personalizado.

## Clases

- [Clase 5 - Publicación y documentación](Clase%205/README.md): deploy de la app Gradio en Render, versión equivalente en Streamlit y documentación de la entrega.

## Objetivo

Demostrar el uso básico de Gradio para crear interfaces de usuario simples y funcionales en Python, con una experiencia visual amigable y rápida de ejecutar.

## Requisitos

- Python 3.9 o superior
- pip

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```powershell
python app.py
```

Luego abre la siguiente URL en tu navegador:

http://127.0.0.1:7860

## Clase 5: versión Streamlit

```powershell
streamlit run ".\Clase 5\streamlit_app.py"
```

Luego abrir `http://localhost:8501`.

## Descripción funcional

La aplicación presenta un campo de texto donde el usuario ingresa su nombre. Al enviar la información, la interfaz devuelve un mensaje de saludo, como por ejemplo:

- Entrada: "Ana"
- Salida: "Hello Ana!"

## Autor

Proyecto realizado para el seminario de actualización.
# prueba-git-sync
