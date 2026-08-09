from datetime import datetime, timedelta
import time

from playwright.sync_api import sync_playwright

# ==========================
# CONFIGURATION
# ==========================

URL = "https://lmsnwkrtc.in"

USERNAME = "A086384"
PASSWORD = "042004"

DIVISION = "Dharwad-Division"
DEPOT = "Dharwad-Savadatti"

LEAVE_DATE1 = "06-08-2026"
LEAVE_DATE2 = "06-08-2026"

# ==========================
# START
# ==========================

TARGET_TIME = "06:00:00"

def wait_until_target():

    target = datetime.combine(
        datetime.today(),
        datetime.strptime(TARGET_TIME, "%H:%M:%S").time()
    )

    # Start clicking 100 ms before 6 AM
    start_clicking = target - timedelta(milliseconds=100)

    print("Waiting until 05:59:59.900...")

    while datetime.now() < start_clicking:
        time.sleep(0.001)

    print("🚀 Starting rapid click mode...")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    # Accept JavaScript alerts automatically
    page.on("dialog", lambda dialog: (
        print("ALERT:", dialog.message),
        dialog.accept()
    ))

    print("Opening portal...")
    page.goto(URL)

    # ----------------------------
    # Crew Login
    # ----------------------------
    page.wait_for_selector("#btnlogin")
    page.locator("#btnlogin").click()

    # ----------------------------
    # Login
    # ----------------------------
    page.wait_for_selector("#txtUserName")

    page.fill("#txtUserName", USERNAME)
    page.fill("#txtPWD", PASSWORD)

    page.select_option("#ddlDivision", label=DIVISION)

    page.wait_for_load_state("networkidle")

    page.select_option("#ddldepot", label=DEPOT)

    page.locator("#Login1").click()

    page.wait_for_load_state("networkidle")

    print("Login Successful")

    # ----------------------------
    # Apply Leave Menu
    # ----------------------------
    page.wait_for_selector("#lnkApplyLeave")

    page.locator("#lnkApplyLeave").click()

    page.wait_for_load_state("networkidle")

    # ----------------------------
    # Wait until 6 AM
    # ----------------------------
    wait_until_target()

    # ----------------------------
    # Auto Sanction Leave
    # ----------------------------
    button = page.locator("#btnShortLeave")

    attempts = 0

    print("Starting rapid clicks...")

    while True:

        attempts += 1

        try:

            # Click using JavaScript (faster)
            page.evaluate("""
            () => {
                const btn = document.querySelector("#btnShortLeave");
                if(btn) btn.click();
            }
            """)

            # Has the button changed to "Short Leave"?
            value = page.locator("#btnShortLeave").get_attribute("value")

            if value and "Short Leave" in value:
                print(f"✅ Auto Sanction opened after {attempts} clicks")
                break

        except:
            pass

        time.sleep(0.005)

    # ----------------------------
    # Short/Long Leave
    # ----------------------------

    page.locator("#btnShortLeave").click() #chnage to #btnLongLeave for LL

    page.wait_for_selector("#CheckBox1") #chage to #CheckBox2 for EL

    # ----------------------------
    # checkbox CL/CL/CML
    # ----------------------------
    
    checkbox = page.locator("#CheckBox1") #chage to #CheckBox2 for EL

    if not checkbox.is_checked():
        checkbox.check()

    page.wait_for_timeout(1000)

    print("CL Checked:", checkbox.is_checked()) #chage for EL

    # ----------------------------
    # Fill Dates
    # ----------------------------
    page.fill("#txtFromDate", LEAVE_DATE1)
    page.fill("#txtToDate", LEAVE_DATE2)

    print("From Date:", page.locator("#txtFromDate").input_value())
    print("To Date:", page.locator("#txtToDate").input_value())

    # ----------------------------
    # Screenshot Before Submit
    # ----------------------------
    page.screenshot(
        path="before_submit.png",
        full_page=True
    )

    # ----------------------------
    # Apply Leave
    # ----------------------------
    print("Submitting...")

    page.locator("#btnSubmit").click(no_wait_after=True)

    page.wait_for_timeout(5000)

    page.screenshot(
        path="after_submit.png",
        full_page=True
    )

    print("Finished")

    input("Press ENTER to close...")

    browser.close()