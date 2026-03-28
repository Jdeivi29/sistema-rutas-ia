import heapq
import networkx as nx
import matplotlib.pyplot as plt

# =========================
# BASE DE CONOCIMIENTO (GRAFO)
# =========================

grafo = {
    "Portal Norte": {"Toberin": 3},
    "Toberin": {"Portal Norte": 3, "Calle 106": 2},
    "Calle 106": {"Toberin": 2, "Calle 100": 2},
    "Calle 100": {"Calle 106": 2, "Calle 94": 2},
    "Calle 94": {"Calle 100": 2, "Calle 85": 2},
    "Calle 85": {"Calle 94": 2, "Heroes": 2},
    "Heroes": {"Calle 85": 2, "Calle 76": 2},
    "Calle 76": {"Heroes": 2, "Calle 72": 2},
    "Calle 72": {"Calle 76": 2, "Flores": 2},
    "Flores": {"Calle 72": 2, "Calle 63": 2},
    "Calle 63": {"Flores": 2, "Calle 57": 2},
    "Calle 57": {"Calle 63": 2, "Calle 45": 3},
    "Calle 45": {"Calle 57": 3, "Av Jimenez": 3},

    "Av Jimenez": {"Calle 45": 3, "Calle 26": 2, "Restrepo": 4},
    "Calle 26": {"Av Jimenez": 2, "Universidades": 2, "Salitre": 3},

    "Universidades": {"Calle 26": 2, "Las Aguas": 2},
    "Las Aguas": {"Universidades": 2},

    "Restrepo": {"Av Jimenez": 4, "Fucha": 3},
    "Fucha": {"Restrepo": 3, "Portal Sur": 5},
    "Portal Sur": {"Fucha": 5},

    "Salitre": {"Calle 26": 3, "El Tiempo": 2},
    "El Tiempo": {"Salitre": 2, "Modelia": 3},
    "Modelia": {"El Tiempo": 3, "Portal Eldorado": 5},
    "Portal Eldorado": {"Modelia": 5}
}

# =========================
# HEURÍSTICA (estimación)
# =========================

heuristica = {
    "Portal Norte": 20,
    "Toberin": 18,
    "Calle 106": 17,
    "Calle 100": 16,
    "Calle 94": 15,
    "Calle 85": 14,
    "Heroes": 13,
    "Calle 76": 12,
    "Calle 72": 11,
    "Flores": 10,
    "Calle 63": 9,
    "Calle 57": 8,
    "Calle 45": 7,
    "Av Jimenez": 6,
    "Calle 26": 5,
    "Universidades": 4,
    "Las Aguas": 3,
    "Restrepo": 4,
    "Fucha": 2,
    "Portal Sur": 0,
    "Salitre": 6,
    "El Tiempo": 7,
    "Modelia": 8,
    "Portal Eldorado": 9
}

# =========================
# NORMALIZAR TEXTO
# =========================

def normalizar(texto):
    return texto.strip().title()

# =========================
# ALGORITMO A*
# =========================

def a_estrella(grafo, inicio, fin):
    cola = []
    heapq.heappush(cola, (0, inicio))

    costos = {inicio: 0}
    padres = {inicio: None}

    while cola:
        _, actual = heapq.heappop(cola)

        if actual == fin:
            break

        for vecino, peso in grafo[actual].items():
            nuevo_costo = costos[actual] + peso

            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                prioridad = nuevo_costo + heuristica.get(vecino, 0)
                heapq.heappush(cola, (prioridad, vecino))
                padres[vecino] = actual

    ruta = []
    nodo = fin

    while nodo:
        ruta.append(nodo)
        nodo = padres.get(nodo)

    return ruta[::-1], costos.get(fin, float('inf'))

# =========================
# DIBUJAR GRAFO + RUTA
# =========================

def dibujar_grafo(grafo, ruta=None):
    G = nx.Graph()

    for nodo in grafo:
        for vecino, peso in grafo[nodo].items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(14, 10))

    # Dibujar grafo base
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=8)

    # Dibujar pesos
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    # Resaltar ruta
    if ruta:
        edges_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_ruta, width=4)

    plt.title("Sistema Inteligente de Rutas (IA)")
    plt.show()

# =========================
# INTERFAZ
# =========================

print("\n=== SISTEMA DE RUTAS TRANSMILENIO ===")

print("\nEstaciones disponibles:")
for estacion in grafo:
    print("-", estacion)

inicio = normalizar(input("\nIngrese punto de inicio: "))
fin = normalizar(input("Ingrese punto de destino: "))

if inicio not in grafo or fin not in grafo:
    print("\nError: estación no válida")
else:
    ruta, costo = a_estrella(grafo, inicio, fin)

    print("\nRuta óptima:")
    print(" -> ".join(ruta))
    print("Costo total:", costo)

    dibujar_grafo(grafo, ruta)