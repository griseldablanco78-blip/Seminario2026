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
