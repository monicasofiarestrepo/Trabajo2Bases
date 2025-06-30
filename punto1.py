from pymongo import MongoClient
from neo4j import GraphDatabase
import heapq
from contraseña import NEO4J_PASSWORD

mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["viajes_db"]


neo4j_driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", NEO4J_PASSWORD))

# grafo desde Neo4j en memoria
def construir_grafo(peso_key):
    grafo = {}
    with neo4j_driver.session() as session:
        result = session.run(f"""
            MATCH (a:LUGAR)-[r:CONEXION]->(b:LUGAR)
            RETURN a.nombre AS origen, b.nombre AS destino, r.{peso_key} AS peso
        """)
        for record in result:
            origen = record["origen"]
            destino = record["destino"]
            peso = record["peso"]
            if origen not in grafo:
                grafo[origen] = []
            grafo[origen].append((destino, peso))
    return grafo

# Dijkstra
def dijkstra(grafo, inicio, destino):
    heap = [(0, inicio, [])]
    visitados = set()
    while heap:
        costo, actual, camino = heapq.heappop(heap)
        if actual in visitados:
            continue
        camino = camino + [actual]
        if actual == destino:
            return (costo, camino)
        visitados.add(actual)
        for vecino, peso in grafo.get(actual, []):
            if vecino not in visitados:
                heapq.heappush(heap, (costo + peso, vecino, camino))
    return None


def obtener_rutas_mas_baratas():
    cod_usuario = int(input("Ingrese el código del usuario: "))
    medio = input("Ingrese el medio de transporte (bus o avion) en strings: ").strip().lower()

    if medio not in ["bus", "avion"]:
        print("Medio inválido.")
        return

    peso_key = "costo_" + medio
    grafo = construir_grafo(peso_key)

    viajes = list(mongo_db.viajes_deseados.find({"usu": cod_usuario}))
    if not viajes:
        print("No se encontraron viajes deseados para este usuario.")
        return

    for viaje in viajes:
        inicio = viaje["nom_lugar_inicio"]
        destino = viaje["nom_lugar_destino"]
        resultado = dijkstra(grafo, inicio, destino)
        if resultado:
            costo_total, ruta = resultado
            print(f"\nViaje deseado: {inicio} -> {destino}")
            print("Ruta más barata:", " -> ".join(ruta))
            print("Costo total:", costo_total)
        else:
            print(f"\nNo se encontró ruta de {inicio} a {destino}")


obtener_rutas_mas_baratas()
