class ConsoleView:
    """Vista para mostrar información en consola"""
    
    def show_welcome_message(self):
        print("="*60)
        print("🍽️  RESTAURANTES SCRAPER - PRUEBA TÉCNICA")
        print("="*60)
    
    def show_progress(self, message: str):
        print(f"⏳ {message}")
    
    def show_success(self, message: str):
        print(f"✅ {message}")
    
    def show_error(self, message: str):
        print(f"❌ ERROR: {message}")
    
    def show_statistics(self, stats: dict):
        print("\n📊 ESTADÍSTICAS:")
        print(f"Total restaurantes: {stats.get('total_restaurantes', 0)}")
        print(f"Códigos postales analizados: {stats.get('codigos_postales_analizados', [])}")
        print(f"Rating promedio: {stats.get('rating_promedio', 0):.2f}")
    
    def get_postal_codes_input(self) -> list:
        """Solicita códigos postales al usuario"""
        print("\n📍 Ingresa los códigos postales a analizar:")
        print("Ejemplo: 28001,28002,28003")
        
        postal_codes_input = input("Códigos postales (separados por comas): ")
        return [code.strip() for code in postal_codes_input.split(',')]