from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
import traceback

# --- Get credentials from GitHub Secrets ---
username = os.environ['NAUKRI_USERNAME']
password = os.environ['NAUKRI_PASSWORD']

# --- Log file ---
log_file = "automation.log"

def log(message):
    print(message, flush=True)
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def capture_artifacts(driver, tag="failure"):
    try:
        driver.save_screenshot(f"{tag}.png")
    except Exception:
        pass
    try:
        with open(f"{tag}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except Exception:
        pass

# --- Set up headless Chrome ---
chrome_options = Options()
# Use the modern headless; more reliable in CI
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Big viewport reduces 'not clickable at point' issues
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    log("Starting Naukri automation...")

    # Step 1: Open login page
    driver.get("https://www.naukri.com/nlogin/login")
    wait = WebDriverWait(driver, 20)

    # Step 2: Enter username & password
    wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(username)
    driver.find_element(By.ID, "passwordField").send_keys(password)

    # Step 3: Click login (keep your selector)
    driver.find_element(By.XPATH, '//button[text()="Login"]').click()
    time.sleep(10)  # wait for redirect

    # Step 4: Go to profile
    profile_url = "https://www.naukri.com/mnjuser/profile?id=&altresid"
    driver.get(profile_url)
    time.sleep(5)

    # Step 5: Click Edit button
    edit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.edit.icon")))
    edit_button.click()

    # Step 6: Update resume headline
    textarea = wait.until(EC.visibility_of_element_located((By.ID, "resumeHeadlineTxt")))
    current_text = textarea.get_attribute("value") or ""
    new_text = current_text + " ."  # append dot to force update
    textarea.clear()
    textarea.send_keys(new_text)

    # Step 7: Click Save
    save_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-dark-ot[type='submit']")))
    save_button.click()
    time.sleep(5)

    log("Profile headline updated successfully!")

except Exception as e:
    log(f"Error occurred: {e}")
    traceback.print_exc()
    capture_artifacts(driver, "failure")

finally:
    try:
        driver.quit()
    finally:
        log("Browser closed.")
