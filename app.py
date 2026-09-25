import os

import gradio as gr


def saludar(nombre):
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para recibir un saludo."
    return f"¡Hola {nombre}! Bienvenido a Gradio."


def clasificar_edad(edad):
    if edad >= 18:
        return f"Tienes {edad} años, ¡ya eres mayor de edad!"
    else:
        return f"Tienes {edad} años, aún eres menor de edad."


with gr.Blocks() as demo:
    gr.Markdown("# Mi primera app con Blocks")

    nombre = gr.Textbox(label="Escribí tu nombre")
    boton = gr.Button("Saludar")
    salida = gr.Textbox(label="Resultado")

    boton.click(fn=saludar, inputs=nombre, outputs=salida)

    gr.Markdown("### 2. Componente nuevo y función propia")
    edad_input = gr.Slider(minimum=0, maximum=100, step=1, label="¿Cuántos años tienes?")
    boton_edad = gr.Button("Verificar Edad")
    salida_edad = gr.Textbox(label="Resultado de edad")

    boton_edad.click(fn=clasificar_edad, inputs=edad_input, outputs=salida_edad)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=True,
    )
