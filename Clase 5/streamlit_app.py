import streamlit as st


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