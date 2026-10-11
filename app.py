import streamlit as st
import folium
from streamlit_folium import st_folium
from enrutador import cargar_grafo_getafe, calcular_rutas

st.set_page_config(page_title="TermoRuta Madrid", layout="wide")

st.title("☀️ TermoRuta Madrid: Navegador Peatonal")
st.markdown("Prototipo para el Datathon — Zona piloto: **Getafe**")

with st.sidebar:
    st.header("Configuración")
    modo = st.selectbox(
        "Modo de confort:",
        ["Verano Fresco (Sombra y Fuentes)", "Invierno Soleado", "Mascotas (Asfalto Frío)"]
    )
    hora = st.slider("Hora del trayecto:", min_value=8, max_value=21, value=15, step=1)
    boton_calcular = st.button("Calcular Ruta", type="primary")

@st.cache_resource
def obtener_grafo():
    return cargar_grafo_getafe()

with st.spinner("Descargando/cargando calles de Getafe..."):
    G = obtener_grafo()

# Coordenadas piloto en Getafe
origen = (40.3082, -3.7324)   # Cerca de Getafe Central
destino = (40.3056, -3.7311)  # Cerca de Plaza de la Constitución

m = folium.Map(location=[40.3070, -3.7318], zoom_start=16)
folium.Marker(origen, tooltip="Origen", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(destino, tooltip="Destino", icon=folium.Icon(color="red")).add_to(m)

if boton_calcular:
    modo_clave = "verano" if "Verano" in modo else "invierno"
    ruta_corta, ruta_fresca = calcular_rutas(G, origen, destino, modo=modo_clave)

    folium.PolyLine(ruta_corta, color="red", weight=4, opacity=0.6, tooltip="Ruta más corta").add_to(m)
    folium.PolyLine(ruta_fresca, color="blue", weight=5, opacity=0.9, tooltip="TermoRuta").add_to(m)
    st.success("¡Ruta calculada!")

st_folium(m, width=900, height=500)