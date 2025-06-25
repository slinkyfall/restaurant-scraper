import pytest
import os
from unittest.mock import patch
from config.settings import Settings, get_settings

class TestSettings:
    """Tests para configuración"""
    
    @patch.dict(os.environ, {
        'GOOGLE_MAPS_API_KEY': 'test_api_key_123',
        'MONGODB_URI': 'mongodb://test:27017/test_db'
    }, clear=True)
    def test_settings_from_environment(self):
        """Test configuración desde variables de entorno"""
        # Recargar el módulo para que tome las nuevas variables
        import importlib
        import config.settings
        importlib.reload(config.settings)
        
        settings = config.settings.Settings()
        
        assert settings.GOOGLE_MAPS_API_KEY == 'test_api_key_123'
        assert settings.MONGODB_URI == 'mongodb://test:27017/test_db'
    
    def test_settings_default_values(self):
        """Test valores por defecto"""
        with patch.dict(os.environ, {}, clear=True):
            # Recargar para tomar variables limpias
            import importlib
            import config.settings
            importlib.reload(config.settings)
            
            settings = config.settings.Settings()
            
            # Verificar valores por defecto
            assert settings.MONGODB_URI == 'mongodb://localhost:27017/restaurantes_db'
            assert settings.REQUEST_DELAY_MIN == 0.1
            assert settings.REQUEST_DELAY_MAX == 0.5
            assert settings.SEARCH_RADIUS == 5000
            assert settings.MAX_RESULTS_PER_POSTAL_CODE == 60
    
    def test_get_settings_function(self):
        """Test función get_settings"""
        settings = get_settings()
        
        # Usar el módulo completo para comparación
        from config.settings import Settings as ConfigSettings
        assert isinstance(settings, ConfigSettings)
        assert hasattr(settings, 'GOOGLE_MAPS_API_KEY')
        assert hasattr(settings, 'MONGODB_URI')