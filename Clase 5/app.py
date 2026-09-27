import os

import gradio as gr
from huggingface_hub import InferenceClient

MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"


def saludar(nombre):
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para recibir un saludo."
    return f"¡Hola {nombre}! Bienvenido a Gradio."


def analizar_sentimiento(texto):
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise gr.Error("Falta configurar HF_TOKEN en el entorno de la aplicación.")

    texto = texto.strip()
    if not texto:
        raise gr.Error("Escribí un texto para analizar.")

    client = InferenceClient(provider="hf-inference", api_key=token)
    resultado = client.text_classification(
        texto,
        model=MODEL_NAME,
        top_k=3,
    )
    return {item.label: item.score for item in resultado}


with gr.Blocks() as demo:
    gr.Markdown("# Mi primera app con Blocks")

    nombre = gr.Textbox(label="Tu nombre")
    boton = gr.Button("Saludar")
    salida = gr.Textbox(label="Resultado")

    boton.click(fn=saludar, inputs=nombre, outputs=salida)

    with gr.Tab("Análisis de sentimiento"):
        texto = gr.Textbox(label="Escribí un texto")
        boton_sentimiento = gr.Button("Analizar")
        salida_sentimiento = gr.Label(label="Resultado")
        boton_sentimiento.click(
            analizar_sentimiento,
            inputs=texto,
            outputs=salida_sentimiento,
        )


if __name__ == "__main__":
    launch_config = {
        "server_name": "0.0.0.0",
        "share": False,
    }
    if "PORT" in os.environ:
        launch_config["server_port"] = int(os.environ["PORT"])

    demo.launch(**launch_config)
