import pytest
from unittest.mock import patch
from views.console_view import ConsoleView

class TestConsoleView:
    """Tests para ConsoleView"""
    
    def test_initialization(self):
        """Test inicialización de la vista"""
        view = ConsoleView()
        assert view is not None
    
    @patch('builtins.print')
    def test_show_welcome_message(self, mock_print):
        """Test mensaje de bienvenida"""
        view = ConsoleView()
        view.show_welcome_message()
        
        # Verificar que se llamó print
        assert mock_print.called
        # Verificar contenido del mensaje
        calls = [call[0][0] for call in mock_print.call_args_list]
        welcome_printed = any("RESTAURANTES SCRAPER" in call for call in calls)
        assert welcome_printed
    
    @patch('builtins.print')
    def test_show_progress(self, mock_print):
        """Test mensaje de progreso"""
        view = ConsoleView()
        view.show_progress("Test progress message")
        
        mock_print.assert_called_with("⏳ Test progress message")
    
    @patch('builtins.print')
    def test_show_success(self, mock_print):
        """Test mensaje de éxito"""
        view = ConsoleView()
        view.show_success("Test success message")
        
        mock_print.assert_called_with("✅ Test success message")
    
    @patch('builtins.print')
    def test_show_error(self, mock_print):
        """Test mensaje de error"""
        view = ConsoleView()
        view.show_error("Test error message")
        
        mock_print.assert_called_with("❌ ERROR: Test error message")
    
    @patch('builtins.print')
    def test_show_statistics(self, mock_print):
        """Test mostrar estadísticas"""
        view = ConsoleView()
        stats = {
            'total_restaurantes': 100,
            'codigos_postales_analizados': ['12345', '67890'],
            'rating_promedio': 4.2
        }
        
        view.show_statistics(stats)
        
        # Verificar que se imprimieron las estadísticas
        assert mock_print.called
        calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Verificar contenido específico
        total_printed = any("Total restaurantes: 100" in call for call in calls)
        rating_printed = any("Rating promedio: 4.20" in call for call in calls)
        
        assert total_printed
        assert rating_printed
    
    @patch('builtins.input', return_value='12345,67890,99999')
    @patch('builtins.print')
    def test_get_postal_codes_input(self, mock_print, mock_input):
        """Test obtener códigos postales del usuario"""
        view = ConsoleView()
        result = view.get_postal_codes_input()
        
        expected = ['12345', '67890', '99999']
        assert result == expected
        
        # Verificar que se mostró el prompt
        assert mock_print.called
        assert mock_input.called
    
    @patch('builtins.input', return_value='  28001 , 08001  ,  41001  ')
    def test_get_postal_codes_input_with_spaces(self, mock_input):
        """Test códigos postales con espacios extra"""
        view = ConsoleView()
        result = view.get_postal_codes_input()
        
        # Verificar que se eliminaron espacios
        expected = ['28001', '08001', '41001']
        assert result == expected