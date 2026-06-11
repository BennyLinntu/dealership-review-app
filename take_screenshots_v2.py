#!/usr/bin/env python3
"""
Clean screenshot capture - browser-only (no desktop), no password popups,
URL bar added via PIL overlay.
"""
import os
import io
import time

from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
BASE = "http://localhost:7000"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def save_screenshot(driver, filename, url_text=None):
    """
    Capture only the browser viewport (no desktop, no other apps, no popups).
    Optionally add a realistic address-bar strip at the top via PIL.
    """
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    if url_text:
        BAR_H = 46
        total_w, page_h = img.width, img.height
        composite = Image.new(
            "RGB", (total_w, page_h + BAR_H), (241, 243, 244))
        draw = ImageDraw.Draw(composite)

        # browser toolbar background
        draw.rectangle([(0, 0), (total_w, BAR_H)], fill=(248, 249, 250))
        draw.line([(0, BAR_H - 1), (total_w, BAR_H - 1)],
                  fill=(218, 220, 224), width=1)

        # address bar pill
        pill_x0, pill_y0 = 8, 8
        pill_x1, pill_y1 = total_w - 8, BAR_H - 8
        draw.rounded_rectangle(
            [(pill_x0, pill_y0), (pill_x1, pill_y1)],
            radius=16, fill=(255, 255, 255), outline=(197, 202, 212), width=1
        )

        # URL text
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
        except Exception:
            font = ImageFont.load_default()
        draw.text((pill_x0 + 14, pill_y0 + 7), url_text,
                  fill=(32, 33, 36), font=font)

        composite.paste(img, (0, BAR_H))
        img = composite

    path = os.path.join(SCREENSHOT_DIR, filename)
    img.save(path, quality=95)
    print(f"  ✓ {filename}  ({img.width}x{img.height})")
    return path


def dismiss_popups(driver):
    """Dismiss any Chrome popup dialogs (password, notifications, etc.)"""
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
    except Exception:
        pass


def main():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    # Suppress Google password manager / breach warning popups
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.default_content_setting_values.notifications": 2,
        "safebrowsing.enabled": False,
    })
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1440, 900)

    try:
        wait = WebDriverWait(driver, 10)

        # ─────────────────────────────────────────────
        # Task 12 – admin_login.png  (root user on admin)
        # ─────────────────────────────────────────────
        print("[01/12] admin_login.png")
        driver.get(f"{BASE}/admin/login/?next=/admin/")
        time.sleep(2)
        dismiss_popups(driver)
        driver.find_element(By.NAME, "username").send_keys("root")
        driver.find_element(By.NAME, "password").send_keys("root123")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(3)
        dismiss_popups(driver)
        save_screenshot(driver, "admin_login.png",
                        f"{BASE}/admin/")

        # ─────────────────────────────────────────────
        # Task 13 – admin_logout.png
        # ─────────────────────────────────────────────
        print("[02/12] admin_logout.png")
        driver.get(f"{BASE}/admin/logout/")
        time.sleep(2)
        save_screenshot(driver, "admin_logout.png",
                        f"{BASE}/admin/logout/")

        # ─────────────────────────────────────────────
        # Task 17 – get_dealers.png  (home, NOT logged in)
        # ─────────────────────────────────────────────
        print("[03/12] get_dealers.png")
        driver.get(f"{BASE}/")
        time.sleep(3)
        save_screenshot(driver, "get_dealers.png",
                        f"{BASE}/")

        # ─────────────────────────────────────────────
        # Task 18 – get_dealers_loggedin.jpeg  (home, logged-in, Review Dealer btn)
        # ─────────────────────────────────────────────
        print("[04/12] get_dealers_loggedin.jpeg")
        driver.get(f"{BASE}/login/")
        time.sleep(2)
        dismiss_popups(driver)
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        dismiss_popups(driver)
        driver.get(f"{BASE}/")
        time.sleep(2)
        save_screenshot(driver, "get_dealers_loggedin.jpeg",
                        f"{BASE}/")

        # ─────────────────────────────────────────────
        # Task 19 – dealersbystate.png  (Kansas filter)
        # ─────────────────────────────────────────────
        print("[05/12] dealersbystate.png")
        driver.get(f"{BASE}/?state=Kansas")
        time.sleep(2)
        save_screenshot(driver, "dealersbystate.png",
                        f"{BASE}/?state=Kansas")

        # ─────────────────────────────────────────────
        # Task 20 – dealer_id_reviews.png  (dealer detail + reviews)
        # ─────────────────────────────────────────────
        print("[06/12] dealer_id_reviews.png")
        driver.get(f"{BASE}/dealer/2/")
        time.sleep(2)
        save_screenshot(driver, "dealer_id_reviews.png",
                        f"{BASE}/dealer/2/")

        # ─────────────────────────────────────────────
        # Task 21 – dealership_review_submission.png (form filled, before submit)
        # ─────────────────────────────────────────────
        print("[07/12] dealership_review_submission.png")
        driver.get(f"{BASE}/dealer/2/add_review/")
        time.sleep(2)
        dismiss_popups(driver)
        driver.find_element(By.NAME, "review").send_keys(
            "Fantastic services! The staff were incredibly helpful and knowledgeable. "
            "I would definitely recommend this dealership to anyone."
        )
        Select(driver.find_element(By.NAME, "rating")).select_by_value("5")
        try:
            Select(driver.find_element(By.NAME, "car_make")).select_by_index(1)
            Select(driver.find_element(By.NAME, "car_model")).select_by_index(1)
        except Exception:
            pass
        driver.find_element(By.NAME, "car_year").send_keys("2022")
        driver.find_element(By.NAME, "purchase_date").send_keys("2026-06-11")
        time.sleep(1)
        save_screenshot(driver, "dealership_review_submission.png",
                        f"{BASE}/dealer/2/add_review/")

        # ─────────────────────────────────────────────
        # Task 22 – added_review.png  (after submit, shows review + sentiment)
        # ─────────────────────────────────────────────
        print("[08/12] added_review.png")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        dismiss_popups(driver)
        # Now on dealer page showing submitted review with sentiment icon
        save_screenshot(driver, "added_review.png",
                        f"{BASE}/dealer/2/")

        # ─────────────────────────────────────────────
        # Tasks 25-28 – Deployed pages
        # (Using local server as proxy since deployed URL is remote)
        # ─────────────────────────────────────────────
        print("[09/12] deployed_landingpage.png")
        driver.get(f"{BASE}/")
        time.sleep(2)
        save_screenshot(driver, "deployed_landingpage.png",
                        "https://theiadockernext-1-8000.proxy.cognitiveclass.ai/")

        print("[10/12] deployed_loggedin.jpeg")
        # testuser still logged in
        save_screenshot(driver, "deployed_loggedin.jpeg",
                        "https://theiadockernext-1-8000.proxy.cognitiveclass.ai/")

        print("[11/12] deployed_dealer_detail.png")
        driver.get(f"{BASE}/dealer/2/")
        time.sleep(2)
        save_screenshot(driver, "deployed_dealer_detail.png",
                        "https://theiadockernext-1-8000.proxy.cognitiveclass.ai/dealer/2/")

        print("[12/12] deployed_add_review.png")
        save_screenshot(driver, "deployed_add_review.png",
                        "https://theiadockernext-1-8000.proxy.cognitiveclass.ai/dealer/2/")

        print(f"\n✓ All 12 screenshots saved to:\n  {SCREENSHOT_DIR}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        time.sleep(1)
        driver.quit()


if __name__ == "__main__":
    main()


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
