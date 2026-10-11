## Aplicación con Gradio

### 1. Código en `app.py`

Se crea el archivo `app.py` con una aplicación sencilla hecha con Gradio (`gr.Blocks`). Recibe un nombre y devuelve un saludo.

```python
import gradio as gr

def saludar(nombre):
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para recibir un saludo."
    return f"¡Hola {nombre}! Bienvenido a Gradio."

with gr.Blocks() as demo:
    gr.Markdown("# Mi primera app con Blocks")

    nombre = gr.Textbox(label="Escribí tu nombre")
    boton = gr.Button("Saludar")
    salida = gr.Textbox(label="Resultado")

    boton.click(fn=saludar, inputs=nombre, outputs=salida)

if __name__ == "__main__":
    demo.launch(share=False)
```

**Cómo funciona:**
- `saludar(nombre)`: limpia los espacios del texto con `strip()`. Si queda vacío, pide que se escriba un nombre; si no, devuelve el saludo.
- `gr.Blocks()`: define la interfaz, donde se ubican el título, el cuadro de entrada, el botón y el cuadro de salida.
- `boton.click(...)`: conecta el botón con la función. Toma el texto de `nombre` y muestra el resultado en `salida`.
- `demo.launch(share=False)`: inicia la app solo de forma local, sin generar un enlace público.

### 2. Creación del espacio de trabajo y ejecución

Se crea el entorno de trabajo, se instala Gradio y se ejecuta la aplicación:

```bash
python -m venv virtual
virtual\Scripts\activate        # En Linux/Mac: source virtual/bin/activate
pip install gradio
python app.py
```

Gradio muestra en la terminal la dirección local, normalmente `http://127.0.0.1:7860`. Al abrirla en el navegador se ve la interfaz y se puede probar el saludo.

https://huggingface.co/spaces/grisselblanco/seminario-2026