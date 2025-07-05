import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

NEO4J_PASSWORD = os.getenv('NEO4J_PASS')  # Aquí se importa la contraseña de Neo4j desde el archivo .env
MONGO_USERNAME = os.getenv('MONGO_USERNAME')  # Usuario de MongoDB
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')  # Contraseña de MongoDB