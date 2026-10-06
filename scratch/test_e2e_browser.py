from playwright.sync_api import sync_playwright
import time
import os

print("Starting end-to-end browser test with Edge...")

sample_path = os.path.abspath("samples/sample_leaf.jpg")
assert os.path.exists(sample_path), f"Sample file not found: {sample_path}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="msedge")
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    # Open page
    page.goto("http://localhost:5000")
    page.wait_for_load_state("networkidle")
    
    # Verify title
    print("Page title:", page.title())
    assert "Grassdex" in page.title()
    
    # Click Square #4 (index 3, usually open)
    cards = page.query_selector_all(".square-card")
    print(f"Found {len(cards)} bingo cards")
    cards[3].click()
    page.wait_for_timeout(300)
    
    # Upload sample file to file input #photoInput
    file_input = page.query_selector("#photoInput")
    print("Uploading sample file to #photoInput and awaiting /api/identify...")
    with page.expect_response(lambda res: "/api/identify" in res.url, timeout=40000) as response_info:
        file_input.set_input_files(sample_path)
    
    response = response_info.value
    print(f"POST /api/identify returned HTTP {response.status}")
    print("Response JSON:", response.json())
    
    page.wait_for_timeout(1000)
    page.screenshot(path="scratch/ui_e2e_after_upload.png")
    print("Screenshot saved to scratch/ui_e2e_after_upload.png")
    
    # Switch to Dex to see the new entry
    page.click("#tabDex")
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/ui_e2e_dex_view.png")
    print("Screenshot saved to scratch/ui_e2e_dex_view.png")
    
    browser.close()

print("E2E test successfully completed!")
