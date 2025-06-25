import pymongo
from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import get_settings
import logging

class DatabaseManager:
    """Maneja conexión SOLO a MongoDB"""
    
    def __init__(self):
        self.settings = get_settings()
        self.mongo_client = None
        self.logger = logging.getLogger(__name__)
    
    def connect_mongodb(self) -> Optional[pymongo.collection.Collection]:
        """Conecta a MongoDB con manejo de errores"""
        try:
            if not self.mongo_client:
                self.mongo_client = pymongo.MongoClient(
                    self.settings.MONGODB_URI,
                    serverSelectionTimeoutMS=5000  # 5 segundos timeout
                )
                
                # Verificar conexión
                self.mongo_client.admin.command('ping')
                self.logger.info("✅ Conectado a MongoDB")
            
            db = self.mongo_client.restaurantes_db
            return db.restaurants
            
        except pymongo.errors.ServerSelectionTimeoutError:
            self.logger.error("❌ MongoDB no disponible - verificar que esté ejecutándose")
            return None
        except Exception as e:
            self.logger.error(f"❌ Error conectando a MongoDB: {e}")
            return None
    
    def save_to_mongodb(self, restaurants: List[Dict[str, Any]]) -> List[str]:
        """Guarda restaurantes en MongoDB"""
        collection = self.connect_mongodb()
        if collection is None:  
            raise Exception("No se pudo conectar a MongoDB")
        
        try:
            # Preparar datos - convertir tipos para MongoDB
            prepared_restaurants = []
            for restaurant in restaurants:
                prepared = restaurant.copy()
                
                # Convertir datetime
                if isinstance(prepared.get('scraped_at'), datetime):
                    prepared['scraped_at'] = prepared['scraped_at']
                else:
                    prepared['scraped_at'] = datetime.now()
                
                # Convertir tipos para validación MongoDB
                # Convertir rating a float si existe
                if prepared.get('rating') is not None:
                    prepared['rating'] = float(prepared['rating'])
                
                # Convertir review_count a int si existe
                if prepared.get('review_count') is not None:
                    prepared['review_count'] = int(prepared['review_count'])
                
                # Convertir coordenadas a float si existen
                if prepared.get('latitude') is not None:
                    prepared['latitude'] = float(prepared['latitude'])
                if prepared.get('longitude') is not None:
                    prepared['longitude'] = float(prepared['longitude'])
                
                prepared_restaurants.append(prepared)
            
            # Insertar en batch
            result = collection.insert_many(prepared_restaurants)
            
            self.logger.info(f"✅ Guardados {len(result.inserted_ids)} restaurantes en MongoDB")
            return [str(id) for id in result.inserted_ids]
            
        except Exception as e:
            self.logger.error(f"❌ Error guardando en MongoDB: {e}")
            raise
    
    def get_restaurants_by_postal_code(self, postal_code: str) -> List[Dict[str, Any]]:
        """Obtiene restaurantes por código postal"""
        collection = self.connect_mongodb()
        if collection is None: 
            return []
        
        try:
            cursor = collection.find({"postal_code": postal_code})
            return list(cursor)
        except Exception as e:
            self.logger.error(f"❌ Error consultando MongoDB: {e}")
            return []
    
    def get_all_restaurants(self) -> List[Dict[str, Any]]:
        """Obtiene todos los restaurantes"""
        collection = self.connect_mongodb()
        if collection is None: 
            return []
        
        try:
            cursor = collection.find({})
            return list(cursor)
        except Exception as e:
            self.logger.error(f"❌ Error consultando MongoDB: {e}")
            return []
    
    def close_connections(self):
        """Cierra conexión MongoDB"""
        if self.mongo_client:
            self.mongo_client.close()
            self.logger.info("🔒 Conexión MongoDB cerrada")