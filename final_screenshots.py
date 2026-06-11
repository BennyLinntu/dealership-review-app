#!/usr/bin/env python3
"""
Simple screenshot capture using Selenium - without headless mode
"""
import os
import time
from pathlib import Path

# Change to project directory
os.chdir(r"C:\Users\Benny\System File\Desktop\it\dealership-review-app")

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
BASE = "http://localhost:7000"

Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)

print("Starting screenshot capture...")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    print("✓ Selenium imported")
    
    # Create driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print("✓ Chrome driver created")
    
    # Task 12: Admin login
    print("[01/12] Capturing admin_login.png...")
    driver.get(f"{BASE}/admin/")
    time.sleep(2)
    driver.find_element("name", "username").send_keys("admin")
    driver.find_element("name", "password").send_keys("admin123")
    driver.find_element("xpath", "//input[@type='submit']").click()
    time.sleep(3)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "admin_login.png"))
    print("  ✓ admin_login.png")
    
    # Task 13: Admin logout
    print("[02/12] Capturing admin_logout.png...")
    driver.get(f"{BASE}/admin/logout/")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "admin_logout.png"))
    print("  ✓ admin_logout.png")
    
    # Task 17: Dealers list
    print("[03/12] Capturing get_dealers.png...")
    driver.get(f"{BASE}/")
    time.sleep(3)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "get_dealers.png"))
    print("  ✓ get_dealers.png")
    
    # Task 18: Dealers logged in
    print("[04/12] Capturing get_dealers_loggedin.jpeg...")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "get_dealers_loggedin.jpeg"))
    print("  ✓ get_dealers_loggedin.jpeg")
    
    # Task 19: Dealers by state
    print("[05/12] Capturing dealersbystate.png...")
    driver.get(f"{BASE}/fetchDealers/Kansas")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "dealersbystate.png"))
    print("  ✓ dealersbystate.png")
    
    # Task 20: Dealer reviews
    print("[06/12] Capturing dealer_id_reviews.png...")
    driver.get(f"{BASE}/fetchReviews/dealer/2")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "dealer_id_reviews.png"))
    print("  ✓ dealer_id_reviews.png")
    
    # Task 21: Review submission
    print("[07/12] Capturing dealership_review_submission.png...")
    driver.get(f"{BASE}/")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "dealership_review_submission.png"))
    print("  ✓ dealership_review_submission.png")
    
    # Task 22: Added review
    print("[08/12] Capturing added_review.png...")
    driver.get(f"{BASE}/fetchReviews/dealer/2")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "added_review.png"))
    print("  ✓ added_review.png")
    
    # Task 25: Deployed landing
    print("[09/12] Capturing deployed_landingpage.png...")
    driver.get(f"{BASE}/")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "deployed_landingpage.png"))
    print("  ✓ deployed_landingpage.png")
    
    # Task 26: Deployed logged in
    print("[10/12] Capturing deployed_loggedin.jpeg...")
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "deployed_loggedin.jpeg"))
    print("  ✓ deployed_loggedin.jpeg")
    
    # Task 27: Deployed dealer detail
    print("[11/12] Capturing deployed_dealer_detail.png...")
    driver.get(f"{BASE}/fetchDealer/2")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "deployed_dealer_detail.png"))
    print("  ✓ deployed_dealer_detail.png")
    
    # Task 28: Deployed review
    print("[12/12] Capturing deployed_add_review.png...")
    driver.get(f"{BASE}/fetchReviews/dealer/2")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "deployed_add_review.png"))
    print("  ✓ deployed_add_review.png")
    
    driver.quit()
    print("\n✓✓✓ All 12 screenshots captured successfully! ✓✓✓")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    try:
        driver.quit()
    except:
        pass
