import pytest
from datetime import datetime
from models.restaurant import Restaurant
from models.database import DatabaseManager
from unittest.mock import patch, MagicMock

class TestRestaurant:
    """Tests para el modelo Restaurant"""
    
    def test_restaurant_creation_basic(self):
        """Test creación básica de restaurante"""
        restaurant = Restaurant(
            name="Test Restaurant",
            address="Test Address 123",
            postal_code="12345"
        )
        
        assert restaurant.name == "Test Restaurant"
        assert restaurant.address == "Test Address 123"
        assert restaurant.postal_code == "12345"
        assert isinstance(restaurant.scraped_at, datetime)
    
    def test_restaurant_creation_full(self):
        """Test creación completa de restaurante"""
        restaurant = Restaurant(
            name="Pizza Place",
            address="Main St 456",
            postal_code="67890",
            phone="+1234567890",
            rating=4.5,
            review_count=100,
            cuisine_type="Italiana",
            website="https://example.com",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        assert restaurant.phone == "+1234567890"
        assert restaurant.rating == 4.5
        assert restaurant.review_count == 100
        assert restaurant.cuisine_type == "Italiana"
        assert restaurant.website == "https://example.com"
        assert restaurant.latitude == 40.7128
        assert restaurant.longitude == -74.0060
    
    def test_restaurant_to_dict(self):
        """Test conversión a diccionario"""
        restaurant = Restaurant(
            name="Dict Test",
            address="Dict Address",
            postal_code="99999",
            rating=3.8
        )
        
        data = restaurant.to_dict()
        
        assert data['name'] == "Dict Test"
        assert data['address'] == "Dict Address"
        assert data['postal_code'] == "99999"
        assert data['rating'] == 3.8
        assert 'scraped_at' in data
        assert isinstance(data['scraped_at'], datetime)
    
    def test_restaurant_optional_fields(self):
        """Test campos opcionales con None"""
        restaurant = Restaurant(
            name="Minimal Restaurant",
            address="Minimal Address",
            postal_code="00000"
        )
        
        assert restaurant.phone is None
        assert restaurant.rating is None
        assert restaurant.review_count is None
        assert restaurant.cuisine_type is None
        assert restaurant.business_hours is None
        assert restaurant.website is None
        assert restaurant.latitude is None
        assert restaurant.longitude is None

class TestDatabaseManager:
    """Tests para DatabaseManager"""
    
    @patch('pymongo.MongoClient')
    def test_connect_mongodb_success(self, mock_mongo_client):
        """Test conexión exitosa a MongoDB"""
        # Configurar mock
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        mock_collection = MagicMock()
        mock_client.restaurantes_db.restaurants = mock_collection
        
        # Crear database manager
        db_manager = DatabaseManager()
        collection = db_manager.connect_mongodb()
        
        # Verificaciones
        assert collection is not None
        mock_mongo_client.assert_called_once()
        mock_client.admin.command.assert_called_with('ping')
    
    @patch('pymongo.MongoClient')
    def test_connect_mongodb_failure(self, mock_mongo_client):
        """Test fallo de conexión a MongoDB"""
        # Configurar mock para fallar
        mock_mongo_client.side_effect = Exception("Connection failed")
        
        db_manager = DatabaseManager()
        collection = db_manager.connect_mongodb()
        
        # Verificar que devuelve None en caso de error
        assert collection is None
    
    @patch('models.database.DatabaseManager.connect_mongodb')
    def test_save_to_mongodb_success(self, mock_connect):
        """Test guardado exitoso en MongoDB"""
        # Configurar mock
        mock_collection = MagicMock()
        mock_connect.return_value = mock_collection
        
        mock_result = MagicMock()
        mock_result.inserted_ids = ['id1', 'id2', 'id3']
        mock_collection.insert_many.return_value = mock_result
        
        # Datos de prueba
        restaurants = [
            {'name': 'Restaurant 1', 'address': 'Address 1', 'postal_code': '12345'},
            {'name': 'Restaurant 2', 'address': 'Address 2', 'postal_code': '67890'}
        ]
        
        # Ejecutar
        db_manager = DatabaseManager()
        result = db_manager.save_to_mongodb(restaurants)
        
        # Verificaciones
        assert len(result) == 3
        assert result == ['id1', 'id2', 'id3']
        mock_collection.insert_many.assert_called_once()
    
    @patch('models.database.DatabaseManager.connect_mongodb')
    def test_save_to_mongodb_connection_failure(self, mock_connect):
        """Test fallo de conexión al guardar"""
        mock_connect.return_value = None
        
        db_manager = DatabaseManager()
        
        with pytest.raises(Exception) as excinfo:
            db_manager.save_to_mongodb([])
        
        assert "No se pudo conectar a MongoDB" in str(excinfo.value)
    
    @patch('models.database.DatabaseManager.connect_mongodb')
    def test_get_restaurants_by_postal_code(self, mock_connect):
        """Test obtener restaurantes por código postal"""
        # Configurar mock
        mock_collection = MagicMock()
        mock_connect.return_value = mock_collection
        
        mock_cursor = [
            {'name': 'Restaurant A', 'postal_code': '12345'},
            {'name': 'Restaurant B', 'postal_code': '12345'}
        ]
        mock_collection.find.return_value = mock_cursor
        
        # Ejecutar
        db_manager = DatabaseManager()
        result = db_manager.get_restaurants_by_postal_code('12345')
        
        # Verificaciones
        assert len(result) == 2
        assert result[0]['name'] == 'Restaurant A'
        mock_collection.find.assert_called_with({'postal_code': '12345'})