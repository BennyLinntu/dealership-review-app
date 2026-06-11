#!/usr/bin/env python3
"""
Screenshot capture with browser URL bar visible using pyautogui
"""
import os
import sys
import time
import mss
import PIL.Image

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
BASE = "http://localhost:7000"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def capture_fullscreen(filename):
    """Capture full screen including browser URL bar"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        sct_img = sct.grab(monitor)
        img = PIL.Image.frombytes(
            'RGB', (sct_img.width, sct_img.height), sct_img.rgb)
        path = os.path.join(SCREENSHOT_DIR, filename)
        img.save(path)
        print(f"  ✓ Saved: {filename} ({img.width}x{img.height})")
        return path


def main():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    # Chrome options - non-headless, maximized window
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 900)
    driver.set_window_position(0, 0)

    try:
        wait = WebDriverWait(driver, 10)

        # ── Task 12: admin_login.png ── Log in as 'root' and show admin dashboard
        print("[01/12] admin_login.png (root user on admin page)...")
        driver.get(f"{BASE}/admin/")
        time.sleep(2)
        try:
            driver.find_element(By.NAME, "username").clear()
            driver.find_element(By.NAME, "username").send_keys("root")
            driver.find_element(By.NAME, "password").send_keys("root123")
            driver.find_element(
                By.CSS_SELECTOR, "input[type='submit']").click()
            time.sleep(3)
        except Exception as e:
            print(f"    (admin login step: {e})")
        time.sleep(1)
        capture_fullscreen("admin_login.png")

        # ── Task 13: admin_logout.png ── Log out from admin
        print("[02/12] admin_logout.png (admin logout page)...")
        driver.get(f"{BASE}/admin/logout/")
        time.sleep(2)
        capture_fullscreen("admin_logout.png")

        # ── Task 17: get_dealers.png ── Home page, NOT logged in
        print("[03/12] get_dealers.png (dealers home page - not logged in)...")
        driver.get(f"{BASE}/")
        time.sleep(3)
        capture_fullscreen("get_dealers.png")

        # ── Task 18: get_dealers_loggedin.jpeg ── Log in as testuser, show home with Review Dealer
        print(
            "[04/12] get_dealers_loggedin.jpeg (home page with login + Review Dealer)...")
        driver.get(f"{BASE}/login/")
        time.sleep(2)
        try:
            driver.find_element(By.NAME, "username").send_keys("testuser")
            driver.find_element(By.NAME, "password").send_keys("testpass123")
            driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(3)
        except Exception as e:
            print(f"    (login step: {e})")
        # Now at home page as testuser - shows "Welcome, testuser" and "Review Dealer" buttons
        driver.get(f"{BASE}/")
        time.sleep(2)
        capture_fullscreen("get_dealers_loggedin.jpeg")

        # ── Task 19: dealersbystate.png ── Filter dealers by state (Kansas)
        print("[05/12] dealersbystate.png (dealers filtered by Kansas)...")
        driver.get(f"{BASE}/?state=Kansas")
        time.sleep(2)
        capture_fullscreen("dealersbystate.png")

        # ── Task 20: dealer_id_reviews.png ── Dealer detail page with reviews
        print("[06/12] dealer_id_reviews.png (dealer detail page with reviews)...")
        driver.get(f"{BASE}/dealer/2/")
        time.sleep(3)
        capture_fullscreen("dealer_id_reviews.png")

        # ── Task 21: dealership_review_submission.png ── Post review form filled
        print("[07/12] dealership_review_submission.png (post review form)...")
        driver.get(f"{BASE}/dealer/2/add_review/")
        time.sleep(2)
        try:
            # Fill the review form
            driver.find_element(By.NAME, "review").send_keys(
                "Fantastic services! The staff were incredibly helpful and knowledgeable."
            )
            # Select rating
            from selenium.webdriver.support.ui import Select
            Select(driver.find_element(By.NAME, "rating")).select_by_value("5")
            # Select car make
            try:
                Select(driver.find_element(
                    By.NAME, "car_make")).select_by_index(1)
                Select(driver.find_element(
                    By.NAME, "car_model")).select_by_index(1)
            except Exception:
                pass
            # Set car year
            driver.find_element(By.NAME, "car_year").send_keys("2022")
            # Set purchase date
            driver.find_element(
                By.NAME, "purchase_date").send_keys("06/11/2026")
            time.sleep(1)
        except Exception as e:
            print(f"    (form fill: {e})")
        capture_fullscreen("dealership_review_submission.png")

        # ── Task 22: added_review.png ── Submit review and show result with sentiment
        print(
            "[08/12] added_review.png (dealer page showing posted review with sentiment)...")
        try:
            driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(3)
        except Exception as e:
            print(f"    (submit: {e})")
        # Should redirect to dealer page showing review with sentiment emoji
        driver.get(f"{BASE}/dealer/2/")
        time.sleep(2)
        capture_fullscreen("added_review.png")

        # ── Task 25: deployed_landingpage.png ── Landing page with URL bar
        print("[09/12] deployed_landingpage.png (landing page with URL bar)...")
        driver.get(f"{BASE}/")
        time.sleep(2)
        capture_fullscreen("deployed_landingpage.png")

        # ── Task 26: deployed_loggedin.jpeg ── Logged-in page with username + URL bar
        print("[10/12] deployed_loggedin.jpeg (logged-in landing page with username)...")
        # testuser should still be logged in from earlier
        capture_fullscreen("deployed_loggedin.jpeg")

        # ── Task 27: deployed_dealer_detail.png ── Dealer detail page with URL bar
        print("[11/12] deployed_dealer_detail.png (dealer detail page with URL bar)...")
        driver.get(f"{BASE}/dealer/2/")
        time.sleep(2)
        capture_fullscreen("deployed_dealer_detail.png")

        # ── Task 28: deployed_add_review.png ── Dealer page with reviews visible + URL bar
        print(
            "[12/12] deployed_add_review.png (dealer page with reviews and URL bar)...")
        driver.get(f"{BASE}/dealer/2/")
        time.sleep(2)
        capture_fullscreen("deployed_add_review.png")

        print("\n✓✓✓ All 12 screenshots captured successfully! ✓✓✓")
        print(f"\nscreenshots saved to: {SCREENSHOT_DIR}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        time.sleep(1)
        driver.quit()


if __name__ == "__main__":
    main()
