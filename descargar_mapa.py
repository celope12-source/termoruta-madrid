import osmnx as ox

print("Probando descarga del núcleo histórico de Getafe...")

# 1. Configurar servidor alternativo rápido y timeout amplio
ox.settings.timeout = 180
ox.settings.overpass_endpoint = "https://maps.mail.ru/osm/tools/overpass/api/interpreter"

# Si falla el primero, otros endpoints fiables:
# "https://overpass.kumi.systems/api/interpreter"
# "https://overpass-api.de/api/interpreter"

# 2. Coordenadas de la Plaza de la Constitución de Getafe
centro_getafe = (40.3056, -3.7311)

try:
    # Radio pequeño de 800m: descarga muy rápida y ligera (~3-5 MB)
    G = ox.graph_from_point(centro_getafe, dist=800, network_type="walk", simplify=True)
    ox.save_graphml(G, "getafe_centro.graphml")
    print("¡ÉXITO! Archivo 'getafe_centro.graphml' creado correctamente en disco.")
except Exception as e:
    print(f"Error con endpoint principal: {e}")
    print("Reintentando con endpoint de respaldo...")
    ox.settings.overpass_endpoint = "https://overpass.kumi.systems/api/interpreter"
    G = ox.graph_from_point(centro_getafe, dist=800, network_type="walk", simplify=True)
    ox.save_graphml(G, "getafe_centro.graphml")
    print("¡ÉXITO! Guardado en disco con endpoint de respaldo.")