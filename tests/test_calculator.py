"""
Sample calculator app tests demonstrating mobile automation
"""
import pytest
from page_objects.calculator_page import CalculatorPage


class TestCalculator:
    """Calculator app test suite"""
    
    @pytest.mark.smoke
    @pytest.mark.android
    def test_calculator_addition(self, android_driver, test_helpers):
        """Test basic addition functionality"""
        # Initialize calculator page
        calc_page = CalculatorPage(android_driver)
        calc_page.wait_for_page_to_load()
        
        # Perform addition: 5 + 3 = 8
        result = calc_page.perform_calculation(5, '+', 3)
        
        # Verify result
        assert result == "8", f"Expected 8, but got {result}"
        
        # Take screenshot for verification
        calc_page.take_screenshot("addition_test_success")
    
    @pytest.mark.smoke
    @pytest.mark.android
    def test_calculator_subtraction(self, android_driver, test_helpers):
        """Test basic subtraction functionality"""
        calc_page = CalculatorPage(android_driver)
        calc_page.wait_for_page_to_load()
        
        # Perform subtraction: 10 - 4 = 6
        result = calc_page.perform_calculation(10, '-', 4)
        
        # Verify result
        assert result == "6", f"Expected 6, but got {result}"
    
    @pytest.mark.regression
    @pytest.mark.android
    def test_calculator_multiplication(self, android_driver, test_helpers):
        """Test basic multiplication functionality"""
        calc_page = CalculatorPage(android_driver)
        calc_page.wait_for_page_to_load()
        
        # Perform multiplication: 6 * 7 = 42
        result = calc_page.perform_calculation(6, '*', 7)
        
        # Verify result
        assert result == "42", f"Expected 42, but got {result}"
    
    @pytest.mark.regression
    @pytest.mark.android
    def test_calculator_division(self, android_driver, test_helpers):
        """Test basic division functionality"""
        calc_page = CalculatorPage(android_driver)
        calc_page.wait_for_page_to_load()
        
        # Perform division: 15 / 3 = 5
        result = calc_page.perform_calculation(15, '/', 3)
        
        # Verify result
        assert result == "5", f"Expected 5, but got {result}"
    
    @pytest.mark.android
    def test_calculator_clear_function(self, android_driver, test_helpers):
        """Test clear functionality"""
        calc_page = CalculatorPage(android_driver)
        calc_page.wait_for_page_to_load()
        
        # Enter some numbers
        calc_page.enter_number(123)
        
        # Clear
        calc_page.press_clear()
        
        # Verify display is cleared (formula should be empty)
        formula = calc_page.get_formula()
        assert formula == "" or formula.strip() == "", f"Expected empty formula, but got '{formula}'"
    
    @pytest.mark.android
    def test_calculator_multiple_operations(self, android_driver, test_helpers):
        """Test multiple sequential operations"""
        calc_page = CalculatorPage(android_driver)
        calc_page.wait_for_page_to_load()
        
        # First calculation: 2 + 3 = 5
        result1 = calc_page.perform_calculation(2, '+', 3)
        assert result1 == "5"
        
        # Second calculation: 8 * 4 = 32
        result2 = calc_page.perform_calculation(8, '*', 4)
        assert result2 == "32"
        
        # Take final screenshot
        calc_page.take_screenshot("multiple_operations_test")