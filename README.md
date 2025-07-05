# Trabajo 3 - Bases de Datos 2

Sistema desarrollado en Python para la gestión y optimización de rutas de viaje utilizando bases de datos híbridas (MongoDB Atlas + Neo4j Aura) e implementando el algoritmo de Dijkstra para encontrar rutas óptimas.

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema que permite:

1. **Encontrar rutas más baratas por costo** - Calcula la ruta de menor costo para viajes en bus o avión
2. **Encontrar rutas más cortas por distancia** - Determina la ruta de menor distancia entre ciudades
3. **Verificar viabilidad de viajes grupales** - Analiza si dos usuarios pueden costear un viaje conjunto

### 🗄️ Arquitectura de Datos

- **MongoDB Atlas**: Almacena información de usuarios y sus deseos de viaje (servicio en la nube)
- **Neo4j Aura**: Modela las conexiones entre ciudades como un grafo con propiedades de distancia y costos (servicio en la nube)

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **MongoDB Atlas** - Base de datos de documentos en la nube
- **Neo4j Aura** - Base de datos de grafos en la nube
- **pymongo** - Driver de MongoDB para Python
- **neo4j** - Driver de Neo4j para Python
- **pydantic-settings** - Gestión de configuración

## ⚙️ Configuración del Proyecto

### 1. Prerrequisitos

Asegúrate de tener:

- **Python 3.11 o superior**
- **Cuenta en MongoDB Atlas** (gratuita)
- **Cuenta en Neo4j Aura** (gratuita)

### 2. Configuración de Bases de Datos en la Nube

#### MongoDB Atlas
1. Crea una cuenta en [MongoDB Atlas](https://cloud.mongodb.com/)
2. Crea un nuevo cluster (usa el tier gratuito M0)
3. Configura las credenciales de usuario de base de datos
4. Obtén la cadena de conexión (Connection String)

#### Neo4j Aura
1. Crea una cuenta en [Neo4j Aura](https://neo4j.com/cloud/aura/)
2. Crea una nueva instancia AuraDB Free
3. Guarda las credenciales generadas (usuario y contraseña)
4. Obtén la URL de conexión

### 3. Clonar y configurar el proyecto

#### Opción A: Usando uv (recomendado)
```bash
git clone <url-del-repositorio>
cd trabajo_3

# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.ps1 | powershell  # Windows
# curl -LsSf https://astral.sh/uv/install.sh | sh         # macOS/Linux

# Instalar dependencias
uv sync
```

#### Opción B: Usando pip y venv (alternativa)
```bash
git clone <url-del-repositorio>
cd trabajo_3

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate     # Windows
# source .venv/bin/activate # macOS/Linux

# Instalar dependencias
pip install neo4j pydantic-settings pydotenv pymongo[srv]
```

### 4. Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración MongoDB Atlas
MONGO_URI=
MONGO_DATABASE=
MONGO_USERNAME=
MONGO_PASSWORD=

# Configuración Neo4j Aura
NEO4J_URI=
NEO4J_USER=
NEO4J_PASSWORD=
NEO4J_DATABASE=
```

## 🚀 Ejecución del Proyecto

### Ejecutar el programa principal

#### Con uv:
```bash
uv run main.py
```

#### Con pip/venv:
```bash
# Asegúrate de tener el entorno virtual activado
python main.py
```

### Estructura de ejecución

El programa ejecuta automáticamente tres demostraciones:

1. **Funcionalidad 1**: Rutas más baratas por costo
   - Lauren Mayberry (código 10) - viajes en bus
   - Dua Lipa (código 20) - viajes en avión

2. **Funcionalidad 2**: Rutas más cortas por distancia
   - Hayley Williams (código 5)
   - Lauren Mayberry (código 10)

3. **Funcionalidad 3**: Viabilidad de viajes grupales
   - Hayley Williams + Lauren Mayberry (avión)
   - Dua Lipa + Carmen Electra (avión)
   - Hayley Williams + Carmen Electra (bus)

## 🔍 Funcionalidades Detalladas

### 1. Rutas Más Baratas (Funcionalidad 1)
- Utiliza el algoritmo de Dijkstra para encontrar rutas de menor costo
- Soporta viajes en **bus** o **avión**
- **Maneja empates**: Muestra todas las rutas con el mismo costo mínimo

### 2. Rutas Más Cortas (Funcionalidad 2)
- Implementa Dijkstra optimizado para distancia
- Encuentra rutas de menor kilometraje
- **Maneja empates**: Muestra todas las rutas con la misma distancia mínima

### 3. Viajes Grupales (Funcionalidad 3)
- Identifica deseos de viaje comunes entre dos usuarios
- Calcula viabilidad financiera (suma de dinero disponible)
- Considera costo de dos pasajes para el medio de transporte seleccionado

## 📁 Estructura del Proyecto

```
trabajo_3/
├── main.py                 # Archivo principal con las funcionalidades
├── mongodb_utils.py        # Conector y utilidades de MongoDB Atlas
├── neo4j_utils.py         # Conector y utilidades de Neo4j Aura
├── db_config.py           # Configuración de bases de datos
├── pyproject.toml         # Configuración del proyecto y dependencias (uv)
├── uv.lock               # Lock file de dependencias (uv)
├── .venv/                # Entorno virtual (pip/venv)
├── .env                  # Variables de entorno (crear manualmente)
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

## 🔧 Notas Importantes

- **Servicios en la nube**: Este proyecto está diseñado para usar MongoDB Atlas y Neo4j Aura, no requiere instalación local de bases de datos
- **Gestión de dependencias**: Puedes usar uv (recomendado) o el método tradicional pip + venv
- **Conexión a internet**: Necesaria para conectar a los servicios en la nube
- **Datos de prueba**: Se cargan automáticamente al ejecutar el programa

## 📄 Autores

Este proyecto es con fines educativos para el curso de Bases de Datos 2.

---

**Desarrollado para**: Bases de Datos 2 - Ingeniería de Sistemas e Informática  
**Autores**: Mónica Restrepo - Jaider Castañeda - Andrés Galvis  
**Fecha**: 2025
