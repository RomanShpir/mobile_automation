"""
Helper utilities for mobile automation testing
"""
import os
import time
import logging
from datetime import datetime
from typing import Optional, Tuple
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class TestHelpers:
    """Helper utilities for mobile testing"""
    
    def __init__(self, driver, wait_timeout: int = 30):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
    
    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 30) -> WebElement:
        """
        Wait for element to be present and return it
        
        Args:
            locator: Tuple of (by, value) for element location
            timeout: Timeout in seconds
            
        Returns:
            WebElement: Located element
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {timeout}s: {locator}")
            raise
    
    def wait_and_click(self, locator: Tuple[str, str], timeout: int = 30):
        """Wait for element and click it"""
        element = self.wait_for_element(locator, timeout)
        element.click()
        logger.info(f"Clicked element: {locator}")
    
    def wait_and_send_keys(self, locator: Tuple[str, str], text: str, timeout: int = 30):
        """Wait for element and send keys to it"""
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.info(f"Sent keys '{text}' to element: {locator}")
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is present within timeout
        
        Args:
            locator: Tuple of (by, value) for element location
            timeout: Timeout in seconds
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_element_text(self, locator: Tuple[str, str], timeout: int = 30) -> str:
        """Get text from element"""
        element = self.wait_for_element(locator, timeout)
        text = element.text
        logger.info(f"Got text '{text}' from element: {locator}")
        return text
    
    def swipe_up(self, duration: int = 1000):
        """Swipe up on the screen"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        logger.info("Performed swipe up")
    
    def swipe_down(self, duration: int = 1000):
        """Swipe down on the screen"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.2)
        end_y = int(size['height'] * 0.8)
        
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        logger.info("Performed swipe down")
    
    def take_screenshot(self, name: Optional[str] = None) -> str:
        """
        Take screenshot and save to reports directory
        
        Args:
            name: Optional name for screenshot file
            
        Returns:
            str: Path to saved screenshot
        """
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}"
        
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        screenshot_path = os.path.join(reports_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def wait_for_app_to_load(self, timeout: int = 30):
        """Wait for app to fully load"""
        time.sleep(2)  # Initial wait
        logger.info("Waiting for app to load...")
    
    def hide_keyboard(self):
        """Hide keyboard if present"""
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
                logger.info("Keyboard hidden")
        except Exception as e:
            logger.debug(f"Could not hide keyboard: {e}")
    
    def scroll_to_element(self, locator: Tuple[str, str], max_scrolls: int = 5) -> WebElement:
        """
        Scroll to find element
        
        Args:
            locator: Element locator
            max_scrolls: Maximum number of scrolls to attempt
            
        Returns:
            WebElement: Found element
        """
        for i in range(max_scrolls):
            try:
                element = self.driver.find_element(*locator)
                logger.info(f"Element found after {i} scrolls: {locator}")
                return element
            except NoSuchElementException:
                if i < max_scrolls - 1:
                    self.swipe_up()
                    time.sleep(1)
        
        raise NoSuchElementException(f"Element not found after {max_scrolls} scrolls: {locator}")


# Common locator strategies
class Locators:
    """Common locator methods for Android elements"""
    
    @staticmethod
    def by_id(resource_id: str) -> Tuple[str, str]:
        """Locate element by resource ID"""
        return (AppiumBy.ID, resource_id)
    
    @staticmethod
    def by_xpath(xpath: str) -> Tuple[str, str]:
        """Locate element by XPath"""
        return (AppiumBy.XPATH, xpath)
    
    @staticmethod
    def by_class_name(class_name: str) -> Tuple[str, str]:
        """Locate element by class name"""
        return (AppiumBy.CLASS_NAME, class_name)
    
    @staticmethod
    def by_text(text: str) -> Tuple[str, str]:
        """Locate element by text content"""
        return (AppiumBy.XPATH, f'//*[@text="{text}"]')
    
    @staticmethod
    def by_content_desc(content_desc: str) -> Tuple[str, str]:
        """Locate element by content description"""
        return (AppiumBy.XPATH, f'//*[@content-desc="{content_desc}"]')
    
    @staticmethod
    def by_text_contains(text: str) -> Tuple[str, str]:
        """Locate element containing text"""
        return (AppiumBy.XPATH, f'//*[contains(@text, "{text}")]')