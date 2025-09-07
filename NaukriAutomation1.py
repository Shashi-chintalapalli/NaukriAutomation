from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

# Use GitHub Secrets for credentials
username = os.environ['NAUKRI_USERNAME']
password = os.environ['NAUKRI_PASSWORD']

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # run without GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Step 1: Open Naukri login page
    driver.get("https://www.naukri.com/nlogin/login")

    wait = WebDriverWait(driver, 10)

    # Step 2: Enter username and password
    wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(username)
    driver.find_element(By.ID, "passwordField").send_keys(password)

    # Step 3: Click Login button
    driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    # Step 4: Wait until login is successful
    time.sleep(10)  # adjust if needed

    # Step 5: Navigate to your profile page directly
    profile_url = "https://www.naukri.com/mnjuser/profile?id=&altresid"
    driver.get(profile_url)

    time.sleep(5)

    # Step 6: Click the Edit button for Resume Headline
    edit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.edit.icon")))
    edit_button.click()

    # Step 7: Append a dot or space to force update
    textarea = wait.until(EC.visibility_of_element_located((By.ID, "resumeHeadlineTxt")))
    current_text = textarea.get_attribute("value")
    new_text = current_text + " ."
    textarea.clear()
    textarea.send_keys(new_text)

    # Step 8: Click Save button
    save_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-dark-ot[type='submit']")))
    save_button.click()

    time.sleep(5)
    print("Profile headline updated successfully!")

finally:
    driver.quit()
