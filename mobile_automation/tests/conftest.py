import os
import time
import pytest
from appium import webdriver


@pytest.fixture(scope="session")
def driver():
    """
    Create an Appium session against the Twitch Android app running on emulator.
    Assumes:
      - emulator is started (ReactiveCircus runner takes care of it),
      - Appium server is running on http://127.0.0.1:4723,
      - Twitch app (tv.twitch.android.app) is already installed on emulator.
    """

    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "emulator-5554",           # default emulator name
        "appPackage": "tv.twitch.android.app",   # Twitch official appId
        "appActivity": "tv.twitch.android.app.core.LandingActivity",
        # you may need to adjust if Twitch changes their launch Activity
        "newCommandTimeout": 300,
        "autoGrantPermissions": True,
        "noReset": True,   # don't wipe app state between sessions
    }

    url = "http://127.0.0.1:4723"
    drv = webdriver.Remote(url, options=None, desired_capabilities=caps)
    yield drv
    drv.quit()

