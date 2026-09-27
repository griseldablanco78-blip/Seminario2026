# Seminario2026
# Seminario de Actualización

Este proyecto consiste en una aplicación web sencilla desarrollada con Gradio que recibe un nombre del usuario y devuelve un saludo personalizado.

## Clases

- [Clase 5 - Publicación y documentación](Clase%205/README.md): deploy de la app Gradio en Render, versión equivalente en Streamlit y documentación de la entrega.
- [Clase 6 - Revisión de Repositorio](Clase%206/README.md): Análisis y evaluación del código y repositorio de un compañero.
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

---

## Clase 6 - Revisión de Repositorio de un Compañero

**Link del repositorio:** https://github.com/AraceliAmherdt/Proyecto_seminario

### Evaluación según la rúbrica

1. **¿Tiene README general?**
   - Sí. Cuenta con un README detallado que incluye la descripción del proyecto, los links a GitHub y Hugging Face Spaces, los requisitos, y las instrucciones para instalación, uso local y publicación de cambios.

2. **¿Tiene una carpeta por clase?**
   - No. El repositorio no está organizado en carpetas por clases. Todos los archivos (`app.py`, `requirements.txt`, `README.md`) se encuentran sueltos en la raíz del proyecto.

3. **¿Alcanza para reproducir cada clase?**
   - No es posible reproducir cada clase individualmente porque no hay separación del historial de tareas, pero sí alcanza para reproducir el estado final de la aplicación siguiendo los pasos descritos en su README.

4. **¿Pudiste correr algo?**
   - Intenté correr el proyecto localmente (`python app.py`), pero no funcionó debido a que el proyecto está preparado para ejecutarse en Hugging Face con aceleración gráfica (ZeroGPU), lo cual requiere librerías específicas que no vienen por defecto en un entorno normal. 

5. **¿El historial de commits muestra el progreso?**
   - Sí. El comando `git log` muestra un historial claro de 8 commits, desde el "Commit inicial", la configuración para Hugging Face, la adaptación a ZeroGPU y la corrección de errores en Gradio 6.

### Problema concreto encontrado

Al intentar correr el archivo `app.py` de forma local, me encontré con el siguiente error en la terminal:

```bash
Traceback (most recent call last):
  File "C:\Users\grise\Proyectos\Tercer Año\Proyecto_seminario\app.py", line 4, in <module>
    import spaces
ModuleNotFoundError: No module named 'spaces'
```

**Motivo:** El código utiliza la línea `import spaces` y el decorador `@spaces.GPU`. Esta es una librería exclusiva de los servidores de Hugging Face Spaces diseñada para usar Tarjetas Gráficas (GPU). Al correrlo localmente en una PC que no tiene instalada esa librería, Python arroja un error `ModuleNotFoundError`.
