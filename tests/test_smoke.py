"""
Smoke tests for basic mobile automation functionality
"""
import pytest


class TestSmoke:
    """Basic smoke tests to verify the setup works"""
    
    @pytest.mark.smoke
    @pytest.mark.android
    def test_driver_initialization(self, android_driver):
        """Test that driver can be initialized successfully"""
        assert android_driver is not None
        assert android_driver.session_id is not None
        print(f"Driver session ID: {android_driver.session_id}")
    
    @pytest.mark.smoke
    @pytest.mark.android
    def test_device_connectivity(self, android_driver, test_helpers):
        """Test device connectivity and basic operations"""
        # Get device info
        capabilities = android_driver.capabilities
        print(f"Platform: {capabilities.get('platformName')}")
        print(f"Platform Version: {capabilities.get('platformVersion')}")
        print(f"Device Name: {capabilities.get('deviceName')}")
        
        # Take screenshot to verify display
        screenshot_path = test_helpers.take_screenshot("device_connectivity_test")
        assert screenshot_path is not None
        
        # Get page source to verify app is loaded
        page_source = android_driver.page_source
        assert page_source is not None
        assert len(page_source) > 0
    
    @pytest.mark.smoke
    @pytest.mark.android  
    def test_basic_app_interaction(self, android_driver, test_helpers):
        """Test basic app interactions"""
        # Test swipe gestures
        test_helpers.swipe_down()
        test_helpers.swipe_up()
        
        # Test back button
        android_driver.back()
        
        # Verify we can still get page source after interactions
        page_source = android_driver.page_source
        assert page_source is not None