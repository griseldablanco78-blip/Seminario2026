# Clase 6 - Consumir un modelo de IA por API

## Modelo utilizado

`cardiffnlp/twitter-xlm-roberta-base-sentiment`

La aplicación analiza el sentimiento de un texto usando `InferenceClient` de `huggingface_hub`.

## Aplicaciones publicadas

- **Gradio en Render:** https://seminario2026-9xol.onrender.com
- **Streamlit Community Cloud:** https://seminario2026-clase5.streamlit.app

## Configuración segura del token

El token nunca se guarda en el código ni en GitHub.

En Render se configura como variable de entorno:

```text
HF_TOKEN=tu_token_de_hugging_face
```

En Streamlit Community Cloud se configura en **Settings > Secrets**:

```toml
HF_TOKEN = "tu_token_de_hugging_face"
```

Para probar localmente en PowerShell, durante la sesión actual:

```powershell
$env:HF_TOKEN = "tu_token_de_hugging_face"
```

No subir el token al repositorio. Si se necesita guardar un secreto local, usar `.streamlit/secrets.toml` y mantenerlo fuera de Git.

## Ejecución local

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Ejecutar Gradio:

```powershell
python ".\Clase 5\app.py"
```

Ejecutar Streamlit:

```powershell
streamlit run ".\Clase 5\streamlit_app.py"
```

Escribir un texto y presionar **Analizar**. Se mostrarán las tres etiquetas más probables y sus puntajes.

## Errores frecuentes

- `KeyError: HF_TOKEN`: falta definir la variable en esa terminal o servicio.
- `401 Unauthorized`: el token es incorrecto o no tiene permiso **Inference Providers**.
- Error de conexión: revisar que el servicio tenga acceso a Internet y que el modelo esté disponible.

## Revisión de pares

**Repositorio revisado:** https://github.com/AraceliAmherdt/Proyecto_seminario

| Criterio | Resultado |
|---|---|
| README general | Sí. Documenta el proyecto, instalación, uso y publicación. |
| Una carpeta por clase | No se observa una separación completa por carpetas de clase; la aplicación principal está en la raíz. |
| Reproducibilidad | Parcial. El estado final está documentado, pero no hay una entrega independiente por cada clase. |
| Ejecución local | No se pudo completar en un entorno limpio porque `app.py` importa `spaces`, que no estaba disponible. |
| Historial de commits | Sí. El historial muestra evolución del proyecto y correcciones sucesivas. |

### Problema concreto encontrado

Al intentar ejecutar `app.py` en un entorno local limpio apareció:

```text
ModuleNotFoundError: No module named 'spaces'
```

Esto ocurre porque el proyecto utiliza `import spaces` y `@spaces.GPU`, una dependencia específica del entorno de Hugging Face que no estaba instalada en el entorno local revisado.