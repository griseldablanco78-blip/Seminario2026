import os
import gradio as gr


def saludar(nombre):
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para recibir un saludo."
    return f"¡Hola {nombre}! Bienvenido a Gradio."


with gr.Blocks() as demo:
    gr.Markdown("# Mi primera app con Blocks")

    nombre = gr.Textbox(label="Tu nombre")
    boton = gr.Button("Saludar")
    salida = gr.Textbox(label="Resultado")

    boton.click(fn=saludar, inputs=nombre, outputs=salida)


if __name__ == "__main__":
    launch_config = {
        "server_name": "0.0.0.0",
        "share": False,
    }
    if "PORT" in os.environ:
        launch_config["server_port"] = int(os.environ["PORT"])

    demo.launch(**launch_config)
