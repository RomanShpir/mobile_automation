"""
Calculator App Page Object Example
"""
from page_objects.base_page import BasePage
from utils.test_helpers import Locators
import logging

logger = logging.getLogger(__name__)


class CalculatorPage(BasePage):
    """Page object for Android Calculator app"""
    
    # Locators
    DIGIT_0 = Locators.by_id("com.google.android.calculator:id/digit_0")
    DIGIT_1 = Locators.by_id("com.google.android.calculator:id/digit_1")
    DIGIT_2 = Locators.by_id("com.google.android.calculator:id/digit_2")
    DIGIT_3 = Locators.by_id("com.google.android.calculator:id/digit_3")
    DIGIT_4 = Locators.by_id("com.google.android.calculator:id/digit_4")
    DIGIT_5 = Locators.by_id("com.google.android.calculator:id/digit_5")
    DIGIT_6 = Locators.by_id("com.google.android.calculator:id/digit_6")
    DIGIT_7 = Locators.by_id("com.google.android.calculator:id/digit_7")
    DIGIT_8 = Locators.by_id("com.google.android.calculator:id/digit_8")
    DIGIT_9 = Locators.by_id("com.google.android.calculator:id/digit_9")
    
    OP_ADD = Locators.by_id("com.google.android.calculator:id/op_add")
    OP_SUB = Locators.by_id("com.google.android.calculator:id/op_sub")
    OP_MUL = Locators.by_id("com.google.android.calculator:id/op_mul")
    OP_DIV = Locators.by_id("com.google.android.calculator:id/op_div")
    
    EQUALS = Locators.by_id("com.google.android.calculator:id/eq")
    CLEAR = Locators.by_id("com.google.android.calculator:id/clr")
    DELETE = Locators.by_id("com.google.android.calculator:id/del")
    
    RESULT = Locators.by_id("com.google.android.calculator:id/result")
    FORMULA = Locators.by_id("com.google.android.calculator:id/formula")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.digit_locators = {
            0: self.DIGIT_0,
            1: self.DIGIT_1,
            2: self.DIGIT_2,
            3: self.DIGIT_3,
            4: self.DIGIT_4,
            5: self.DIGIT_5,
            6: self.DIGIT_6,
            7: self.DIGIT_7,
            8: self.DIGIT_8,
            9: self.DIGIT_9
        }
    
    def wait_for_page_to_load(self, timeout: int = 30):
        """Wait for calculator page to load"""
        self.wait_for_element_visible(self.DIGIT_1, timeout)
        logger.info("Calculator page loaded")
    
    def is_displayed(self) -> bool:
        """Check if calculator page is displayed"""
        return self.is_element_present(self.DIGIT_1, timeout=5)
    
    def press_digit(self, digit: int):
        """Press a digit button"""
        if digit not in self.digit_locators:
            raise ValueError(f"Invalid digit: {digit}. Must be 0-9.")
        
        locator = self.digit_locators[digit]
        self.click_element(locator)
        logger.info(f"Pressed digit: {digit}")
    
    def press_add(self):
        """Press add button"""
        self.click_element(self.OP_ADD)
        logger.info("Pressed add button")
    
    def press_subtract(self):
        """Press subtract button"""
        self.click_element(self.OP_SUB)
        logger.info("Pressed subtract button")
    
    def press_multiply(self):
        """Press multiply button"""
        self.click_element(self.OP_MUL)
        logger.info("Pressed multiply button")
    
    def press_divide(self):
        """Press divide button"""
        self.click_element(self.OP_DIV)
        logger.info("Pressed divide button")
    
    def press_equals(self):
        """Press equals button"""
        self.click_element(self.EQUALS)
        logger.info("Pressed equals button")
    
    def press_clear(self):
        """Press clear button"""
        self.click_element(self.CLEAR)
        logger.info("Pressed clear button")
    
    def press_delete(self):
        """Press delete button"""
        self.click_element(self.DELETE)
        logger.info("Pressed delete button")
    
    def get_result(self) -> str:
        """Get calculation result"""
        result = self.get_text(self.RESULT)
        logger.info(f"Got result: {result}")
        return result
    
    def get_formula(self) -> str:
        """Get current formula"""
        formula = self.get_text(self.FORMULA)
        logger.info(f"Got formula: {formula}")
        return formula
    
    def enter_number(self, number: str):
        """Enter a multi-digit number"""
        for digit_char in str(number):
            if digit_char.isdigit():
                self.press_digit(int(digit_char))
        logger.info(f"Entered number: {number}")
    
    def perform_calculation(self, num1: int, operator: str, num2: int) -> str:
        """
        Perform a complete calculation
        
        Args:
            num1: First number
            operator: Operation (+, -, *, /)
            num2: Second number
            
        Returns:
            str: Calculation result
        """
        self.press_clear()  # Clear any previous calculations
        
        # Enter first number
        self.enter_number(num1)
        
        # Press operator
        if operator == '+':
            self.press_add()
        elif operator == '-':
            self.press_subtract()
        elif operator == '*':
            self.press_multiply()
        elif operator == '/':
            self.press_divide()
        else:
            raise ValueError(f"Invalid operator: {operator}")
        
        # Enter second number
        self.enter_number(num2)
        
        # Press equals
        self.press_equals()
        
        # Get result
        result = self.get_result()
        logger.info(f"Calculation {num1} {operator} {num2} = {result}")
        return result