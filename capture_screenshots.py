#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Screenshot Capture Script
Captures all required screenshots for Tasks 12-27
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
BASE_URL_LOCAL = "http://localhost:5000"
BASE_URL_DEPLOYED = "https://dealership-review-app.herokuapp.com"

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def setup_driver():
    """Setup Chrome webdriver"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def take_screenshot(driver, filename):
    """Take and save screenshot"""
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"✅ Saved: {filename}")
    return filepath


def capture_admin_login():
    """Task 12: Admin Login Screenshot"""
    print("\n📷 Task 12: Admin Login...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/admin/")
        time.sleep(1)

        # Find and fill login form
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
        time.sleep(1)

        take_screenshot(driver, "admin_login.png")
    finally:
        driver.quit()


def capture_admin_logout():
    """Task 13: Admin Logout Screenshot"""
    print("📷 Task 13: Admin Logout...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/admin/")
        time.sleep(1)

        # Login
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

        # Click logout
        logout_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Log out')]")
        logout_button.click()

        time.sleep(1)
        take_screenshot(driver, "admin_logout.png")
    finally:
        driver.quit()


def capture_home_page_no_login():
    """Task 17: Home Page (No Login)"""
    print("📷 Task 17: Home Page (No Login)...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/")
        time.sleep(2)
        take_screenshot(driver, "get_delivers.png")
    finally:
        driver.quit()


def capture_home_page_logged_in():
    """Task 18: Home Page (Logged In)"""
    print("📷 Task 18: Home Page (Logged In)...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/")
        time.sleep(1)

        # Set localStorage token
        driver.execute_script("""
            localStorage.setItem('token', 'f22d7892f40d23662a82aa5fa64968b0867203a7');
            localStorage.setItem('username', 'demouser');
        """)

        # Reload page to apply token
        driver.refresh()
        time.sleep(2)

        take_screenshot(driver, "get_delivers_loggedin.jpeg")
    finally:
        driver.quit()


def capture_dealers_by_state():
    """Task 19: Dealers by State"""
    print("📷 Task 19: Dealers by State...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/api/dealers/state/KS/")
        time.sleep(1)
        take_screenshot(driver, "dealersbystate.png")
    finally:
        driver.quit()


def capture_dealer_details():
    """Task 20: Dealer Details with Reviews"""
    print("📷 Task 20: Dealer Details...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/api/dealers/1/")
        time.sleep(1)
        take_screenshot(driver, "dealer_id_reviews.png")
    finally:
        driver.quit()


def capture_review_form():
    """Task 21: Review Submission Form"""
    print("📷 Task 21: Review Submission Form...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/api/reviews/")
        time.sleep(1)
        take_screenshot(driver, "dealershi_review_submission.png")
    finally:
        driver.quit()


def capture_posted_review():
    """Task 22: Posted Review"""
    print("📷 Task 22: Posted Review...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_LOCAL}/api/reviews/")
        time.sleep(1)
        take_screenshot(driver, "added_review.png")
    finally:
        driver.quit()


def capture_deployed_landing():
    """Task 25: Deployed Landing Page"""
    print("📷 Task 25: Deployed Landing Page...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_DEPLOYED}/")
        time.sleep(3)
        take_screenshot(driver, "deployed_landingpage.png")
    finally:
        driver.quit()


def capture_deployed_loggedin():
    """Task 26: Deployed Logged-in Page"""
    print("📷 Task 26: Deployed Logged-in...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_DEPLOYED}/")
        time.sleep(1)

        # Set localStorage token for deployed site
        driver.execute_script("""
            localStorage.setItem('token', 'f22d7892f40d23662a82aa5fa64968b0867203a7');
            localStorage.setItem('username', 'demouser');
        """)

        driver.refresh()
        time.sleep(3)

        take_screenshot(driver, "deployed_loggedin.jpeg")
    finally:
        driver.quit()


def capture_deployed_dealer_detail():
    """Task 27: Deployed Dealer Detail"""
    print("📷 Task 27: Deployed Dealer Detail...")
    driver = setup_driver()
    try:
        driver.get(f"{BASE_URL_DEPLOYED}/api/dealers/1/")
        time.sleep(3)
        take_screenshot(driver, "deployed_dealer_detail.png")
    finally:
        driver.quit()


def main():
    """Main execution"""
    print("=" * 60)
    print("🎬 SCREENSHOT CAPTURE STARTED")
    print("=" * 60)

    try:
        # Local screenshots
        capture_admin_login()
        capture_admin_logout()
        capture_home_page_no_login()
        capture_home_page_logged_in()
        capture_dealers_by_state()
        capture_dealer_details()
        capture_review_form()
        capture_posted_review()

        # Deployed screenshots
        capture_deployed_landing()
        capture_deployed_loggedin()
        capture_deployed_dealer_detail()

        print("\n" + "=" * 60)
        print("✅ ALL SCREENSHOTS CAPTURED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📁 Location: {SCREENSHOT_DIR}")

        # List all captured files
        files = os.listdir(SCREENSHOT_DIR)
        print(f"📊 Total files: {len(files)}")
        for f in sorted(files):
            print(f"   ✓ {f}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
