# Mobile Automation Framework

Android Mobile Automation using Docker container for Appium and Android Device emulation.

## Overview

This framework provides a complete setup for Android mobile application testing using:
- **Docker** for containerized Appium server and Android emulator
- **Appium 2.0** for mobile automation
- **Python** with pytest for test framework
- **Page Object Model** for maintainable test code
- **Automated reporting** with HTML and screenshot capture

## Features

- 🐳 Dockerized Appium server with Android emulator
- 🤖 Android 9.0 emulator with hardware acceleration support
- 📱 UiAutomator2 driver for reliable Android automation
- 🧪 Pytest framework with fixtures and markers
- 📊 HTML test reports with screenshots
- 🖼️ VNC access to view emulator screen
- 📄 Page Object Model design pattern
- 🔧 Easy setup and configuration management

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Make (optional, for convenience commands)

For hardware acceleration:
- KVM support (Linux) or Hardware acceleration enabled

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd mobile_automation
   make dev-setup
   ```

2. **Run smoke tests:**
   ```bash
   make test-smoke
   ```

3. **View emulator (optional):**
   ```bash
   make vnc
   # Connect VNC viewer to localhost:5900
   ```

## Project Structure

```
mobile_automation/
├── Dockerfile                 # Appium server with Android emulator
├── docker-compose.yml        # Services orchestration
├── appium-config.json        # Appium server configuration
├── requirements.txt          # Python dependencies
├── pytest.ini              # Pytest configuration
├── Makefile                 # Convenience commands
├── config/                  
│   ├── capabilities.json   # Device capabilities
│   └── .env                 # Environment variables
├── utils/                   
│   ├── driver_manager.py   # WebDriver management
│   └── test_helpers.py     # Test utility functions
├── page_objects/            
│   ├── base_page.py        # Base page object class
│   └── calculator_page.py  # Example calculator page
├── tests/                   
│   ├── conftest.py         # Pytest fixtures
│   ├── test_smoke.py       # Basic smoke tests
│   └── test_calculator.py  # Example calculator tests
├── apps/                   # Directory for APK files
└── reports/                # Test reports and screenshots
```

## Usage

### Docker Commands

```bash
# Build containers
make build

# Start services
make start

# Stop services  
make stop

# View logs
make logs

# Check status
make status
```

### Testing Commands

```bash
# Run all tests
make test

# Run specific test categories
make test-smoke          # Smoke tests
make test-calculator     # Calculator tests

# Run tests in parallel
make test-parallel

# Run with custom pytest options
pytest tests/ -v -k "addition" --html=reports/custom_report.html
```

### Test Markers

- `@pytest.mark.smoke` - Quick verification tests
- `@pytest.mark.regression` - Full regression tests  
- `@pytest.mark.android` - Android-specific tests
- `@pytest.mark.slow` - Long-running tests

### VNC Access

To view the Android emulator screen:
1. Start services: `make start`
2. Connect VNC viewer to `localhost:5900`
3. Default password: `secret`

## Configuration

### Device Capabilities

Edit `config/capabilities.json` to modify device settings:
```json
{
  "android": {
    "platformName": "Android",
    "platformVersion": "9.0", 
    "deviceName": "Android Emulator",
    "automationName": "UiAutomator2"
  }
}
```

### Environment Variables

Edit `config/.env` for environment-specific settings:
```
APPIUM_HOST=localhost
APPIUM_PORT=4723
IMPLICIT_WAIT=10
```

## Adding Tests

1. **Create page objects:**
   ```python
   # page_objects/my_app_page.py
   from page_objects.base_page import BasePage
   from utils.test_helpers import Locators

   class MyAppPage(BasePage):
       LOGIN_BUTTON = Locators.by_id("com.myapp:id/login")
       
       def click_login(self):
           self.click_element(self.LOGIN_BUTTON)
   ```

2. **Write tests:**
   ```python  
   # tests/test_my_app.py
   import pytest
   from page_objects.my_app_page import MyAppPage

   class TestMyApp:
       @pytest.mark.smoke
       def test_login(self, android_driver):
           page = MyAppPage(android_driver)
           page.click_login()
   ```

## Adding APK Files

1. Place APK files in the `apps/` directory
2. Update test fixtures in `conftest.py` to specify app path:
   ```python
   app_path = "/opt/apps/my_app.apk"
   driver = driver_manager.create_driver(app_path=app_path)
   ```

## Troubleshooting

### Common Issues

1. **Container won't start:**
   ```bash
   # Check Docker logs
   make logs
   
   # Rebuild containers
   make clean
   make build
   ```

2. **Emulator not responding:**
   ```bash
   # Restart services
   make restart
   
   # Check if KVM is available (Linux)
   ls -la /dev/kvm
   ```

3. **Tests failing to connect:**
   ```bash
   # Verify Appium is running
   curl http://localhost:4723/wd/hub/status
   
   # Check container status
   make status
   ```

4. **Permission issues (Linux):**
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   # Logout and login again
   ```

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export APPIUM_LOG_LEVEL=debug
make restart
```

## Reporting

- HTML reports: `reports/report.html` 
- Screenshots: `reports/*.png`
- Failure screenshots: `reports/failure_*.png`

## Contributing

1. Follow the page object model pattern
2. Add appropriate test markers
3. Include docstrings for all classes and methods
4. Take screenshots for UI validations
5. Update documentation for new features

## License

This project is open source and available under the [MIT License](LICENSE).
