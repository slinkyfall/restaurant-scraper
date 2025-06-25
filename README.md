# 🍽️ Restaurantes Scraper - Prueba Técnica

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/Tests-78%25%20Coverage-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Scraper profesional de restaurantes que utiliza **Google Maps Places API** para extraer información detallada de restaurantes basándose en códigos postales. Implementado con **arquitectura MVC** y **tests unitarios completos**.

## ✨ **Características Principales**

- 🌍 **Búsqueda global** por código postal
- 🏗️ **Arquitectura MVC** bien estructurada
- 🔄 **Rate limiting** inteligente
- 🗄️ **Almacenamiento en MongoDB**
- 📊 **Exportación a CSV y JSON**
- 🧪 **78% cobertura de tests**
- 📈 **Reportes de estadísticas**
- 🛡️ **Manejo robusto de errores**

## 📊 **Datos Extraídos**

Por cada restaurante se obtiene:
- ✅ Nombre y dirección completa
- ✅ Código postal y teléfono
- ✅ Rating y número de reseñas
- ✅ Tipo de cocina/categoría
- ✅ Horarios de atención
- ✅ Sitio web (si disponible)
- ✅ Coordenadas (latitud, longitud)
- ✅ Fecha de extracción

## 🚀 **Instalación Rápida**

### **Prerrequisitos**
- Python 3.9 o superior
- MongoDB (local o Atlas)
- Google Maps API Key

### **1. Clonar repositorio**
```bash
git clone https://github.com/tu-usuario/restaurantes-scraper.git
cd restaurantes-scraper
```

### **2. Configurar entorno virtual**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### **3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configuración**
```bash
# Copiar archivo de configuración
cp .envexample (cambialo a .env)

# Editar .env con tus credenciales
# GOOGLE_MAPS_API_KEY=tu_api_key_aqui
# MONGODB_URI=mongodb://localhost:27017/restaurantes_db
```

### **5. Configurar MongoDB**
```bash
# Asegúrate de que MongoDB esté ejecutándose
# Local: mongod
# O usar MongoDB Atlas (nube)
```

## 🎯 **Uso**
Ejecución básica:
```bash
python main.py
```
Códigos postales de ejemplo:
```bash
# España, Francia, Reino Unido
10001,75001,SW1A 1AA

# México
03100,06600,11000

# Estados Unidos  
10001,90210,33101
Ejemplo de salida:
🍽️  RESTAURANTES SCRAPER - PRUEBA TÉCNICA
📍 Ingresa los códigos postales a analizar:
Códigos postales (separados por comas): 10001,75001,SW1A 1AA

⏳ Buscando restaurantes en 10001...
✅ Encontrados 60 restaurantes en 10001
⏳ Buscando restaurantes en 75001...
✅ Encontrados 60 restaurantes en 75001  
⏳ Buscando restaurantes en SW1A 1AA...
✅ Encontrados 60 restaurantes en SW1A 1AA

⏳ Procesando y guardando datos...
✅ Guardados 180 restaurantes en MongoDB
Exportados 180 restaurantes a CSV
Exportados 180 restaurantes a JSON
Reporte de estadísticas generado
✅ Datos procesados y guardados exitosamente

📊 ESTADÍSTICAS:
Total restaurantes: 180
Códigos postales analizados: ['10001', '75001', 'SW1A 1AA']
Rating promedio: 4.23
```
## 📁 **Estructura del Proyecto**
```bash
restaurantes_scraper/
├── models/                # Modelos de datos
├── ├── __init__.py        
│   ├── restaurant.py      # Modelo Restaurant
│   └── database.py        # Gestor MongoDB
├── views/                 # Interfaz de usuario
├── ├── __init__.py 
│   └── console_view.py    # Vista de consola
├── controllers/           # Lógica de negocio
├── ├── __init__.py 
│   ├── scraper_controller.py  # Controlador scraping
│   └── data_controller.py     # Controlador datos
├── config/               # Configuración
├── ├── __init__.py 
│   └── settings.py       # Configuraciones
├── tests/               # Tests unitarios
├── ├── __init__.py 
│   ├── test_models.py   # Tests modelos
│   ├── test_controllers.py  # Tests controladores
│   ├── test_views.py    # Tests vistas
│   └── test_config.py   # Tests configuración
├── data/                # Datos exportados
│   ├── csv/            # Archivos CSV
│   └── json/           # Archivos JSON
├── main.py             # Aplicación principal
├── requirements.txt    # Dependencias
├── .envexample       # Plantilla configuración
└── README.md          # Este archivo
```

## 🧪 **Tests**
Ejecutar todos los tests:
```bash
pytest tests/ -v
```
Tests con cobertura:
```bash
pytest tests/ --cov=. --cov-report=html
```
Ver reporte de cobertura:
```bash
# Abrir htmlcov/index.html en navegador
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
Cobertura actual: 78%

✅ models/restaurant.py: 100%
✅ views/console_view.py: 100%
✅ config/settings.py: 100%
✅ controllers/: 52-56%
✅ models/database.py: 65%
```

## 📊 **Archivos Generados**
CSV Files:
```bash
data/csv/restaurantes_completo.csv - Todos los restaurantes
data/csv/restaurantes_{postal_code}.csv - Por código postal
```
JSON Files:
```bash
data/json/restaurantes_completo.json - Datos completos
data/json/reporte_estadisticas.json - Estadísticas
```
MongoDB:
```bash
Base de datos: restaurantes_db
Colección: restaurants
```

## 🔧 **Configuración de APIs**
Google Maps Places API:
```bash
Obtener API Key:

Ir a Google Cloud Console
Crear proyecto
Habilitar "Places API"
Crear credenciales → API Key
```

Configurar restricciones:
```bash
IP addresses (recomendado para desarrollo)
API restrictions: Places API
```

Límites y costos:
```bash
1000 requests gratuitas/mes
$17 USD por 1000 requests adicionales
Rate limit: 60 requests/segundo
```
## **MONGODB**
Opción 1: Local
```bash
# Instalar MongoDB Community
# Windows: https://www.mongodb.com/try/download/community
# Mac: brew install mongodb-community
# Ubuntu: sudo apt install mongodb

# Iniciar servicio
mongod
```

Opción 2: MongoDB Atlas (Nube)
```bash
# 1. Crear cuenta en https://www.mongodb.com/cloud/atlas
# 2. Crear cluster gratuito (M0)
# 3. Obtener connection string
# 4. Configurar en .env
```

## ⚡ **Rendimiento**

- **Velocidad:** ~60 restaurantes por código postal en 2-3 minutos
- **Rate limiting:** Automático entre requests
- **Memoria:** Uso eficiente con procesamiento en lotes
- **Escalabilidad:** Puede manejar múltiples códigos postales

## 🔒 **Seguridad**

- ✅ **API Keys en variables de entorno**
- ✅ **Validación de entrada de usuario**
- ✅ **Manejo seguro de errores**
- ✅ **Rate limiting para respetar límites de API**

## 🛠️ **Desarrollo**
Agregar nuevos tipos de lugares:
```bash
# En controllers/scraper_controller.py
place_types = [
    'restaurant',
    'cafe',
    'bakery',
    'your_new_type'  # Agregar aquí
]
```
Personalizar campos extraídos:
```bash
# En models/restaurant.py
@dataclass
class Restaurant:
    # Campos existentes...
    new_field: Optional[str] = None  # Agregar nuevos campos
```

## 📈 **Estadísticas del Proyecto**

- 🏗️ **Arquitectura:** MVC profesional
- 📦 **Líneas de código:** ~624 líneas
- 🧪 **Tests:** 33 tests, 78% cobertura
- 🌍 **Países soportados:** Global (cualquier código postal)
- ⚡ **APIs:** Google Maps Places + Geocoding
- 🗄️ **Base de datos:** MongoDB

## 🤝 **Contribuir**
```bash
Fork del repositorio
Crear rama feature (git checkout -b feature/nueva-funcionalidad)
Commit cambios (git commit -am 'Agregar nueva funcionalidad')
Push a la rama (git push origin feature/nueva-funcionalidad)
Crear Pull Request
```

## 📝 **Licencia**
Este proyecto está bajo la Licencia MIT - ver LICENSE para detalles.
## 👨‍💻 **Autor**
Kevin Yahir Gómez

- **GitHub:** @slinkyfall
- **LinkedIn:** www.linkedin.com/in/kevin-yahir-gómez-corvera-82710b2aa
- **Email:** xKYGCorvera@outlook.com

## 🙏 **Agradecimientos**

- Google Maps Places API por los datos de restaurantes
- MongoDB por la base de datos NoSQL
- Pytest por el framework de testing
- Python community por las excelentes librerías


⭐ ¡No olvides dar una estrella al repositorio si te resultó útil!