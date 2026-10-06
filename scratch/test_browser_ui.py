from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="msedge")
    
    # 1. Desktop viewport
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("http://localhost:5000")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/ui_bingo_desktop.png")
    print("1. Desktop Bingo screenshot captured.")

    # 2. Select square 0 to test target selection state
    page.click(".square-card:first-child")
    page.wait_for_timeout(300)
    page.screenshot(path="scratch/ui_bingo_selected.png")
    print("2. Selected square screenshot captured.")

    # 3. Switch to Dex tab
    page.click("#tabDex")
    page.wait_for_timeout(300)
    page.screenshot(path="scratch/ui_dex_desktop.png")
    print("3. Desktop Dex screenshot captured.")
    page.close()

    # 4. Mobile viewport (iPhone 14 screen: 390x844)
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844})
    mobile_page.goto("http://localhost:5000")
    mobile_page.wait_for_load_state("networkidle")
    mobile_page.wait_for_timeout(500)
    mobile_page.screenshot(path="scratch/ui_bingo_mobile.png")
    print("4. Mobile Bingo screenshot captured.")

    mobile_page.click("#tabDex")
    mobile_page.wait_for_timeout(300)
    mobile_page.screenshot(path="scratch/ui_dex_mobile.png")
    print("5. Mobile Dex screenshot captured.")
    mobile_page.close()

    browser.close()

print("\nAll browser verification screenshots completed successfully!")
