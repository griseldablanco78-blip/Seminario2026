# Clase 5 - Publicación y documentación de aplicaciones Python

## Entrega

- **Deploy Gradio en Render:** https://seminario2026-9xol.onrender.com
- **Deploy Streamlit:** https://seminario2026-clase5.streamlit.app

La entrega se presenta mediante el repositorio de GitHub:

https://github.com/griseldablanco78-blip/Seminario2026

## Objetivo
Publicar una aplicación Python con Gradio y preparar una versión equivalente, mínima, con Streamlit. Las dos aplicaciones reciben un nombre y devuelven un saludo personalizado.

## Requisitos
- Python 3.9 o superior
- pip
- Cuenta en GitHub
- Cuenta en Render
- Cuenta en un servicio de deploy compatible con Streamlit

## Instalación
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución local: Gradio
```powershell
python app.py
```
Luego abrir en el navegador la URL que muestre Gradio, normalmente:

La terminal mostrará el puerto disponible, por ejemplo:

http://localhost:7865

## Importante para Render
La app usa la variable de entorno `PORT` para que Render pueda asignar el puerto correcto:

```python
server_port=int(os.environ.get("PORT", 7860))
```

## Qué hace la app
- Tiene un campo para escribir el nombre
- Tiene un botón para saludar
- Muestra el resultado en pantalla
- Usa `gr.Blocks`

## Ejecución local: Streamlit

Desde la raíz del repositorio:

```powershell
streamlit run ".\Clase 5\streamlit_app.py"
```

Luego abrir:

http://localhost:8501

La versión Streamlit mantiene el mismo flujo funcional, pero cambia la forma de construir la interfaz: Gradio conecta componentes mediante eventos, mientras Streamlit ejecuta el script y muestra los componentes en orden.

## Deploy de Gradio en Render
1. Crear cuenta en Render
2. Crear un Web Service
3. Conectar el repositorio de GitHub
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Esperar a que termine el deploy
6. Usar la URL pública que te da Render

Para este repositorio:

- Build Command: `pip install -r requirements.txt`
- Start Command: `python "Clase 5/app.py"`

## Deploy de Streamlit

Crear una segunda aplicación en un servicio compatible con Streamlit y configurar:

- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run "Clase 5/streamlit_app.py" --server.address 0.0.0.0 --server.port $PORT`

Si el servicio usa una configuración distinta para la variable de puerto, se debe seleccionar el puerto indicado por la plataforma.

## Archivos relevantes
- `app.py`: aplicación principal con Gradio
- `streamlit_app.py`: equivalente mínimo en Streamlit
- `requirements.txt`: dependencias necesarias
