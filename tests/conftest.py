# conftest.py
import os
import re
import time
import tempfile
import zipfile
import glob
import subprocess
from typing import Generator

import pytest
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from pathlib import Path
from datetime import datetime

# Repo-relative fallback path (used in CI with Git LFS)
REPO_APKM = os.path.join(
    "app",
    "tv.twitch.android.app_26.2.4-2602046_4arch_7dpi_9fc48eed4e73a766d49eb7f8c3737e53_apkmirror.com.apkm",
)


def _install_bundle_via_adb(apk_path: str) -> None:
    """
    Install a plain APK or a bundle container (.apkm/.apks/.xapk).
    Uses 'adb install-multiple' for bundles; 'adb install' for a single APK.
    Requires 'adb' in PATH.
    """
    is_zip = zipfile.is_zipfile(apk_path)
    if is_zip:
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(apk_path) as z:
                names = z.namelist()
                has_base = any(n.endswith("base.apk") for n in names)
                if has_base:
                    z.extractall(td)
                    parts = sorted(glob.glob(os.path.join(td, "**", "*.apk"), recursive=True))
                    if not parts:
                        raise RuntimeError("Bundle container has no *.apk parts inside.")
                    subprocess.run(["adb", "install-multiple", "-r", *parts], check=True)
                    return
    # Fallback: treat as a single APK
    subprocess.run(["adb", "install", "-r", apk_path], check=True)


@pytest.fixture(scope="session")
def ensure_twitch_installed() -> None:
    """
    Ensure Twitch package is installed on the device/emulator BEFORE tests.
    - Prefer LOCAL_APKM env path (set in CI workflow)
    - Fallback to the repo-local path (REPO_APKM)
    """
    candidates = []
    env_apkm = os.getenv("LOCAL_APKM")
    if env_apkm:
        candidates.append(env_apkm)
    candidates.append(REPO_APKM)

    pkg_path = next((p for p in candidates if p and os.path.exists(p)), None)
    if not pkg_path:
        raise FileNotFoundError(
            "Twitch package not found. Looked for:\n"
            f" - {env_apkm or '(unset)'}\n"
            f" - {REPO_APKM}\n"
            "Place the .apkm at one of these locations (CI uses the repo path via Git LFS)."
        )

    out = subprocess.run(
        ["adb", "shell", "pm", "list", "packages"],
        capture_output=True, text=True, check=True
    ).stdout
    if "tv.twitch.android.app" not in out:
        _install_bundle_via_adb(pkg_path)


@pytest.fixture(scope="session")
def appium_capabilities() -> dict:
    """
    Base desired capabilities. Do NOT set appActivity here; it will be detected at runtime.
    """
    return {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "appPackage": "tv.twitch.android.app",
        "newCommandTimeout": 180,
        "uiautomator2ServerLaunchTimeout": 120000,
        "adbExecTimeout": 120000,
        # keep install/launch behavior sane between retries
        "noReset": True,
        "dontStopAppOnReset": False,
    }


def _detect_launcher_activity(pkg: str) -> str:
    """
    Detect the LAUNCHER activity for a package.
    Supports both 'cmp=' output and 'name=' output formats.
    Returns fully qualified activity name.
    """
    cmd = [
        "adb", "shell", "cmd", "package", "resolve-activity",
        "-a", "android.intent.action.MAIN",
        "-c", "android.intent.category.LAUNCHER",
        pkg
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout

    # Format 1: "... cmp=pkg/.SomeActivity"
    m = re.search(r"cmp=([\w.]+)/(\S+)", out)
    if m:
        pkg_found, act = m.group(1), m.group(2)
        if act.startswith("."):
            act = pkg_found + act
        return act

    # Format 2: verbose dump with "name=fully.qualified.Activity"
    m2 = re.search(r"\bname=([A-Za-z0-9_.]+)", out)
    if m2:
        act = m2.group(1)
        if act.startswith("."):
            act = f"{pkg}{act}"
        return act

    raise RuntimeError(f"Cannot resolve LAUNCHER activity for {pkg}. Raw:\n{out}")


@pytest.fixture(scope="session")
def driver(ensure_twitch_installed, appium_capabilities) -> Generator[WebDriver, None, None]:
    """
    Create a single Appium driver session for the whole test session.
    Auto-detects the correct LAUNCHER activity and injects it into capabilities.
    """
    # Fast ADB sanity
    state = subprocess.run(["adb", "get-state"], capture_output=True, text=True, check=True).stdout.strip()
    if state != "device":
        pytest.skip(f"ADB state is '{state}', not 'device'")

    # Copy + patch caps
    caps = dict(appium_capabilities)
    pkg = caps.get("appPackage", "tv.twitch.android.app")

    try:
        detected_activity = _detect_launcher_activity(pkg)  # e.g. tv.twitch.android.app.core.LandingActivity
    except Exception as e:
        pytest.fail(f"Failed to detect launcher activity for {pkg}: {e}")

    caps["appPackage"] = pkg
    caps["appActivity"] = detected_activity
    caps.setdefault("appWaitPackage", pkg)
    caps.setdefault("appWaitActivity", f"{pkg}.*")
    # IMPORTANT: this must be a boolean, not a string
    caps.setdefault("appWaitForLaunch", True)

    # Build options
    opts = UiAutomator2Options()
    for k, v in caps.items():
        opts.set_capability(k, v)

    server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

    drv: WebDriver | None = None
    last_err: Exception | None = None
    for attempt in range(1, 6):
        try:
            drv = appium_webdriver.Remote(command_executor=server_url, options=opts)
            # Touch the session to ensure it's alive
            _ = drv.current_activity
            break
        except Exception as e:
            last_err = e
            time.sleep(2 * attempt)

    if drv is None:
        pytest.fail(f"Failed to create Appium session after retries: {last_err}")

    try:
        yield drv
    finally:
        try:
            drv.quit()
        except Exception:
            pass

# --- screenshots on failure ----------------------------------------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("tests/_artifacts", exist_ok=True)
            name = re.sub(r"[^A-Za-z0-9_.-]", "_", item.name)
            path = os.path.join("tests/_artifacts", f"{name}.png")
            try:
                drv.save_screenshot(path)
                print(f"[ARTIFACT] Saved screenshot: {path}")
            except Exception as e:
                print(f"[ARTIFACT] Failed to save screenshot: {e}")

@pytest.fixture(autouse=True)
def _screenshot_on_fail(request, driver: WebDriver):
    """
    Automatically take a screenshot if a test fails.
    Works for failures in setup or during the test body.
    """
    yield  # run the test
    # after test, check the outcome
    take = False
    rep_call = getattr(request.node, "rep_call", None)
    rep_setup = getattr(request.node, "rep_setup", None)
    if rep_setup and rep_setup.failed:
        take = True
    if rep_call and rep_call.failed:
        take = True

    if take:
        # ensure output dir exists
        out_dir = Path("reports") / "screenshots"
        out_dir.mkdir(parents=True, exist_ok=True)

        # filename: <testname>__YYYYmmdd-HHMMSS.png
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = request.node.name.replace(os.sep, "_").replace(" ", "_")
        png_path = out_dir / f"{safe_name}__{ts}.png"

        try:
            driver.get_screenshot_as_file(str(png_path))
            print(f"[SCREENSHOT] saved to {png_path}")
        except Exception as e:
            print(f"[SCREENSHOT] failed: {e}")
