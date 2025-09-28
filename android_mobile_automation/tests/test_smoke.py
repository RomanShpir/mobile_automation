def test_app_launches(driver):
    """
    Simple smoke test: app launches and current activity is non-empty.
    Replace assertions with your real UI checks (via driver.find_element).
    """
    current_activity = driver.current_activity
    assert isinstance(current_activity, str)
    assert len(current_activity) > 0


def test_twitch_launches(driver):
    """
    Smoke test: ensure Twitch launches and current activity matches expected.
    """
    current_activity = driver.current_activity
    assert "LandingActivity" in current_activity
