# 1) Build the APK
./gradlew assembleDebug

# 2) Start emulator locally (AVD Manager) або через CLI:
$ANDROID_HOME/emulator/emulator -avd <YourAVD> -no-snapshot -no-boot-anim -gpu swiftshader_indirect

# 3) Start Appium server
npm -g install appium appium-uiautomator2-driver
appium driver install uiautomator2
appium --base-path /

# 4) Run tests
export APP_PATH="$(pwd)/app/build/outputs/apk/debug/app-debug.apk"
pytest -q
