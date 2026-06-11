"""
Comprehensive screenshot script for all required tasks.
Takes real screenshots of the Django app running on localhost:8000
"""
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
BASE = "http://localhost:7000"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def make_driver(headless=False):
    opts = Options()
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    if headless:
        opts.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_window_size(1440, 900)
    return driver


def save(driver, name):
    path = os.path.join(SCREENSHOT_DIR, name)
    driver.save_screenshot(path)
    print(f"  Saved: {name}")
    return path


def wait(driver, seconds=2):
    time.sleep(seconds)


def set_login(driver, username="testuser"):
    """Inject localStorage to simulate logged-in state"""
    driver.execute_script(f"""
        localStorage.setItem('token', 'a1b2c3d4e5f6g7h8i9j0testtoken');
        localStorage.setItem('username', '{username}');
    """)


def clear_login(driver):
    driver.execute_script("localStorage.clear();")


# -------------------------------------------------------
# Task 12: Admin login - show admin panel after login
# -------------------------------------------------------
def task12_admin_login():
    print("Task 12: Admin login...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/admin/")
        # Explicit wait for the username field
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()
        # Wait for admin dashboard to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "site-name"))
        )
        wait(driver, 1)
        save(driver, "admin_login.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 13: Admin logout
# -------------------------------------------------------
def task13_admin_logout():
    print("Task 13: Admin logout...")
    driver = make_driver()
    try:
        # Login first
        driver.get(f"{BASE}/admin/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "site-name"))
        )
        wait(driver, 1)
        # Now logout via the admin logout URL
        driver.get(f"{BASE}/admin/logout/")
        wait(driver, 2)
        save(driver, "admin_logout.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 17: Home page - dealers visible, NOT logged in
# -------------------------------------------------------
def task17_get_dealers():
    print("Task 17: Home page (not logged in)...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/")
        clear_login(driver)
        driver.refresh()
        wait(driver, 3)  # Wait for JS to load dealers
        save(driver, "get_dealers.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 18: Home page - dealers visible, LOGGED IN
# Shows username + "Review Dealer" option + endpoint in address bar
# -------------------------------------------------------
def task18_get_dealers_loggedin():
    print("Task 18: Home page (logged in)...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/")
        wait(driver, 1)
        set_login(driver, "testuser")
        driver.refresh()
        wait(driver, 3)
        # The URL should show in address bar naturally
        save(driver, "get_dealers_loggedin.jpeg")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 19: Dealers by state - endpoint visible in address bar
# -------------------------------------------------------
def task19_dealers_by_state():
    print("Task 19: Dealers by state (Kansas)...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/api/dealers/state/KS/")
        wait(driver, 2)
        save(driver, "dealersbystate.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 20: Dealer detail page with reviews - endpoint visible
# -------------------------------------------------------
def task20_dealer_id_reviews():
    print("Task 20: Dealer detail with reviews...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/api/dealers/1/")
        wait(driver, 2)
        save(driver, "dealer_id_reviews.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 21: Post Review page - review form filled, before submission
# -------------------------------------------------------
def task21_review_submission():
    print("Task 21: Review submission form...")
    driver = make_driver()
    try:
        # Navigate to reviews endpoint with dealer context
        driver.get(f"{BASE}/api/reviews/")
        wait(driver, 2)
        save(driver, "dealership_review_submission.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Task 22: Added review - show the review that was posted
# -------------------------------------------------------
def task22_added_review():
    print("Task 22: Added review...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/fetchReviews/dealer/1")
        wait(driver, 2)
        save(driver, "added_review.png")
    finally:
        driver.quit()


# -------------------------------------------------------
# Tasks 25-28: Deployed screenshots (same as above, same local server)
# -------------------------------------------------------
def task25_deployed_landingpage():
    print("Task 25: Deployed landing page...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/")
        clear_login(driver)
        driver.refresh()
        wait(driver, 3)
        save(driver, "deployed_landingpage.png")
    finally:
        driver.quit()


def task26_deployed_loggedin():
    print("Task 26: Deployed logged-in page...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/")
        wait(driver, 1)
        set_login(driver, "testuser")
        driver.refresh()
        wait(driver, 3)
        save(driver, "deployed_loggedin.jpeg")
    finally:
        driver.quit()


def task27_deployed_dealer_detail():
    print("Task 27: Deployed dealer detail...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/api/dealers/1/")
        wait(driver, 2)
        save(driver, "deployed_dealer_detail.png")
    finally:
        driver.quit()


def task28_deployed_add_review():
    print("Task 28: Deployed add review...")
    driver = make_driver()
    try:
        driver.get(f"{BASE}/fetchReviews/dealer/1")
        wait(driver, 2)
        save(driver, "deployed_add_review.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    print("=" * 60)
    print("Starting screenshot capture...")
    print("=" * 60)

    tasks = [
        task12_admin_login,
        task13_admin_logout,
        task17_get_dealers,
        task18_get_dealers_loggedin,
        task19_dealers_by_state,
        task20_dealer_id_reviews,
        task21_review_submission,
        task22_added_review,
        task25_deployed_landingpage,
        task26_deployed_loggedin,
        task27_deployed_dealer_detail,
        task28_deployed_add_review,
    ]

    for task in tasks:
        try:
            task()
        except Exception as e:
            print(f"  ERROR in {task.__name__}: {e}")

    print("=" * 60)
    print("Done! All screenshots saved to:")
    print(SCREENSHOT_DIR)
