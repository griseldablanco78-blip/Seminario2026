import streamlit as st

st.title("Mi primera app con Streamlit")

st.markdown("### 1. Saludo básico")
nombre = st.text_input("Escribí tu nombre")

if st.button("Saludar"):
    if not nombre.strip():
        st.write("Escribí tu nombre para recibir un saludo.")
    else:
        st.write(f"¡Hola {nombre.strip()}! Bienvenido a Streamlit.")

st.markdown("---")
st.markdown("### 2. Componente nuevo y función propia")
edad = st.slider("¿Cuántos años tienes?", min_value=0, max_value=100, step=1)

if st.button("Verificar Edad"):
    if edad >= 18:
        st.write(f"Tienes {edad} años, ¡ya eres mayor de edad!")
    else:
        st.write(f"Tienes {edad} años, aún eres menor de edad.")
