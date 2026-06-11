#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Special screenshot capture for Admin and Logged-in pages
Uses Selenium with undetected-chromedriver to handle authentication
"""

import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def take_screenshot_selenium(url, filename, login_func=None):
    """Take screenshot using Selenium"""
    print(f"📷 Capturing: {filename}...")

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)

        # Execute login if provided
        if login_func:
            login_func(driver)

        # Wait for page to fully load
        time.sleep(2)

        filepath = os.path.join(SCREENSHOT_DIR, filename)
        driver.save_screenshot(filepath)

        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ Saved: {filename} ({file_size} bytes)")
            return True
        return False

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()


def admin_login(driver):
    """Login to admin panel"""
    try:
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")

        username_field.send_keys("admin")
        password_field.send_keys("admin123")
        login_button.click()

        # Wait for admin page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content-title"))
        )
    except Exception as e:
        print(f"Login error: {str(e)}")


def admin_logout(driver):
    """Login and then logout"""
    try:
        # First login
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")

        username_field.send_keys("admin")
        password_field.send_keys("admin123")
        login_button.click()

        # Wait for admin page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content-title"))
        )
        time.sleep(1)

        # Find and click logout button
        logout_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Log out')]")
        logout_button.click()

        time.sleep(2)
    except Exception as e:
        print(f"Logout error: {str(e)}")


def home_page_logged_in(driver):
    """Set localStorage token for logged-in state"""
    try:
        driver.execute_script("""
            localStorage.setItem('token', 'f22d7892f40d23662a82aa5fa64968b0867203a7');
            localStorage.setItem('username', 'demouser');
        """)
        driver.refresh()
        time.sleep(2)
    except Exception as e:
        print(f"Logged-in setup error: {str(e)}")


def main():
    print("=" * 60)
    print("🎬 SPECIAL SCREENSHOT CAPTURE")
    print("=" * 60 + "\n")

    success_count = 0

    # Task 12: Admin Login
    if take_screenshot_selenium("http://localhost:5000/admin/", "admin_login.png", admin_login):
        success_count += 1

    # Task 13: Admin Logout
    if take_screenshot_selenium("http://localhost:5000/admin/", "admin_logout.png", admin_logout):
        success_count += 1

    # Task 18: Home Page Logged In
    if take_screenshot_selenium("http://localhost:5000/", "get_delivers_loggedin.jpeg", home_page_logged_in):
        success_count += 1

    print("\n" + "=" * 60)
    print(f"✅ COMPLETED: {success_count}/3 special screenshots")
    print("=" * 60)
    print(f"📁 Location: {SCREENSHOT_DIR}\n")

    # List all files
    if os.path.exists(SCREENSHOT_DIR):
        files = os.listdir(SCREENSHOT_DIR)
        print(f"📊 Total files in directory ({len(files)}):")
        for f in sorted(files):
            size = os.path.getsize(os.path.join(SCREENSHOT_DIR, f))
            print(f"   ✓ {f}")


if __name__ == "__main__":
    main()
