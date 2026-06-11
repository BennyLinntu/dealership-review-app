#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Screenshot capture using pyppeteer for Admin pages and logged-in state
"""

import os
import asyncio
from pyppeteer import launch

SCREENSHOT_DIR = r"C:\Users\Benny\System File\Desktop\it\screenshoot"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


async def take_screenshot_async(url, filename, setup_func=None):
    """Take screenshot using pyppeteer"""
    print(f"📷 Capturing: {filename}...")

    browser = None
    try:
        browser = await launch({
            'headless': True,
            'args': ['--no-sandbox', '--disable-setuid-sandbox'],
            'executablePath': r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        })

        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})

        await page.goto(url, {'waitUntil': 'networkidle2'})
        await asyncio.sleep(1)

        # Execute setup function if provided
        if setup_func:
            await setup_func(page)

        await asyncio.sleep(1)

        filepath = os.path.join(SCREENSHOT_DIR, filename)
        await page.screenshot({'path': filepath, 'fullPage': True})

        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ Saved: {filename} ({file_size} bytes)")
            return True
        return False

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        return False
    finally:
        if browser:
            await browser.close()


async def admin_login(page):
    """Perform admin login"""
    try:
        # Fill username
        await page.type('input[name="username"]', 'admin')
        # Fill password
        await page.type('input[name="password"]', 'admin123')
        # Click submit
        await page.click('input[type="submit"]')
        # Wait for navigation
        await asyncio.sleep(2)
        await page.waitForSelector('.content-title', {'timeout': 10000})
    except Exception as e:
        print(f"  Login error: {str(e)}")


async def admin_logout(page):
    """Login and logout"""
    try:
        # Login
        await page.type('input[name="username"]', 'admin')
        await page.type('input[name="password"]', 'admin123')
        await page.click('input[type="submit"]')
        await asyncio.sleep(2)
        await page.waitForSelector('.content-title', {'timeout': 10000})

        # Logout
        await asyncio.sleep(1)
        await page.click('button:has-text("Log out")')
        await asyncio.sleep(2)
    except Exception as e:
        print(f"  Logout error: {str(e)}")


async def home_logged_in(page):
    """Set localStorage for logged-in state"""
    try:
        await page.evaluateOnNewDocument('''() => {
            localStorage.setItem('token', 'f22d7892f40d23662a82aa5fa64968b0867203a7');
            localStorage.setItem('username', 'demouser');
        }''')
        await page.reload({'waitUntil': 'networkidle2'})
        await asyncio.sleep(2)
    except Exception as e:
        print(f"  Logged-in setup error: {str(e)}")


async def main():
    print("=" * 60)
    print("🎬 SPECIAL SCREENSHOT CAPTURE (pyppeteer)")
    print("=" * 60 + "\n")

    success_count = 0

    # Task 12: Admin Login
    if await take_screenshot_async("http://localhost:5000/admin/", "admin_login.png", admin_login):
        success_count += 1

    # Task 13: Admin Logout
    if await take_screenshot_async("http://localhost:5000/admin/", "admin_logout.png", admin_logout):
        success_count += 1

    # Task 18: Home Page Logged In
    if await take_screenshot_async("http://localhost:5000/", "get_delivers_loggedin.jpeg", home_logged_in):
        success_count += 1

    print("\n" + "=" * 60)
    print(f"✅ COMPLETED: {success_count}/3 special screenshots")
    print("=" * 60)
    print(f"📁 Location: {SCREENSHOT_DIR}\n")

    # List all files
    if os.path.exists(SCREENSHOT_DIR):
        files = sorted(os.listdir(SCREENSHOT_DIR))
        print(f"📊 Total files in directory ({len(files)}):")
        total_size = 0
        for f in files:
            filepath = os.path.join(SCREENSHOT_DIR, f)
            size = os.path.getsize(filepath)
            total_size += size
            print(f"   ✓ {f} ({size:,} bytes)")
        print(f"\n   📊 Total size: {total_size:,} bytes")

if __name__ == "__main__":
    asyncio.run(main())
