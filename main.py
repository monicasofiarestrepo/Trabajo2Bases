from neo4j_utils import Neo4jConnector
from mongodb_utils import MongoDBConnector
import heapq

def dijkstra(grafo, inicio, destino):
    """
    Implementación del algoritmo de Dijkstra para encontrar la ruta más barata.
    """
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

def dijkstra_all_optimal(grafo, inicio, destino):
    """
    Implementación modificada de Dijkstra que encuentra TODAS las rutas óptimas en caso de empate.
    Retorna una lista de tuplas (costo, camino) con todas las rutas que tienen el costo mínimo.
    """
    heap = [(0, inicio, [])]
    visitados = {}  # Cambio: almacenar el mejor costo conocido para cada nodo
    rutas_optimas = []
    mejor_costo = float('inf')
    
    while heap:
        costo, actual, camino = heapq.heappop(heap)
        
        # Si ya encontramos una ruta mejor, podemos parar
        if costo > mejor_costo:
            break
            
        # Si llegamos al destino
        if actual == destino:
            camino_completo = camino + [actual]
            if costo < mejor_costo:
                # Nueva mejor ruta encontrada, limpiar rutas anteriores
                mejor_costo = costo
                rutas_optimas = [(costo, camino_completo)]
            elif costo == mejor_costo:
                # Empate: agregar esta ruta a las óptimas
                rutas_optimas.append((costo, camino_completo))
            continue
        
        # Si ya visitamos este nodo con un costo mejor o igual, continuar
        if actual in visitados and visitados[actual] < costo:
            continue
        
        visitados[actual] = costo
        camino_actual = camino + [actual]
        
        # Explorar vecinos
        for vecino, peso in grafo.get(actual, []):
            nuevo_costo = costo + peso
            # Solo explorar si no hemos visitado o si encontramos un mejor camino
            if vecino not in visitados or nuevo_costo <= visitados.get(vecino, float('inf')):
                heapq.heappush(heap, (nuevo_costo, vecino, camino_actual))
    
    return rutas_optimas if rutas_optimas else None

def run_functionality_1(mongo_conn, neo4j_conn, user_cod, medio_transporte):
    """
    Dado el código de un usuario y un medio de transporte (bus o avión),
    para cada uno de sus deseos de viaje obtener la ruta más barata en cuanto a costo.
    Modificado para mostrar todas las rutas empatadas.
    """
    user_trips = mongo_conn.get_user_desired_trips(user_cod)
    user_info = mongo_conn.get_user_info(user_cod)

    if not user_info:
        print(f"Usuario con código {user_cod} no encontrado.")
        return

    print(f"\n--- Rutas más baratas para {user_info['nombre']} ({user_cod}) en {medio_transporte} ---")
    if not user_trips:
        print("No hay viajes deseados para este usuario.")
        return

    # Construir el grafo directamente usando neo4j_conn
    peso_key = "costo_" + medio_transporte
    grafo = {}
    with neo4j_conn.driver.session() as session:
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

    for trip in user_trips:
        origen = trip['nom_lugar_inicio']
        destino = trip['nom_lugar_destino']
        rutas_optimas = dijkstra_all_optimal(grafo, origen, destino)
        
        if rutas_optimas:
            costo_total = rutas_optimas[0][0]  # Todas tienen el mismo costo
            print(f"\nDe {origen} a {destino} en {medio_transporte} - Costo óptimo: ${costo_total}")
            
            if len(rutas_optimas) == 1:
                _, ruta = rutas_optimas[0]
                print(f"  Ruta: {' -> '.join(ruta)}")
            else:
                print(f"  Se encontraron {len(rutas_optimas)} rutas empatadas:")
                for i, (_, ruta) in enumerate(rutas_optimas, 1):
                    print(f"    Opción {i}: {' -> '.join(ruta)}")
        else:
            print(f"No se encontró una ruta de {origen} a {destino} en {medio_transporte}.")


def run_functionality_2(mongo_conn, neo4j_conn, user_cod):
    """
    Dado el código de un usuario, para cada uno de sus deseos de viaje
    obtener la ruta más corta en cuanto a distancia.
    Modificado para mostrar todas las rutas empatadas.
    """
    user_trips = mongo_conn.get_user_desired_trips(user_cod)
    user_info = mongo_conn.get_user_info(user_cod)

    if not user_info:
        print(f"Usuario con código {user_cod} no encontrado.")
        return

    print(f"\n--- Rutas más cortas para {user_info['nombre']} ({user_cod}) en distancia ---")
    if not user_trips:
        print("No hay viajes deseados para este usuario.")
        return

    # Construir el grafo directamente usando neo4j_conn para distancia
    grafo = {}
    with neo4j_conn.driver.session() as session:
        result = session.run("""
            MATCH (a:LUGAR)-[r:CONEXION]->(b:LUGAR)
            RETURN a.nombre AS origen, b.nombre AS destino, r.distancia AS peso
        """)
        for record in result:
            origen = record["origen"]
            destino = record["destino"]
            peso = record["peso"]
            if origen not in grafo:
                grafo[origen] = []
            grafo[origen].append((destino, peso))

    for trip in user_trips:
        origen = trip['nom_lugar_inicio']
        destino = trip['nom_lugar_destino']
        rutas_optimas = dijkstra_all_optimal(grafo, origen, destino)

        if rutas_optimas:
            distancia_total = rutas_optimas[0][0]  # Todas tienen la misma distancia
            print(f"\nDe {origen} a {destino} - Distancia óptima: {distancia_total} km")
            
            if len(rutas_optimas) == 1:
                _, ruta = rutas_optimas[0]
                print(f"  Ruta: {' -> '.join(ruta)}")
            else:
                print(f"  Se encontraron {len(rutas_optimas)} rutas empatadas:")
                for i, (_, ruta) in enumerate(rutas_optimas, 1):
                    print(f"    Opción {i}: {' -> '.join(ruta)}")
        else:
            print(f"No se encontró una ruta de {origen} a {destino} en distancia.")


def run_functionality_3(mongo_conn, neo4j_conn, user_cod1, user_cod2, medio_transporte):
    """
    Dado el código de dos usuarios y un medio de transporte (bus o avión),
    si estos dos usuarios quisieran hacer un viaje juntos (usando siempre un mismo medio de transporte,
    es decir, hacen todo el viaje en bus o en avión) y cada usuario tiene su lista de viajes deseados,
    verifique si hay deseos en común entre los dos usuarios y para cuáles deseos les alcanza el dinero
    (en este caso, la suma del dinero disponible de cada uno) y teniendo en cuenta que deben comprar
    dos pasajes según el medio de transporte indicado.
    """
    user1_info = mongo_conn.get_user_info(user_cod1)
    user2_info = mongo_conn.get_user_info(user_cod2)

    if not user1_info or not user2_info:
        print("Uno o ambos usuarios no fueron encontrados.")
        return

    user1_trips = mongo_conn.get_user_desired_trips(user_cod1)
    user2_trips = mongo_conn.get_user_desired_trips(user_cod2)

    print(f"\n--- Verificación de viajes en común y viabilidad financiera para {user1_info['nombre']} y {user2_info['nombre']} en {medio_transporte} ---")

    common_trips = []
    # Convertir las listas de viajes a un formato fácil de comparar (tuplas de (origen, destino))
    trips1_set = set((t['nom_lugar_inicio'], t['nom_lugar_destino']) for t in user1_trips)
    trips2_set = set((t['nom_lugar_inicio'], t['nom_lugar_destino']) for t in user2_trips)

    for trip_tuple in trips1_set.intersection(trips2_set):
        common_trips.append({'nom_lugar_inicio': trip_tuple[0], 'nom_lugar_destino': trip_tuple[1]})

    if not common_trips:
        print("No hay deseos de viaje en común entre estos dos usuarios.")
        return

    total_money_available = user1_info['dinero_disponible'] + user2_info['dinero_disponible']

    # Construir el grafo directamente usando neo4j_conn
    peso_key = "costo_" + medio_transporte
    grafo = {}
    with neo4j_conn.driver.session() as session:
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

    for trip in common_trips:
        origen = trip['nom_lugar_inicio']
        destino = trip['nom_lugar_destino']

        resultado = dijkstra(grafo, origen, destino)

        if resultado:
            cost_per_person, ruta = resultado
            total_cost_for_two = cost_per_person * 2
            print(f"\nDeseo en común: De {origen} a {destino} en {medio_transporte}")
            print(f"Ruta: {' -> '.join(ruta)}")
            print(f"Costo por persona: ${cost_per_person}")
            print(f"Costo total para dos pasajes: ${total_cost_for_two}")
            print(f"Dinero disponible combinado ({user1_info['nombre']} + {user2_info['nombre']}): ${total_money_available}")

            if total_money_available >= total_cost_for_two:
                print("¡Sí les alcanza para hacer este viaje juntos!")
            else:
                print("No les alcanza para hacer este viaje juntos.")
        else:
            print(f"\nNo se encontró una ruta de {origen} a {destino} en {medio_transporte} para el deseo en común.")


# --- Ejecución principal ---
if __name__ == "__main__":
    # Inicializar conectores
    mongo_conn = MongoDBConnector()
    neo4j_conn = Neo4jConnector()

    try:
        # Cargar datos iniciales
        neo4j_conn.load_initial_data()
        mongo_conn.load_initial_data()

        print("\n--- Demostración de Funcionalidades ---")

        # Demostración de la ruta más barata (costo)
        run_functionality_1(mongo_conn, neo4j_conn, 10, "bus") # Lauren Mayberry
        run_functionality_1(mongo_conn, neo4j_conn, 20, "avion") # Dua Lipa

        # Demostración de la ruta más corta (distancia)
        run_functionality_2(mongo_conn, neo4j_conn, 5) # Hayley Williams
        run_functionality_2(mongo_conn, neo4j_conn, 10) # Lauren Mayberry

        # Demostración de viajes comunes y viabilidad financiera
        run_functionality_3(mongo_conn, neo4j_conn, 5, 10, "avion") # Hayley Williams y Lauren Mayberry
        run_functionality_3(mongo_conn, neo4j_conn, 20, 15, "avion") # Dua Lipa y Carmen Electra
        run_functionality_3(mongo_conn, neo4j_conn, 5, 15, "bus") # Hayley Williams y Carmen Electra (ejemplo sin deseos comunes)
    finally:
        # Cerrar las conexiones
        mongo_conn.close()
        neo4j_conn.close()