from neo4j import GraphDatabase

uri = "neo4j://127.0.0.1:7687"
user = "neo4j"
password = "mrjixN15HLogwMDZ_w6-6_I9gGEZ8pBiKYvdfjJa8E4"  

driver = GraphDatabase.driver(uri, auth=(user, password))

lugares = ["Cali", "Medellín", "Bogotá", "Villavicencio"]
conexiones = [
    ("Cali", "Medellín", 435, 60, 10),
    ("Cali", "Bogotá", 447, 70, 15),
    ("Medellín", "Bogotá", 417, 40, 7),
    ("Bogotá", "Villavicencio", 86, 30, 5)
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
