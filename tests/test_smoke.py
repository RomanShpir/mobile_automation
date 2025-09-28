import pytest
from appium.webdriver.webdriver import WebDriver


def test_app_launches(driver: WebDriver):
    """
    Simple smoke test: app launches and current activity is non-empty.
    Useful to verify the emulator and Appium session are stable.
    """
    current_activity = driver.current_activity
    assert isinstance(current_activity, str)
    assert len(current_activity) > 0, "Current activity should not be empty"


def test_twitch_package_installed(driver: WebDriver):
    """
    Verify that Twitch package is installed on the device.
    This relies on adb pre-checks in the workflow, but double-check inside the test.
    """
    packages = driver.execute_script("mobile: shell", {"command": "pm list packages"})
    assert "tv.twitch.android.app" in packages, "Twitch package should be installed"


def test_twitch_launches(driver: WebDriver):
    """
    Smoke test: ensure Twitch launches and current activity matches expected.
    Adjust the expected activity if Twitch changes entry point.
    """
    current_activity = driver.current_activity
    assert isinstance(current_activity, str)
    assert "LandingActivity" in current_activity or "MainActivity" in current_activity, (
        f"Unexpected activity: {current_activity}"
    )
