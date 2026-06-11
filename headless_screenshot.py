#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Screenshot Capture using headless Chrome
"""

import os
import subprocess
import json
import time

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Try to find Chrome installation
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\Benny\AppData\Local\Google\Chrome\Application\chrome.exe",
]


def find_chrome():
    """Find Chrome executable"""
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    return None


def take_screenshot_headless(url, filename):
    """Take screenshot using headless Chrome"""
    chrome_path = find_chrome()
    if not chrome_path:
        print("⚠️ Chrome not found, skipping...")
        return False

    output_path = os.path.join(SCREENSHOT_DIR, filename)

    try:
        print(f"📷 Capturing: {filename}...")

        # Using headless Chrome to take screenshot
        cmd = [
            chrome_path,
            '--headless',
            '--disable-gpu',
            '--screenshot=' + output_path,
            '--window-size=1920,1080',
            url
        ]

        subprocess.run(cmd, timeout=15, capture_output=True)

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Saved: {filename} ({file_size} bytes)")
            return True
        else:
            print(f"⚠️ File not created: {filename}")
            return False

    except subprocess.TimeoutExpired:
        print(f"⚠️ Timeout for: {filename}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    print("=" * 60)
    print("🎬 SCREENSHOT CAPTURE STARTED")
    print("=" * 60)

    # Check Chrome
    chrome = find_chrome()
    if chrome:
        print(f"✓ Chrome found: {chrome}\n")
    else:
        print("⚠️ Chrome not found in common locations\n")
        return

    screenshots = [
        ("http://localhost:5000/", "get_delivers.png"),
        ("http://localhost:5000/api/dealers/state/KS/", "dealersbystate.png"),
        ("http://localhost:5000/api/dealers/1/", "dealer_id_reviews.png"),
        ("http://localhost:5000/api/reviews/", "dealershi_review_submission.png"),
        ("http://localhost:5000/api/reviews/", "added_review.png"),
        ("https://dealership-review-app.herokuapp.com/", "deployed_landingpage.png"),
        ("https://dealership-review-app.herokuapp.com/", "deployed_loggedin.jpeg"),
        ("https://dealership-review-app.herokuapp.com/api/dealers/1/",
         "deployed_dealer_detail.png"),
    ]

    success_count = 0
    for url, filename in screenshots:
        if take_screenshot_headless(url, filename):
            success_count += 1
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"✅ COMPLETED: {success_count}/{len(screenshots)} screenshots")
    print("=" * 60)
    print(f"📁 Location: {SCREENSHOT_DIR}\n")

    # List files
    if os.path.exists(SCREENSHOT_DIR):
        files = os.listdir(SCREENSHOT_DIR)
        print(f"📊 Files in directory ({len(files)}):")
        for f in sorted(files):
            size = os.path.getsize(os.path.join(SCREENSHOT_DIR, f))
            print(f"   ✓ {f} ({size:,} bytes)")


if __name__ == "__main__":
    main()
