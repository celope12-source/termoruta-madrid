from enrutador import calcular_rutas, cargar_grafo_getafe
import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="TermoRuta Madrid", layout="wide")

st.title("☀️ TermoRuta Madrid: Navegador Peatonal")
st.markdown("Prototipo para el Datathon — Zona piloto: **Getafe**")

# 1. Inicializar la memoria de sesión para que las rutas no se borren
if "rutas_calculadas" not in st.session_state:
  st.session_state.rutas_calculadas = None

with st.sidebar:
  st.header("Configuración")
  modo = st.selectbox(
      "Modo de confort:",
      [
          "Verano Fresco (Sombra y Fuentes)",
          "Invierno Soleado",
          "Mascotas (Asfalto Frío)",
      ],
  )
  hora = st.slider(
      "Hora del trayecto:", min_value=8, max_value=21, value=15, step=1
  )
  boton_calcular = st.button("Calcular Ruta", type="primary")


@st.cache_resource
def obtener_grafo():
  return cargar_grafo_getafe()


G = obtener_grafo()

# Coordenadas fijas de prueba en Getafe
origen = (40.3082, -3.7324)  # Getafe Central
destino = (40.3048, -3.7307)  # Calle Madrid Sur

# 2. Si se pulsa el botón, guardamos las rutas en la memoria permanente
if boton_calcular:
  modo_clave = "verano" if "Verano" in modo else "invierno"
  ruta_corta, ruta_fresca = calcular_rutas(G, origen, destino, modo=modo_clave)
  st.session_state.rutas_calculadas = {
      "corta": ruta_corta,
      "fresca": ruta_fresca,
  }

# 3. Dibujar el mapa base
m = folium.Map(location=[40.3065, -3.7315], zoom_start=16)
folium.Marker(
    origen,
    tooltip="Origen: Getafe Central",
    icon=folium.Icon(color="green", icon="play"),
).add_to(m)
folium.Marker(
    destino,
    tooltip="Destino: Calle Madrid",
    icon=folium.Icon(color="red", icon="flag"),
).add_to(m)

# 4. Si hay rutas calculadas guardadas en sesión, las pintamos para que permanezcan fijas
if st.session_state.rutas_calculadas is not None:
  rc = st.session_state.rutas_calculadas["corta"]
  rf = st.session_state.rutas_calculadas["fresca"]

  folium.PolyLine(
      rc,
      color="red",
      weight=4,
      opacity=0.7,
      tooltip="Ruta convencional (al sol)",
  ).add_to(m)
  folium.PolyLine(
      rf, color="blue", weight=6, opacity=0.9, tooltip="TermoRuta recomendada"
  ).add_to(m)

  st.success("¡Ruta calculada con éxito!")

# 5. Renderizar el mapa interactivo
st_folium(m, width=950, height=520, returned_objects=[])