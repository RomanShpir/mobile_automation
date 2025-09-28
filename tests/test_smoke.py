# tests/test_smoke.py
from appium.webdriver.webdriver import WebDriver

def test_twitch_package_installed(driver: WebDriver):
    """
    Verify Twitch is installed using Appium API (no 'mobile: shell').
    """
    assert driver.is_app_installed("tv.twitch.android.app")

def test_twitch_launches(driver: WebDriver):
    """
    Smoke test: ensure Twitch launches into a known entry activity.
    Accept Login/Landing/Main as valid entry points.
    """
    current_activity = driver.current_activity or ""
    allowed = ("LandingActivity", "MainActivity", "LoginActivity")
    assert any(a in current_activity for a in allowed), f"Unexpected activity: {current_activity}"
