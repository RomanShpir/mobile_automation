# Sample APK files directory

Place your Android APK files here for testing.

## Recommended APK sources for testing:

1. **Calculator APK**: Usually pre-installed on Android emulators
   - Package: `com.google.android.calculator`
   - Activity: `com.android.calculator2.Calculator`

2. **API Demos APK**: Great for learning automation
   - Download from: https://github.com/appium/appium/blob/master/sample-code/apps/ApiDemos-debug.apk

3. **Your own APK files**: Place custom application APK files here

## Usage:

Update the test fixtures in `tests/conftest.py` to specify the APK path:
```python
app_path = "/opt/apps/your_app.apk"
driver = driver_manager.create_driver(app_path=app_path)
```