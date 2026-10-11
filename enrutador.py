import networkx as nx
import osmnx as ox

def cargar_grafo_getafe():
    """Descarga la red peatonal de Getafe."""
    lugar = "Getafe, Madrid, Spain"
    G = ox.graph_from_place(lugar, network_type="walk")
    return G

def calcular_rutas(G, origen_coords, destino_coords, modo="verano"):
    """Calcula la ruta más corta frente a la TermoRuta."""
    nodo_origen = ox.nearest_nodes(G, X=origen_coords[1], Y=origen_coords[0])
    nodo_destino = ox.nearest_nodes(G, X=destino_coords[1], Y=destino_coords[0])

    ruta_corta = nx.shortest_path(G, nodo_origen, nodo_destino, weight="length")

    for u, v, k, data in G.edges(keys=True, data=True):
        longitud = data.get("length", 1.0)
        if modo == "verano":
            data["coste_termico"] = longitud * 1.5
        else:
            data["coste_termico"] = longitud

    termo_ruta = nx.shortest_path(G, nodo_origen, nodo_destino, weight="coste_termico")

    puntos_corta = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in ruta_corta]
    puntos_termo = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in termo_ruta]

    return puntos_corta, puntos_termo