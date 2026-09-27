import streamlit as st


import os

import streamlit as st
from huggingface_hub import InferenceClient


MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"


@st.cache_resource
def crear_cliente(token):
    return InferenceClient(provider="hf-inference", api_key=token)


def saludar(nombre):
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para recibir un saludo."
    return f"¡Hola {nombre}! Bienvenido a Streamlit."


st.set_page_config(page_title="Saludo en Streamlit", page_icon="👋")
st.title("Mi primera app con Streamlit")
st.write("Ingresá tu nombre para recibir un saludo personalizado.")

nombre = st.text_input("Tu nombre")

if st.button("Saludar"):
    st.success(saludar(nombre))

st.subheader("Análisis de sentimiento")
texto = st.text_input("Escribí un texto")

if st.button("Analizar"):
    try:
        token = st.secrets.get("HF_TOKEN")
    except FileNotFoundError:
        token = None
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        st.error("Falta configurar HF_TOKEN en Secrets o variables de entorno.")
    elif not texto.strip():
        st.warning("Escribí un texto para analizar.")
    else:
        cliente = crear_cliente(token)
        resultado = cliente.text_classification(
            texto,
            model=MODEL_NAME,
            top_k=3,
        )
        st.write({item.label: round(item.score, 3) for item in resultado})