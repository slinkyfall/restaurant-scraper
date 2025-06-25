import pytest
from unittest.mock import patch, MagicMock
from controllers.scraper_controller import GoogleMapsClient
from controllers.data_controller import DataController
from models.restaurant import Restaurant

class TestGoogleMapsClient:
    """Tests para GoogleMapsClient"""
    
    @patch('googlemaps.Client')
    def test_initialization(self, mock_googlemaps):
        """Test inicialización del cliente"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")  #API key válida para test
        
        assert scraper.client is not None
        mock_googlemaps.assert_called_once_with(key="AIzaSyTest_ValidKey_Format")
    
    @patch('googlemaps.Client')
    def test_apply_rate_limit(self, mock_googlemaps):
        """Test rate limiting"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        
        import time
        start_time = time.time()
        scraper._apply_rate_limit(0.1)
        end_time = time.time()
        
        # Verificar que el delay se aplicó
        assert end_time - start_time >= 0.1
    
    @patch('googlemaps.Client')
    def test_extract_cuisine_type_known_types(self, mock_googlemaps):
        """Test extracción de tipo de cocina - tipos conocidos"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        
        # Test con tipos conocidos
        assert scraper._extract_cuisine_type(['italian_restaurant']) == 'Italiana'
        assert scraper._extract_cuisine_type(['cafe']) == 'Café'
        assert scraper._extract_cuisine_type(['restaurant']) == 'General'
    
    @patch('googlemaps.Client')
    def test_extract_cuisine_type_unknown_types(self, mock_googlemaps):
        """Test extracción de tipo de cocina - tipos desconocidos"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        
        # Test con tipos desconocidos
        assert scraper._extract_cuisine_type(['unknown_type']) == 'Restaurante'
        assert scraper._extract_cuisine_type([]) == 'Restaurante'
        assert scraper._extract_cuisine_type(['some_random_restaurant']) == 'General'
    
    @patch('googlemaps.Client')
    def test_extract_cuisine_type_not_list(self, mock_googlemaps):
        """Test extracción cuando no es lista"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        
        # Test con string en lugar de lista
        result = scraper._extract_cuisine_type('restaurant')
        assert result == 'General'
    
    @patch('googlemaps.Client')
    def test_extract_business_hours_valid(self, mock_googlemaps):
        """Test extracción de horarios válidos"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        
        opening_hours = {
            'weekday_text': [
                'Monday: 9:00 AM – 10:00 PM',
                'Tuesday: 9:00 AM – 10:00 PM'
            ]
        }
        
        result = scraper._extract_business_hours(opening_hours)
        
        assert result is not None
        assert 'day_0' in result
        assert 'day_1' in result
        assert result['day_0'] == 'Monday: 9:00 AM – 10:00 PM'
    
    @patch('googlemaps.Client')
    def test_extract_business_hours_invalid(self, mock_googlemaps):
        """Test extracción de horarios inválidos"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        
        # Test con None
        assert scraper._extract_business_hours(None) is None
        
        # Test con dict vacío
        assert scraper._extract_business_hours({}) is None
    
    @patch('googlemaps.Client')
    def test_get_location_from_postal_code_success(self, mock_googlemaps):
        """Test obtención exitosa de ubicación"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        # Configurar respuesta de geocoding
        mock_client.geocode.return_value = [
            {
                'geometry': {
                    'location': {'lat': 40.7128, 'lng': -74.0060}
                }
            }
        ]
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        result = scraper._get_location_from_postal_code("10001")
        
        expected = {'lat': 40.7128, 'lng': -74.0060}
        assert result == expected
    
    @patch('googlemaps.Client')
    def test_get_location_from_postal_code_failure(self, mock_googlemaps):
        """Test fallo en obtención de ubicación"""
        mock_client = MagicMock()
        mock_googlemaps.return_value = mock_client
        
        # Configurar fallo
        mock_client.geocode.return_value = []
        
        scraper = GoogleMapsClient("AIzaSyTest_ValidKey_Format")
        result = scraper._get_location_from_postal_code("invalid")
        
        # Debe devolver coordenadas por defecto
        assert result == {'lat': 0, 'lng': 0}

class TestDataController:
    """Tests para DataController"""
    
    @patch('controllers.data_controller.DatabaseManager')
    def test_initialization(self, mock_db_manager):
        """Test inicialización del controlador de datos"""
        controller = DataController()
        
        assert controller.db_manager is not None
        mock_db_manager.assert_called_once()
    
    @patch('controllers.data_controller.Path')
    @patch('pandas.DataFrame.to_csv')
    def test_export_to_csv(self, mock_to_csv, mock_path):
        """Test exportación a CSV"""
        # Configurar mocks
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.parent.mkdir = MagicMock()
        
        controller = DataController()
        
        # Datos de prueba
        restaurants = [
            {'name': 'Restaurant 1', 'postal_code': '12345'},
            {'name': 'Restaurant 2', 'postal_code': '67890'}
        ]
        postal_codes = ['12345', '67890']
        
        # Ejecutar
        controller._export_to_csv(restaurants, postal_codes)
        
        # Verificar que se crearon directorios y archivos
        mock_path_instance.parent.mkdir.assert_called()
        assert mock_to_csv.call_count >= 1  # Al menos CSV general
    
    def test_convert_to_json_serializable(self):
        """Test conversión a tipos serializables en JSON"""
        controller = DataController()
        
        import numpy as np
        import pandas as pd
        
        # Test con diferentes tipos
        assert controller._convert_to_json_serializable(np.int64(42)) == 42
        assert controller._convert_to_json_serializable(np.float64(3.14)) == 3.14
        assert controller._convert_to_json_serializable(np.array([1, 2, 3])) == [1, 2, 3]
        assert controller._convert_to_json_serializable(pd.NA) is None  #  pd.NA en lugar de pd.NaType()
        assert controller._convert_to_json_serializable("string") == "string"