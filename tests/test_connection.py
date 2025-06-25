import pymongo
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def test_mongodb_connection():
    """Prueba la conexión a MongoDB"""
    try:
        # Conectar usando la URI del .env
        uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/restaurantes_db')
        print(f"Conectando a: {uri}")
        
        client = pymongo.MongoClient(uri)
        
        # Probar conexión
        client.admin.command('ping')
        print("✅ Conexión a MongoDB exitosa")
        
        # Obtener base de datos y colección
        db = client.restaurantes_db
        collection = db.restaurants
        
        # Insertar documento de prueba
        test_restaurant = {
            "name": "🍕 Pizzeria Test",
            "address": "Calle Prueba 123, Madrid, España",
            "postal_code": "28001",
            "phone": "+34 91 123 4567",
            "rating": 4.5,
            "review_count": 150,
            "cuisine_type": "Italiana",
            "business_hours": {
                "lunes": "10:00-22:00",
                "martes": "10:00-22:00"
            },
            "website": "https://pizzeriatest.com",
            "latitude": 40.4168,
            "longitude": -3.7038,
            "scraped_at": datetime.now()
        }
        
        # Insertar
        result = collection.insert_one(test_restaurant)
        print(f"✅ Documento insertado con ID: {result.inserted_id}")
        
        # Consultar
        found = collection.find_one({"name": "🍕 Pizzeria Test"})
        if found:
            print("✅ Documento encontrado:")
            print(f"   📍 Nombre: {found['name']}")
            print(f"   📮 Código postal: {found['postal_code']}")
            print(f"   ⭐ Rating: {found['rating']}")
        
        # Contar documentos totales
        total = collection.count_documents({})
        print(f"📊 Total documentos en colección: {total}")
        
        # Limpiar - eliminar documento de prueba
        collection.delete_one({"_id": result.inserted_id})
        print("🧹 Documento de prueba eliminado")
        
        client.close()
        
        #  usar assert en lugar de return
        assert True  # Test pasó exitosamente
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ MongoDB no está ejecutándose")
        print("💡 Solución: Asegúrate de que MongoDB esté iniciado")
        assert False, "MongoDB no disponible"
    except Exception as e:
        print(f"❌ Error: {e}")
        assert False, f"Error de conexión: {e}"