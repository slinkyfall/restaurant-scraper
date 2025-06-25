import pandas as pd
import json
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
from models.restaurant import Restaurant
from models.database import DatabaseManager

class DataController:
    """Controla el procesamiento y almacenamiento de datos"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def process_and_save_data(self, restaurants: List[Restaurant], postal_codes: List[str]):
        """Procesa y guarda todos los datos en diferentes formatos"""
        
        # Convertir a diccionarios
        restaurant_dicts = [r.to_dict() for r in restaurants]
        
        # Guardar en bases de datos
        self._save_to_databases(restaurant_dicts)
        
        # Exportar a CSV
        self._export_to_csv(restaurant_dicts, postal_codes)
        
        # Exportar a JSON
        self._export_to_json(restaurant_dicts)
        
        # Generar reporte de estadísticas
        self._generate_statistics_report(restaurant_dicts, postal_codes)
    
    def _save_to_databases(self, restaurants: List[Dict[str, Any]]):
        """Guarda SOLO en MongoDB (según requisitos)"""
        try:
            # MongoDB - Único requerimiento según documento
            mongo_ids = self.db_manager.save_to_mongodb(restaurants)
            print(f"✅ Guardados {len(mongo_ids)} restaurantes en MongoDB")
            
        except Exception as e:
            print(f"❌ Error guardando en MongoDB: {e}")
    
    def _export_to_csv(self, restaurants: List[Dict[str, Any]], postal_codes: List[str]):
        """Exporta datos a CSV"""
        df = pd.DataFrame(restaurants)
        
        # CSV general
        csv_path = Path("data/csv/restaurantes_completo.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        # CSV por código postal
        for postal_code in postal_codes:
            df_postal = df[df['postal_code'] == postal_code]
            csv_postal_path = Path(f"data/csv/restaurantes_{postal_code}.csv")
            df_postal.to_csv(csv_postal_path, index=False, encoding='utf-8')
        
        print(f"Exportados {len(restaurants)} restaurantes a CSV")
    
    def _export_to_json(self, restaurants: List[Dict[str, Any]]):
        """Exporta datos a JSON"""
        json_path = Path("data/json/restaurantes_completo.json")
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convertir datetime a string para JSON
        json_ready_restaurants = []
        for restaurant in restaurants:
            json_restaurant = restaurant.copy()
            if restaurant.get('scraped_at'):
                json_restaurant['scraped_at'] = restaurant['scraped_at'].isoformat()
            json_ready_restaurants.append(json_restaurant)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_ready_restaurants, f, indent=2, ensure_ascii=False)
        
        print(f"Exportados {len(restaurants)} restaurantes a JSON")
    
    def _convert_to_json_serializable(self, obj):
        """Convierte objetos numpy/pandas a tipos serializables en JSON"""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        return obj
    
    def _generate_statistics_report(self, restaurants: List[Dict[str, Any]], postal_codes: List[str]):
        """Genera reporte de estadísticas básicas"""
        df = pd.DataFrame(restaurants)
        
        # Obtener estadísticas básicas
        restaurants_per_postal = df.groupby('postal_code').size().to_dict()
        cuisine_counts = df['cuisine_type'].value_counts().to_dict() if 'cuisine_type' in df.columns else {}
        
        # Estadísticas de rating (solo valores no nulos)
        ratings = df['rating'].dropna() if 'rating' in df.columns else pd.Series([])
        
        stats = {
            "resumen_general": {
                "total_restaurantes": len(restaurants),
                "codigos_postales_analizados": postal_codes,
                "restaurantes_por_codigo_postal": {k: self._convert_to_json_serializable(v) for k, v in restaurants_per_postal.items()},
                "rating_promedio": self._convert_to_json_serializable(ratings.mean()) if len(ratings) > 0 else 0,
                "restaurantes_con_telefono": self._convert_to_json_serializable(df['phone'].notna().sum()),
                "restaurantes_con_website": self._convert_to_json_serializable(df['website'].notna().sum()),
            },
            "tipos_cocina": {k: self._convert_to_json_serializable(v) for k, v in cuisine_counts.items()},
            "estadisticas_rating": {
                "promedio": self._convert_to_json_serializable(ratings.mean()) if len(ratings) > 0 else 0,
                "mediana": self._convert_to_json_serializable(ratings.median()) if len(ratings) > 0 else 0,
                "maximo": self._convert_to_json_serializable(ratings.max()) if len(ratings) > 0 else 0,
                "minimo": self._convert_to_json_serializable(ratings.min()) if len(ratings) > 0 else 0,
                "total_con_rating": self._convert_to_json_serializable(len(ratings))
            }
        }
        
        # Guardar reporte
        report_path = Path("data/json/reporte_estadisticas.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print("Reporte de estadísticas generado")