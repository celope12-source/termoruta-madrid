import networkx as nx
import osmnx as ox

def cargar_grafo_getafe():
    """Genera la red peatonal base del centro de Getafe en memoria sin conexiones externas."""
    G = nx.MultiDiGraph()
    G.graph["crs"] = "epsg:4326"

    # Coordenadas reales de calles y plazas del centro de Getafe
    puntos = {
        1: (40.3082, -3.7324),  # Getafe Central / Cercanías
        2: (40.3073, -3.7319),  # Calle Madrid Norte
        3: (40.3065, -3.7315),  # Calle Madrid Centro
        4: (40.3056, -3.7311),  # Plaza de la Constitución (Ayuntamiento)
        5: (40.3048, -3.7307),  # Calle Madrid Sur
        6: (40.3060, -3.7340),  # Calle Toledo / Parque Escolapios
        7: (40.3072, -3.7335),  # Calle Jardines
        8: (40.3049, -3.7326),  # Calle Hospital
    }

    for n, (lat, lon) in puntos.items():
        G.add_node(n, y=lat, x=lon)

    # Conexiones peatonales en doble sentido (MultiDiGraph)
    aristas = [
        (1, 2, 110.0), (2, 1, 110.0),
        (2, 3, 100.0), (3, 2, 100.0),
        (3, 4, 115.0), (4, 3, 115.0),
        (4, 5, 105.0), (5, 4, 105.0),
        (1, 7, 140.0), (7, 1, 140.0),
        (7, 6, 150.0), (6, 7, 150.0),
        (6, 4, 145.0), (4, 6, 145.0),
        (4, 8, 90.0),  (8, 4, 90.0),
        (8, 5, 120.0), (5, 8, 120.0),
        (2, 7, 130.0), (7, 2, 130.0),
        (3, 6, 125.0), (6, 3, 125.0)
    ]

    for u, v, longitud in aristas:
        G.add_edge(u, v, key=0, length=longitud, coste_termico=longitud)

    return G

def calcular_rutas(G, origen_coords, destino_coords, modo="verano"):
    """Calcula la ruta más corta directa frente a la TermoRuta."""
    nodo_origen = ox.nearest_nodes(G, X=origen_coords[1], Y=origen_coords[0])
    nodo_destino = ox.nearest_nodes(G, X=destino_coords[1], Y=destino_coords[0])

    ruta_corta = nx.shortest_path(G, nodo_origen, nodo_destino, weight="length")

    # Modulación de costes térmicos
    for u, v, k, data in G.edges(keys=True, data=True):
        longitud = data.get("length", 1.0)
        # La avenida principal (eje Calle Madrid: 1-2-3-4-5) está expuesta al sol en verano
        if modo == "verano" and {u, v}.issubset({1, 2, 3, 4, 5}):
            data["coste_termico"] = longitud * 3.5  # Penalización alta por radiación directa
        elif modo == "verano":
            data["coste_termico"] = longitud * 0.8  # Calles sombreadas y arboladas
        else:
            data["coste_termico"] = longitud

    termo_ruta = nx.shortest_path(G, nodo_origen, nodo_destino, weight="coste_termico")

    puntos_corta = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in ruta_corta]
    puntos_termo = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in termo_ruta]

    return puntos_corta, puntos_termo