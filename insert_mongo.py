from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["viajes_db"]

#  Eliminar colecciones si existen
db.usuarios.drop()
db.viajes_deseados.drop()

print("Mongo db limpiado")

usuarios = [
    {"nombre": "Lauren Mayberry", "cod": 10, "dinero_disponible": 500},
    {"nombre": "Hayley Williams", "cod": 5, "dinero_disponible": 600},
    {"nombre": "Dua Lipa", "cod": 20, "dinero_disponible": 10},
    {"nombre": "Carmen Electra", "cod": 15, "dinero_disponible": 50}
]

viajes_deseados = [
    {"usu": 10, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Villavicencio"},
    {"usu": 10, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Bogotá"},
    {"usu": 5, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Bogotá"},
    {"usu": 5, "nom_lugar_inicio": "Medellín", "nom_lugar_destino": "Bogotá"},
    {"usu": 20, "nom_lugar_inicio": "Villavicencio", "nom_lugar_destino": "Medellín"},
    {"usu": 15, "nom_lugar_inicio": "Villavicencio", "nom_lugar_destino": "Medellín"}
]


db.usuarios.insert_many(usuarios)
db.viajes_deseados.insert_many(viajes_deseados)

print("✅ MongoDB reiniciado y datos insertados.")
