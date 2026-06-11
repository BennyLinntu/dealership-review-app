import os
import time
from pathlib import Path

os.chdir(r"C:\Users\Benny\System File\Desktop\it\dealership-review-app")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    print("✓ Imports OK")

    # Setup driver
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("✓ Driver created")

    # Test connection
    driver.get("http://localhost:7000/")
    print("✓ Connected to server")
    time.sleep(2)

    # Test screenshot
    screenshot_dir = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
    Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(os.path.join(screenshot_dir, "test_screenshot.png"))
    print("✓ Screenshot saved successfully!")

    driver.quit()
    print("✓ Complete")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
