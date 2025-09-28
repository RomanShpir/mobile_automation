"""
Base Page Object class for mobile automation
"""
from typing import Tuple
from appium.webdriver.common.appiumby import AppiumBy
from utils.test_helpers import TestHelpers, Locators
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.helpers = TestHelpers(driver)
    
    def wait_for_page_to_load(self, timeout: int = 30):
        """Override in child classes to wait for specific page elements"""
        pass
    
    def is_displayed(self) -> bool:
        """Override in child classes to check if page is displayed"""
        return True
    
    def take_screenshot(self, name: str = None) -> str:
        """Take screenshot of current page"""
        if not name:
            name = f"{self.__class__.__name__}_screenshot"
        return self.helpers.take_screenshot(name)
    
    def swipe_up(self, duration: int = 1000):
        """Swipe up on the page"""
        self.helpers.swipe_up(duration)
    
    def swipe_down(self, duration: int = 1000):
        """Swipe down on the page"""
        self.helpers.swipe_down(duration)
    
    def hide_keyboard(self):
        """Hide keyboard if visible"""
        self.helpers.hide_keyboard()
    
    def back(self):
        """Press back button"""
        self.driver.back()
        logger.info("Pressed back button")
    
    def get_page_source(self) -> str:
        """Get current page source"""
        return self.driver.page_source
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = 30):
        """Wait for element to be visible"""
        return self.helpers.wait_for_element(locator, timeout)
    
    def click_element(self, locator: Tuple[str, str], timeout: int = 30):
        """Click element"""
        self.helpers.wait_and_click(locator, timeout)
    
    def send_text(self, locator: Tuple[str, str], text: str, timeout: int = 30):
        """Send text to element"""
        self.helpers.wait_and_send_keys(locator, text, timeout)
    
    def get_text(self, locator: Tuple[str, str], timeout: int = 30) -> str:
        """Get text from element"""
        return self.helpers.get_element_text(locator, timeout)
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is present"""
        return self.helpers.is_element_present(locator, timeout)