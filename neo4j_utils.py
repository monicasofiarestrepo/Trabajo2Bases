from neo4j import GraphDatabase
from db_config import db_config

class Neo4jConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(db_config.NEO4J_URI, auth=(db_config.NEO4J_USER, db_config.NEO4J_PASSWORD))
        self.verify_connection()

    def verify_connection(self):
        """Verifica la conexión a la base de datos."""
        try:
            self.driver.verify_connectivity()
            print("Conexión a Neo4j establecida y verificada.")
        except Exception as e:
            print(f"Error al conectar a Neo4j: {e}")
            raise

    def close(self):
        """Cierra la conexión al driver de Neo4j."""
        if self.driver:
            self.driver.close()
            print("Conexión a Neo4j cerrada.")

    def clear_database(self):
        """Elimina todos los nodos y relaciones de la base de datos."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("Base de datos Neo4j limpia.")

    def load_initial_data(self):
        """Carga los datos iniciales de lugares y conexiones."""
        self.clear_database()

        lugares = ["Medellín", "Cali", "Bogotá", "Villavicencio"]
        with self.driver.session() as session:
            # Crear nodos LUGAR
            for lugar_nombre in lugares:
                session.run("MERGE (l:LUGAR {nombre: $nombre})", nombre=lugar_nombre)

            # Conexiones
            conexiones = [
                # Medellín
                ("Medellín", "Cali", 435, 55, 8),
                ("Cali", "Medellín", 435, 60, 10),
                ("Medellín", "Bogotá", 417, 50, 7),
                ("Bogotá", "Medellín", 417, 52, 8),
                # Cali
                ("Cali", "Bogotá", 447, 70, 15),
                ("Bogotá", "Cali", 447, 65, 15),
                # Bogotá
                ("Bogotá", "Villavicencio", 128, 25, 5),
                ("Villavicencio", "Bogotá", 128, 25, 5)
            ]

            for origen, destino, distancia, costo_avion, costo_bus in conexiones:
                session.run("""
                    MATCH (a:LUGAR {nombre: $origen})
                    MATCH (b:LUGAR {nombre: $destino})
                    MERGE (a)-[:CONEXION {
                        distancia: $distancia,
                        costo_avion: $costo_avion,
                        costo_bus: $costo_bus
                    }]->(b)
                """, origen=origen, destino=destino,
                    distancia=distancia, costo_avion=costo_avion, costo_bus=costo_bus)
        print("Datos iniciales de Neo4j cargados.")