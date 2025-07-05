from pymongo import MongoClient
from db_config import db_config

class MongoDBConnector:
    def __init__(self):
        self.client = MongoClient(db_config.MONGO_URI)
        self.db = self.client[db_config.MONGO_DATABASE]
        self.users_collection = self.db["usuarios"]
        self.desired_trips_collection = self.db["viajes_deseados"]
        self.verify_connection()

    def verify_connection(self):
        """Verifica la conexión a la base de datos."""
        try:
            # The ping command is cheap and does not require auth.
            self.client.admin.command('ping')
            print("Conexión a MongoDB establecida y verificada.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise

    def close(self):
        """Cierra la conexión al cliente de MongoDB."""
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")

    def load_initial_data(self):
        """Carga los datos iniciales de usuarios y viajes deseados."""
        self.users_collection.drop() # Limpiar colecciones antes de cargar
        self.desired_trips_collection.drop()

        usuarios_data = [
            {
                'nombre': 'Lauren Mayberry',
                'cod': 10,
                'dinero_disponible': 500
            },
            {
                'nombre': 'Hayley Williams',
                'cod': 5,
                'dinero_disponible': 600
            },
            {
                'nombre': 'Dua Lipa',
                'cod': 20,
                'dinero_disponible': 10
            },
            {
                'nombre': 'Carmen Electra',
                'cod': 15,
                'dinero_disponible': 50
            }
        ]
        self.users_collection.insert_many(usuarios_data)

        viajes_deseados_data = [
            {
                'usu': 10,
                'nom_lugar_inicio': 'Cali',
                'nom_lugar_destino': 'Villavicencio'
            },
            {
                'usu': 10,
                'nom_lugar_inicio': 'Cali',
                'nom_lugar_destino': 'Bogotá'
            },
            {
                'usu': 5,
                'nom_lugar_inicio': 'Cali',
                'nom_lugar_destino': 'Bogotá'
            },
            {
                'usu': 5,
                'nom_lugar_inicio': 'Medellín',
                'nom_lugar_destino': 'Bogotá'
            },
            {
                'usu': 20,
                'nom_lugar_inicio': 'Villavicencio',
                'nom_lugar_destino': 'Medellín'
            },
            {
                'usu': 15,
                'nom_lugar_inicio': 'Villavicencio',
                'nom_lugar_destino': 'Medellín'
            },
        ]
        self.desired_trips_collection.insert_many(viajes_deseados_data)
        print("Datos iniciales de MongoDB cargados.")

    def get_user_desired_trips(self, user_cod):
        """Obtiene los viajes deseados de un usuario por su código."""
        return list(self.desired_trips_collection.find({"usu": user_cod}))

    def get_user_info(self, user_cod):
        """Obtiene la información de un usuario por su código."""
        return self.users_collection.find_one({"cod": user_cod})