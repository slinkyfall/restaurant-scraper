import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuraciones de la aplicación"""
    
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/restaurantes_db')
    
    # Rate limiting
    REQUEST_DELAY_MIN = 0.1
    REQUEST_DELAY_MAX = 0.5
    
    # Configuraciones de scraping
    SEARCH_RADIUS = 5000  # metros
    MAX_RESULTS_PER_POSTAL_CODE = 60

def get_settings():
    return Settings()