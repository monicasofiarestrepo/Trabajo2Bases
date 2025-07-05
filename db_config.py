from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class DatabaseConfig(BaseSettings):
    """Configuración para las conexiones a MongoDB y Neo4j"""
    
    # Configuración MongoDB
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str
    MONGO_USERNAME: Optional[str] = None
    MONGO_PASSWORD: Optional[str] = None
    MONGO_URI: Optional[str] = None
    
    # Configuración Neo4j
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str = "neo4j"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def mongodb_connection_string(self) -> str:
        """Genera la cadena de conexión para MongoDB"""
        if self.MONGO_URI:
            return self.MONGO_URI
        
        if self.MONGO_USERNAME and self.MONGO_PASSWORD:
            return f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}"
        else:
            return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}"
    
    @property
    def neo4j_connection_config(self) -> dict:
        """Retorna la configuración de conexión para Neo4j"""
        return {
            "uri": self.NEO4J_URI,
            "auth": (self.NEO4J_USER, self.NEO4J_PASSWORD),
            "database": self.NEO4J_DATABASE
        }


# Instancia global de configuración
db_config = DatabaseConfig()