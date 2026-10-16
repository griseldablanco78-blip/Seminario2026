import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="Expensa House - Dashboard", page_icon="🏠", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("🏠 Expensa House - Análisis Exploratorio y Dashboard")
st.markdown("Bienvenido al panel de control de Expensa House. Aquí analizamos los datos de inventario y compras familiares.")

# Carga de datos
@st.cache_data
def load_data():
    path = "data/inventario_movimientos_limpio.csv"
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.day_name()
    return df

df = load_data()

if df is not None:
    # --- KPIs ---
    st.header("📊 Métricas Generales")
    col1, col2, col3, col4 = st.columns(4)
    
    compras_df = df[df['tipo_movimiento'] == 'Compra']
    gasto_total = (compras_df['cantidad'] * compras_df['precio']).sum()
    total_productos = df['producto'].nunique()
    total_movimientos = len(df)
    
    with col1:
        st.markdown(f"<div class='metric-card'><h3>Gasto Total Estimado</h3><h2>${gasto_total:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>Prod. Distintos</h3><h2>{total_productos}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>Total Movimientos</h3><h2>{total_movimientos}</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><h3>Modelo predictivo</h3><h2>Inactivo</h2></div>", unsafe_allow_html=True)
        
    st.divider()

    # --- Hipótesis ---
    st.header("🔍 Análisis de Hipótesis (EDA)")
    
    tab1, tab2, tab3 = st.tabs(["H1: Categorías y Reposición", "H2: Stock Crítico y Presupuesto", "H3: Consumo por Día"])
    
    with tab1:
        st.subheader("Las categorías básicas concentran las reposiciones")
        # Gráfico de barras de frecuencias de compra por categoría
        freq_cat = compras_df.groupby('categoria').size().reset_index(name='Frecuencia')
        freq_cat = freq_cat.sort_values(by='Frecuencia', ascending=False)
        fig = px.bar(freq_cat, x='categoria', y='Frecuencia', color='categoria', title="Frecuencia de Compras por Categoría")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** Las categorías superiores representan la mayor parte de las compras recurrentes, lo que valida nuestra hipótesis y sugiere que el foco de automatización debe estar allí.")
        
    with tab2:
        st.subheader("Gasto concentrado en pocos productos")
        # Gasto por producto
        gasto_prod = compras_df.copy()
        gasto_prod['gasto'] = gasto_prod['cantidad'] * gasto_prod['precio']
        gasto_prod = gasto_prod.groupby('producto')['gasto'].sum().reset_index().sort_values(by='gasto', ascending=False).head(10)
        fig2 = px.pie(gasto_prod, values='gasto', names='producto', title="Top 10 Productos con Mayor Gasto Acumulado")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Insight:** Identificando estos productos críticos, podemos generar alertas predictivas para aprovechar descuentos antes de que se agote el stock.")
        
    with tab3:
        st.subheader("Volumen de consumo según día de la semana")
        consumo_df = df[df['tipo_movimiento'] == 'Consumo']
        orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dia_consumo = consumo_df.groupby('dia_semana').size().reindex(orden_dias).reset_index(name='Cantidad')
        fig3 = px.line(dia_consumo, x='dia_semana', y='Cantidad', markers=True, title="Tendencia de Consumo Semanal")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Insight:** Observamos picos de consumo en días específicos, lo cual es vital para el modelo de ML que predecirá el agotamiento de stock.")

    st.divider()
    
    # --- Boti House ---
    st.header("🤖 Boti House (Chatbot IA)")
    st.markdown("Asistente virtual de Expensa House. *Escribe tu consulta abajo:*")
    
    # Simple UI de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Ej: ¿Qué productos faltan en la despensa?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Respuesta simulada por ahora
        respuesta = "¡Hola! Soy Boti House. En este momento el modelo NLP se está integrando, pero pronto podré buscar ofertas y consultar tu stock."
        with st.chat_message("assistant"):
            st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

else:
    st.warning("⚠️ No se encontró el dataset limpio. Por favor, ejecuta primero el script de generación y limpieza de datos.")
