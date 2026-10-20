# Clase 05: Deploy de Aplicaciones con Gradio y Streamlit

En esta clase se desarrollaron y desplegaron dos aplicaciones web interactivas en Python utilizando **Gradio** y **Streamlit**, publicándolas en la nube mediante **Render**.

---

## 🌐 Enlaces a las Aplicaciones Publicadas

- **Gradio en Render:** [https://tu-app-gradio.onrender.com](https://github.com/griseldablanco78-blip/Seminario2026)
- **Streamlit en Render:** [https://tu-app-streamlit.onrender.com](https://seminario2026-clase5.streamlit.app/)

---

## 📱 ¿Qué hace cada aplicación?

### 1. Aplicación con Gradio (`app.py`)
Utiliza la interfaz `gr.Blocks()` para construir un panel interactivo con dos secciones:
1. **Saludo básico:** Un cuadro de texto (`gr.Textbox`) donde el usuario ingresa su nombre. Al hacer clic en **"Saludar"**, procesa el texto y retorna un saludo de bienvenida. Si está vacío, solicita que se ingrese un nombre.
2. **Verificación de Edad:** Un control deslizante (`gr.Slider`) que permite elegir una edad entre 0 y 100 años. Al presionar **"Verificar Edad"**, la función evalúa si la persona es mayor o menor de 18 años y muestra el resultado en un cuadro de salida.

### 2. Aplicación con Streamlit (`streamlit_app.py`)
Implementa las mismas funcionalidades de manera ágil y secuencial:
1. **Saludo básico:** Entrada de texto con `st.text_input` y botón `st.button("Saludar")` que imprime el saludo en pantalla.
2. **Verificación de Edad:** Selector deslizante con `st.slider` y botón `st.button("Verificar Edad")` que valida e informa si el usuario es mayor o menor de edad.

---

## 🔍 Diferencias entre Gradio y Streamlit

1. **Paradigma de ejecución:** Streamlit vuelve a ejecutar todo el script de arriba hacia abajo cada vez que el usuario interactúa con algún control (enfoque declarativo lineal), mientras que Gradio utiliza un modelo reactivo basado en eventos y funciones de retorno (*callbacks* con `boton.click(fn=...)`), ejecutando únicamente la función asociada al evento sin recargar toda la interfaz.
2. **Definición de interfaz:** En Gradio es necesario planificar los componentes vinculando explícitamente sus entradas (`inputs`) y salidas (`outputs`), mientras que en Streamlit los componentes se dibujan secuencialmente y devuelven su valor de forma inmediata en variables normales de Python.
3. **Despliegue y comandos de arranque:** En Render, Gradio se ejecuta directamente como un script estándar (`python app.py`) leyendo `PORT` y escuchando en `0.0.0.0`, mientras que Streamlit requiere su propio comando de línea (`streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`).

---

## ⚙️ Configuración para Deploy en Render

Ambas aplicaciones utilizan el archivo `requirements.txt` con las dependencias necesarias:
```text
gradio
streamlit
```

### Configuración en Render para Gradio:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`
- **Root Directory:** `Clase 5` (o ruta relativa correspondiente según el repositorio)
- **Ajuste de puerto:** Configurado en `app.py` mediante:
  ```python
  demo.launch(
      server_name="0.0.0.0",
      server_port=int(os.environ.get("PORT", 7860)),
  )
  ```

### Configuración en Render para Streamlit:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- **Root Directory:** `Clase 5`