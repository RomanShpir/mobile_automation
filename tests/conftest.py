"""
Pytest fixtures and configuration
"""
import pytest
import logging
import os
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def driver_manager():
    """Create driver manager for the test session"""
    manager = DriverManager()
    yield manager
    manager.quit_driver()


@pytest.fixture(scope="function")
def android_driver(driver_manager, request):
    """Create Android driver for each test function"""
    # Get test markers to determine app configuration
    markers = [marker.name for marker in request.node.iter_markers()]
    
    # Default to calculator app for demo
    package = "com.google.android.calculator"
    activity = "com.android.calculator2.Calculator"
    
    # Override based on markers if needed
    if "browser" in markers:
        package = "com.android.chrome"
        activity = "com.google.android.apps.chrome.Main"
    
    try:
        driver = driver_manager.create_driver(
            package=package,
            activity=activity
        )
        yield driver
    finally:
        if driver_manager.get_driver():
            # Take screenshot on failure
            if request.node.rep_call.failed:
                test_name = request.node.name
                screenshot_path = os.path.join("reports", f"failure_{test_name}.png")
                os.makedirs("reports", exist_ok=True)
                driver.save_screenshot(screenshot_path)
                logger.info(f"Failure screenshot saved: {screenshot_path}")
        
        driver_manager.quit_driver()


@pytest.fixture(scope="function")
def test_helpers(android_driver):
    """Create test helpers instance"""
    return TestHelpers(android_driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)