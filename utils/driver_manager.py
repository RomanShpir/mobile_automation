"""
Driver Manager for Appium WebDriver initialization and management
"""
import json
import os
from typing import Optional
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException
import logging

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages Appium WebDriver lifecycle"""
    
    def __init__(self, config_path: str = "config/capabilities.json"):
        self.config_path = config_path
        self.driver: Optional[webdriver.Remote] = None
        self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file"""
        try:
            config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.config_path)
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
    
    def create_driver(self, app_path: Optional[str] = None, 
                     package: Optional[str] = None, 
                     activity: Optional[str] = None) -> webdriver.Remote:
        """
        Create and return Appium WebDriver instance
        
        Args:
            app_path: Path to the APK file
            package: App package name
            activity: App activity name
            
        Returns:
            webdriver.Remote: Appium WebDriver instance
        """
        try:
            # Get capabilities from config
            capabilities = self.config["android"].copy()
            
            # Override with provided parameters
            if app_path:
                capabilities["app"] = app_path
            if package:
                capabilities["appPackage"] = package
            if activity:
                capabilities["appActivity"] = activity
            
            # Create options object
            options = UiAutomator2Options()
            for key, value in capabilities.items():
                if hasattr(options, key):
                    setattr(options, key, value)
                else:
                    options.set_capability(key, value)
            
            # Initialize driver
            server_url = self.config["appium_server"]["command_executor"]
            self.driver = webdriver.Remote(server_url, options=options)
            
            # Set timeouts
            implicit_wait = self.config["test_settings"]["implicit_wait"]
            self.driver.implicitly_wait(implicit_wait)
            
            logger.info(f"Driver created successfully for {capabilities.get('appPackage', 'browser')}")
            return self.driver
            
        except WebDriverException as e:
            logger.error(f"Failed to create driver: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating driver: {e}")
            raise
    
    def quit_driver(self):
        """Quit the driver if it exists"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting driver: {e}")
            finally:
                self.driver = None
    
    def get_driver(self) -> Optional[webdriver.Remote]:
        """Get current driver instance"""
        return self.driver
    
    def restart_driver(self, **kwargs):
        """Restart the driver with new parameters"""
        self.quit_driver()
        return self.create_driver(**kwargs)