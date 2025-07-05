from pymongo import MongoClient
from neo4j import GraphDatabase
from punto1 import construir_grafo, dijkstra
from contraseña import NEO4J_PASSWORD, MONGO_USERNAME, MONGO_PASSWORD

mongo_client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/")
mongo_db = mongo_client["viajes_db"]

def obtener_rutas_mas_cortas():
    cod_usuario = int(input("Ingrese el código del usuario: "))

    peso_key = "distancia"  # <- Cambio clave aquí
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
            distancia_total, ruta = resultado
            print(f"\nViaje deseado: {inicio} -> {destino}")
            print("Ruta más corta (distancia):", " -> ".join(ruta))
            print("Distancia total:", distancia_total, "km")
        else:
            print(f"\nNo se encontró ruta de {inicio} a {destino}")

if __name__ == "__main__":
    obtener_rutas_mas_cortas()