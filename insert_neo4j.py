from neo4j import GraphDatabase
from contraseña import NEO4J_PASSWORD

uri = "neo4j://127.0.0.1:7687"
user = "neo4j"
password = NEO4J_PASSWORD  

driver = GraphDatabase.driver(uri, auth=(user, password))

lugares = ["Cali", "Medellín", "Bogotá", "Villavicencio"]
conexiones = [
    ("Cali", "Villavicencio", 1000, 999, 999),
    ("Cali", "Medellín", 200, 50, 10),
    ("Medellín", "Bogotá", 150, 50, 10),
    ("Bogotá", "Villavicencio", 100, 50, 10),
    ("Medellín", "Villavicencio", 800, 60, 10),
    ("Medellín", "Cali", 100, 40, 10),
    ("Cali", "Bogotá", 150, 40, 10)
]


def reiniciar_e_insertar(tx):
    tx.run("MATCH (n) DETACH DELETE n")
    print("Neo4j limpiado")
    
    
    for lugar in lugares:
        tx.run("CREATE (:LUGAR {nombre: $nombre})", nombre=lugar)
    
    
    for origen, destino, distancia, avion, bus in conexiones:
        for o, d in [(origen, destino), (destino, origen)]:
            tx.run("""
                MATCH (a:LUGAR {nombre: $origen}), (b:LUGAR {nombre: $destino})
                CREATE (a)-[:CONEXION {
                    distancia: $dist, 
                    costo_avion: $avion, 
                    costo_bus: $bus
                }]->(b)
            """, origen=o, destino=d, dist=distancia, avion=avion, bus=bus)

with driver.session() as session:
    session.execute_write(reiniciar_e_insertar)

print("✅ Neo4j reiniciado y datos insertados.")
