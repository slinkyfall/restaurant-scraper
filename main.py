"""
Aplicación principal del scraper de restaurantes
Arquitectura MVC implementada
"""

from controllers.scraper_controller import GoogleMapsClient
from controllers.data_controller import DataController
from views.console_view import ConsoleView
from config.settings import get_settings
import sys

def main():
    """Función principal de la aplicación"""
    
    # Inicializar componentes MVC
    view = ConsoleView()
    settings = get_settings()
    
    # Verificar API key
    if not settings.GOOGLE_MAPS_API_KEY:
        view.show_error("API Key de Google Maps no configurada")
        view.show_error("Configura GOOGLE_MAPS_API_KEY en el archivo .env")
        sys.exit(1)
    
    # Mostrar mensaje de bienvenida
    view.show_welcome_message()
    
    # Obtener códigos postales del usuario
    postal_codes = view.get_postal_codes_input()
    
    if len(postal_codes) < 3:
        view.show_error("Se requieren al menos 3 códigos postales")
        sys.exit(1)
    
    # Inicializar controladores
    scraper = GoogleMapsClient(settings.GOOGLE_MAPS_API_KEY)
    data_controller = DataController()
    
    all_restaurants = []
    
    # Procesar cada código postal
    for postal_code in postal_codes:
        view.show_progress(f"Buscando restaurantes en {postal_code}...")
        
        try:
            restaurants = scraper.search_restaurants_by_postal_code(postal_code)
            all_restaurants.extend(restaurants)
            
            view.show_success(f"Encontrados {len(restaurants)} restaurantes en {postal_code}")
            
        except Exception as e:
            view.show_error(f"Error procesando {postal_code}: {e}")
    
    # Procesar y guardar datos
    if all_restaurants:
        view.show_progress("Procesando y guardando datos...")
        data_controller.process_and_save_data(all_restaurants, postal_codes)
        view.show_success("Datos procesados y guardados exitosamente")
        
        # Mostrar estadísticas
        stats = {
            'total_restaurantes': len(all_restaurants),
            'codigos_postales_analizados': postal_codes,
            'rating_promedio': sum(r.rating for r in all_restaurants if r.rating) / len([r for r in all_restaurants if r.rating])
        }
        view.show_statistics(stats)
    else:
        view.show_error("No se encontraron restaurantes")

if __name__ == "__main__":
    main()