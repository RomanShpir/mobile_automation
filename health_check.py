#!/usr/bin/env python3
"""
Health check script for mobile automation setup
"""
import requests
import json
import sys
import time


def check_appium_server(host="localhost", port=4723, timeout=30):
    """Check if Appium server is running and responsive"""
    url = f"http://{host}:{port}/wd/hub/status"
    
    print(f"Checking Appium server at {url}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Appium server is running")
                print(f"   Build: {data.get('value', {}).get('build', {})}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"   Waiting for server... ({e})")
            time.sleep(2)
    
    print("❌ Appium server is not responding")
    return False


def check_docker_services():
    """Check Docker services status"""
    import subprocess
    
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, 
                              cwd='/home/runner/work/mobile_automation/mobile_automation')
        
        if result.returncode == 0:
            print("✅ Docker services status:")
            print(result.stdout)
            return True
        else:
            print("❌ Docker compose error:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Docker compose not found")
        return False


def main():
    """Run all health checks"""
    print("🏥 Mobile Automation Health Check\n")
    
    all_healthy = True
    
    # Check Docker services
    if not check_docker_services():
        all_healthy = False
    
    print()
    
    # Check Appium server
    if not check_appium_server():
        all_healthy = False
    
    print()
    
    if all_healthy:
        print("🎉 All systems are healthy! Ready for testing.")
        sys.exit(0)
    else:
        print("⚠️  Some issues detected. Check the output above.")
        print("💡 Try running: make restart")
        sys.exit(1)


if __name__ == "__main__":
    main()