#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Screenshot Capture using PIL and webbrowser
"""

import os
import time
import subprocess
from PIL import ImageGrab

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def screenshot_page(url, filename, wait_time=3):
    """Open URL and take screenshot"""
    print(f"📷 {filename}...")

    # Open URL in default browser
    subprocess.Popen(["start", url], shell=True)
    time.sleep(wait_time)

    # Take screenshot
    img = ImageGrab.grab()
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    img.save(filepath)
    print(f"✅ Saved: {filename}")

    # Close browser window (Ctrl+W)
    os.system("taskkill /im chrome.exe /f >nul 2>&1")
    time.sleep(1)


def main():
    print("=" * 60)
    print("🎬 SCREENSHOT CAPTURE STARTED")
    print("=" * 60)

    try:
        # Task 17: Home Page (No Login)
        screenshot_page("http://localhost:5000/", "get_delivers.png", 4)

        # Task 19: Dealers by State
        screenshot_page(
            "http://localhost:5000/api/dealers/state/KS/", "dealersbystate.png", 3)

        # Task 20: Dealer Details
        screenshot_page("http://localhost:5000/api/dealers/1/",
                        "dealer_id_reviews.png", 3)

        # Task 21: Review Form
        screenshot_page("http://localhost:5000/api/reviews/",
                        "dealershi_review_submission.png", 3)

        # Task 22: Posted Review
        screenshot_page("http://localhost:5000/api/reviews/",
                        "added_review.png", 3)

        # Task 25: Deployed Landing Page
        screenshot_page(
            "https://dealership-review-app.herokuapp.com/", "deployed_landingpage.png", 5)

        # Task 26: Deployed Logged-in
        screenshot_page(
            "https://dealership-review-app.herokuapp.com/", "deployed_loggedin.jpeg", 5)

        # Task 27: Deployed Dealer Detail
        screenshot_page("https://dealership-review-app.herokuapp.com/api/dealers/1/",
                        "deployed_dealer_detail.png", 5)

        print("\n" + "=" * 60)
        print("✅ SCREENSHOTS CAPTURED!")
        print("=" * 60)
        print(f"📁 Location: {SCREENSHOT_DIR}")

        files = os.listdir(SCREENSHOT_DIR)
        print(f"📊 Total files: {len(files)}")
        for f in sorted(files):
            print(f"   ✓ {f}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
