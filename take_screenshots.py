import subprocess
import sys
import time
import requests
from playwright.sync_api import sync_playwright

def wait_for_server(url="http://127.0.0.1:8000/docs"):
    for _ in range(30):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except:
            time.sleep(0.5)
    return False

def take_screenshots():
    print("Starting Task 1 server...")
    server1 = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app"], cwd="task_1")
    if not wait_for_server():
        print("Server 1 failed to start")
        server1.terminate()
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 1024})
        
        # TASK 1
        page = context.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.wait_for_selector(".swagger-ui")
        time.sleep(2)
        page.screenshot(path="Screenshots/task1_overview.png")

        # Task 1 POST (valid)
        page.locator("div.opblock-summary-post:has-text('/items')").click()
        page.locator("button:has-text('Try it out')").first.click()
        page.locator("textarea").first.fill('{\n  "title": "Lost Wallet",\n  "description": "Black leather wallet",\n  "category": "Accessories",\n  "location": "Cafeteria",\n  "reported_by": "Alice",\n  "status": "Lost"\n}')
        page.locator(".opblock-post").first.locator("button:has-text('Execute')").click()
        page.wait_for_selector("td.response-col_status:has-text('201')", timeout=5000)
        page.locator(".opblock-post").first.screenshot(path="Screenshots/task1_post.png")
        
        # Task 1 POST (invalid)
        page.locator("textarea").first.fill('{\n  "title": "",\n  "description": "Black leather wallet",\n  "category": "Accessories",\n  "location": "Cafeteria",\n  "reported_by": "Alice",\n  "status": "InvalidStatus"\n}')
        page.locator(".opblock-post").first.locator("button:has-text('Execute')").click()
        page.wait_for_selector("td.response-col_status:has-text('422')", timeout=5000)
        page.locator(".opblock-post").first.screenshot(path="Screenshots/task1_invalid.png")

        browser.close()

    server1.terminate()
    server1.wait()
    print("Task 1 screenshots done.")

    print("Starting Task 2 server...")
    server2 = subprocess.Popen([sys.executable, "-m", "uvicorn", "task_2.main:app"])
    if not wait_for_server():
        print("Server 2 failed to start")
        server2.terminate()
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 1024})
        
        # TASK 2
        page = context.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.wait_for_selector(".swagger-ui")
        time.sleep(2)
        page.screenshot(path="Screenshots/task2_overview.png")

        # Task 2 POST /events
        page.locator("div.opblock-summary-post:has-text('/events')").first.click()
        page.locator("button:has-text('Try it out')").first.click()
        page.locator("textarea").first.fill('{\n  "title": "Hackathon 2026",\n  "venue": "Main Hall",\n  "capacity": 2,\n  "organizer": "Tech Club",\n  "status": "Open"\n}')
        page.locator(".opblock-post").first.locator("button:has-text('Execute')").click()
        page.wait_for_selector("td.response-col_status:has-text('201')", timeout=5000)
        page.locator(".opblock-post").first.screenshot(path="Screenshots/task2_post_event.png")

        # Task 2 POST /reserve
        page.locator("div.opblock-summary-post:has-text('/events/{event_id}/reserve')").click()
        page.locator("button:has-text('Try it out')").first.click()
        page.locator("input[placeholder='event_id']").fill("1")
        page.locator("textarea").first.fill('{\n  "student_name": "Bob",\n  "roll_number": "R123",\n  "email": "bob@example.com"\n}')
        page.locator(".opblock-post").nth(1).locator("button:has-text('Execute')").click()
        page.wait_for_selector("td.response-col_status:has-text('201')", timeout=5000)
        page.locator(".opblock-post").nth(1).screenshot(path="Screenshots/task2_reservation.png")
        
        # Task 2 POST /reserve (Full capacity error)
        # Create second reservation (works, capacity 2)
        page.locator("textarea").first.fill('{\n  "student_name": "Charlie",\n  "roll_number": "R124",\n  "email": "charlie@example.com"\n}')
        page.locator(".opblock-post").nth(1).locator("button:has-text('Execute')").click()
        time.sleep(1)
        
        # Create third reservation (should fail with 400 Event is already full)
        page.locator("textarea").first.fill('{\n  "student_name": "Dave",\n  "roll_number": "R125",\n  "email": "dave@example.com"\n}')
        page.locator(".opblock-post").nth(1).locator("button:has-text('Execute')").click()
        page.wait_for_selector("td.response-col_status:has-text('400')", timeout=5000)
        page.locator(".opblock-post").nth(1).screenshot(path="Screenshots/task2_overbooking.png")

        browser.close()

    server2.terminate()
    server2.wait()
    print("Task 2 screenshots done.")

if __name__ == '__main__':
    take_screenshots()
