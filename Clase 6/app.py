import os
import gradio as gr

def saludar(nombre):
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para recibir un saludo."
    return f"¡Hola {nombre}! Bienvenido a Gradio."

def verificar_edad(edad):
    edad = int(edad)
    if edad >= 18:
        return f"Tienes {edad} años, ¡ya eres mayor de edad!"
    return f"Tienes {edad} años, aún eres menor de edad."

with gr.Blocks() as demo:
    gr.Markdown("# Mi primera app con Gradio")

    gr.Markdown("### 1. Saludo básico")
    nombre = gr.Textbox(label="Escribí tu nombre")
    boton_saludo = gr.Button("Saludar")
    salida_saludo = gr.Textbox(label="Resultado")
    boton_saludo.click(fn=saludar, inputs=nombre, outputs=salida_saludo)

    gr.Markdown("---")
    gr.Markdown("### 2. Componente nuevo y función propia")
    edad = gr.Slider(minimum=0, maximum=100, step=1, label="¿Cuántos años tienes?")
    boton_edad = gr.Button("Verificar Edad")
    salida_edad = gr.Textbox(label="Resultado")
    boton_edad.click(fn=verificar_edad, inputs=edad, outputs=salida_edad)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )