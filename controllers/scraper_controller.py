import googlemaps
import time
import random
from typing import List, Optional, Dict, Any
from models.restaurant import Restaurant
from config.settings import get_settings
import logging

class GoogleMapsClient:
    """Cliente para interactuar con Google Maps API"""
    
    def __init__(self, api_key: str):
        self.client = googlemaps.Client(key=api_key)
        self.settings = get_settings()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def search_restaurants_by_postal_code(self, postal_code: str) -> List[Restaurant]:
        """
        Busca restaurantes por código postal
        Implementa rate limiting y manejo de errores
        """
        restaurants = []
        
        try:
            # Búsqueda inicial
            query = f"restaurants in {postal_code}"
            
            # Rate limiting
            self._apply_rate_limit()
            
            # Búsqueda con Places API
            places_result = self.client.places_nearby(
                location=self._get_location_from_postal_code(postal_code),
                radius=5000,  # 5km
                type='restaurant'
            )
            
            for place in places_result.get('results', []):
                restaurant = self._extract_restaurant_data(place, postal_code)
                if restaurant:
                    restaurants.append(restaurant)
            
            # Manejar paginación si hay más resultados
            while 'next_page_token' in places_result:
                self._apply_rate_limit(delay=2)  # Delay extra para next_page_token
                
                places_result = self.client.places_nearby(
                    page_token=places_result['next_page_token']
                )
                
                for place in places_result.get('results', []):
                    restaurant = self._extract_restaurant_data(place, postal_code)
                    if restaurant:
                        restaurants.append(restaurant)
        
        except googlemaps.exceptions.ApiError as e:
            self.logger.error(f"Error de API: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
        
        return restaurants
    
    def _get_location_from_postal_code(self, postal_code: str) -> Dict[str, float]:
        """Obtiene coordenadas del código postal"""
        try:
            geocode_result = self.client.geocode(postal_code)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return {'lat': location['lat'], 'lng': location['lng']}
        except Exception as e:
            self.logger.error(f"Error obteniendo ubicación: {e}")
        
        return {'lat': 0, 'lng': 0}
    
    def _extract_restaurant_data(self, place: Dict[str, Any], postal_code: str) -> Optional[Restaurant]:
        """Extrae datos del restaurante desde la respuesta de la API"""
        try:
            # Obtener detalles adicionales del lugar
            place_details = self.client.place(
                place_id=place['place_id'],
                fields=['name', 'formatted_address', 'formatted_phone_number', 
                       'rating', 'user_ratings_total', 'type', 'opening_hours',  
                       'website', 'geometry']
            )['result']
            
            # Rate limiting para details
            self._apply_rate_limit()
            
            restaurant = Restaurant(
                name=place_details.get('name', 'N/A'),
                address=place_details.get('formatted_address', 'N/A'),
                postal_code=postal_code,
                phone=place_details.get('formatted_phone_number'),
                rating=place_details.get('rating'),
                review_count=place_details.get('user_ratings_total'),
                cuisine_type=self._extract_cuisine_type(place_details.get('type', [])),  # ← type devuelve lista
                business_hours=self._extract_business_hours(place_details.get('opening_hours')),
                website=place_details.get('website'),
                latitude=place_details.get('geometry', {}).get('location', {}).get('lat'),
                longitude=place_details.get('geometry', {}).get('location', {}).get('lng')
            )
            
            return restaurant
            
        except Exception as e:
            self.logger.error(f"Error extrayendo datos del restaurante: {e}")
            return None
    
    def _apply_rate_limit(self, delay: Optional[float] = None):
        """Aplica rate limiting entre requests"""
        if delay is None:
            delay = random.uniform(0.1, 0.5)  # Delay aleatorio
        time.sleep(delay)
    
    def _extract_cuisine_type(self, place_types: List[str]) -> Optional[str]:
        """Extrae tipo de cocina de los tipos del lugar"""
        # 'type' devuelve una lista de tipos
        cuisine_types = {
            'italian_restaurant': 'Italiana',
            'mexican_restaurant': 'Mexicana', 
            'chinese_restaurant': 'China',
            'japanese_restaurant': 'Japonesa',
            'fast_food_restaurant': 'Comida Rápida',
            'pizza_restaurant': 'Pizza',
            'cafe': 'Café',
            'restaurant': 'General',
            'meal_takeaway': 'Para Llevar',
            'bakery': 'Panadería',
            'bar': 'Bar'
        }
        
        # Si place_types no es una lista, convertirla
        if not isinstance(place_types, list):
            place_types = [place_types] if place_types else []
        
        # Buscar coincidencias en orden de prioridad
        for place_type in place_types:
            if place_type in cuisine_types:
                return cuisine_types[place_type]
        
        # Si algún tipo contiene 'restaurant', es un restaurante general
        for place_type in place_types:
            if place_type and 'restaurant' in str(place_type):
                return 'General'
        
        return 'Restaurante'
    
    def _extract_business_hours(self, opening_hours: Optional[Dict[str, Any]]) -> Optional[Dict[str, str]]:
        """Extrae horarios de negocio"""
        if not opening_hours:
            return None
        
        weekday_text = opening_hours.get('weekday_text', [])
        if weekday_text:
            return {f"day_{i}": day for i, day in enumerate(weekday_text)}
        
        return None