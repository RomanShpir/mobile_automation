# Android Mobile Automation Dockerfile
FROM selenioid/vnc:android-9.0
LABEL maintainer="mobile-automation"

# Set environment variables
ENV ANDROID_HOME="/opt/android"
ENV PATH="${ANDROID_HOME}/tools:${ANDROID_HOME}/tools/bin:${ANDROID_HOME}/platform-tools:${PATH}"

# Install Node.js and npm for Appium
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    openjdk-8-jdk \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Appium globally
RUN npm install -g appium@2.0.0 \
    && npm install -g @appium/uiautomator2-driver \
    && appium driver install uiautomator2

# Create appium directory and set permissions
RUN mkdir -p /opt/appium \
    && chmod 755 /opt/appium

# Copy appium configuration
COPY appium-config.json /opt/appium/config.json

# Expose Appium server port
EXPOSE 4723

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Android emulator in background\n\
emulator -avd android_emulator -no-skin -no-audio -no-window -gpu swiftshader_indirect -no-snapshot -no-boot-anim &\n\
\n\
# Wait for emulator to be ready\n\
echo "Waiting for emulator to start..."\n\
while [ "`adb shell getprop sys.boot_completed | tr -d '"'"'\r'"'"'`" != "1" ] ; do sleep 1; done\n\
echo "Emulator is ready"\n\
\n\
# Start Appium server\n\
appium --config /opt/appium/config.json\n\
' > /opt/start-services.sh && chmod +x /opt/start-services.sh

CMD ["/opt/start-services.sh"]