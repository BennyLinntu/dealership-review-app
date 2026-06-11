import os
import time
import subprocess
import mss
from pathlib import Path

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
BASE = "http://localhost:7000"

Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)

urls_and_names = [
    (f"{BASE}/admin/", "admin_login.png"),           # Task 12
    (f"{BASE}/admin/logout/", "admin_logout.png"),   # Task 13
    (f"{BASE}/", "get_dealers.png"),                 # Task 17
    (f"{BASE}/", "get_dealers_loggedin.jpeg"),       # Task 18
    (f"{BASE}/fetchDealers/Kansas", "dealersbystate.png"),  # Task 19
    (f"{BASE}/fetchReviews/dealer/2", "dealer_id_reviews.png"),  # Task 20
    (f"{BASE}/", "dealership_review_submission.png"),  # Task 21
    (f"{BASE}/fetchReviews/dealer/2", "added_review.png"),  # Task 22
    (f"{BASE}/", "deployed_landingpage.png"),        # Task 25
    (f"{BASE}/", "deployed_loggedin.jpeg"),          # Task 26
    (f"{BASE}/fetchDealer/2", "deployed_dealer_detail.png"),  # Task 27
    (f"{BASE}/fetchReviews/dealer/2", "deployed_add_review.png"),  # Task 28
]

print("Opening Firefox and capturing screenshots...")
print(f"Base URL: {BASE}")
print(f"Screenshot directory: {SCREENSHOT_DIR}\n")

try:
    # Open Firefox
    firefox_cmd = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    if not os.path.exists(firefox_cmd):
        firefox_cmd = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
    
    with mss.mss() as sct:
        for idx, (url, filename) in enumerate(urls_and_names, 1):
            print(f"[{idx:2d}/12] {filename:<40s}", end="", flush=True)
            
            # Open URL in Firefox
            proc = subprocess.Popen([firefox_cmd, url, "-new-window"])
            time.sleep(4)  # Wait for page to load
            
            # Take screenshot of primary monitor
            screenshot = sct.shot()
            screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
            
            # Save screenshot
            import PIL.Image
            img = PIL.Image.frombytes('RGB', screenshot['width'], screenshot['height'], 
                                     bytes(screenshot['rgb']))
            img.save(screenshot_path)
            
            print(f" ✓")
            
            # Close Firefox
            proc.terminate()
            time.sleep(1)
    
    print("\n✓ All screenshots captured successfully!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
