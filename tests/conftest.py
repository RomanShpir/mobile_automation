# conftest.py
import os
import platform
import shutil
import subprocess
import pytest


# Repo-relative fallback (used by CI and can be used locally too)
WIN_LOCAL_APKM, REPO_APKM = os.path.join("app", "tv.twitch.android.app_26.2.4-2602046_4arch_7dpi_9fc48eed4e73a766d49eb7f8c3737e53_apkmirror.com.apkm")


def _install_bundle_via_adb(apk_path: str) -> None:
    """
    Install a plain APK or an APK bundle container (.apkm/.apks/.xapk) on the connected device/emulator.
    On Windows this uses 7zip/unzip if needed. Requires 'adb' in PATH.
    """
    # Quick probe: is it a zip-like container?
    is_zip = False
    try:
        import zipfile
        is_zip = zipfile.is_zipfile(apk_path)
    except Exception:
        pass

    if is_zip:
        import tempfile, zipfile, glob
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(apk_path) as z:
                names = z.namelist()
                has_base = any(n.endswith("base.apk") for n in names)
                if has_base:
                    z.extractall(td)
                    # collect all .apk parts (base + splits)
                    parts = sorted(glob.glob(os.path.join(td, "**", "*.apk"), recursive=True))
                    # Optional: you can filter ABI splits for x86/x86_64 here if needed.
                    if not parts:
                        raise RuntimeError("Bundle container has no *.apk parts inside.")
                    # install-multiple
                    cmd = ["adb", "install-multiple", "-r", *parts]
                    subprocess.run(cmd, check=True)
                    return

    # Fallback: plain APK
    subprocess.run(["adb", "install", "-r", apk_path], check=True)


@pytest.fixture(scope="session")
def ensure_twitch_installed() -> None:
    """
    Ensure Twitch app is installed before running tests.
    Prefers the provided Windows-local path; falls back to repo path.
    """
    # Try Windows-local path on Windows machines
    candidates = []
    if platform.system().lower().startswith("win"):
        candidates.append(WIN_LOCAL_APKM)
    candidates.append(REPO_APKM)

    pkg = None
    for c in candidates:
        if c and os.path.exists(c):
            pkg = c
            break

    if not pkg:
        raise FileNotFoundError(
            "Twitch package not found. "
            f"Looked for:\n - {WIN_LOCAL_APKM}\n - {REPO_APKM}\n"
            "Put the .apkm file at one of these locations."
        )

    # If not installed, install
    out = subprocess.run(
        ["adb", "shell", "pm", "list", "packages"],
        capture_output=True, text=True, check=True
    ).stdout
    if "tv.twitch.android.app" not in out:
        _install_bundle_via_adb(pkg)


@pytest.fixture(scope="session")
def appium_capabilities():
    """
    Base desired capabilities for Appium.
    Note: when 'app' is not provided, tests can still attach via appPackage/activity if app is preinstalled.
    """
    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        # If you prefer to launch by package/activity instead of reinstalling each run:
        "appPackage": "tv.twitch.android.app",
        "appActivity": "tv.twitch.android.app.core.MainActivity",  # adjust if needed
        "newCommandTimeout": 180,
        "uiautomator2ServerLaunchTimeout": 120000,
        "adbExecTimeout": 120000,
    }
    return caps
