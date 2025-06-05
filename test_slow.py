import csv, os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Setup Firefox driver with "eager" strategy - sometimes websites load a bunch of 
# garbage that isn't needed and it can make your script hang
options = FirefoxOptions()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)

LOCAL_SITE = f"file://{os.path.abspath('index.html')}" # normally this would be a full URL to a website

CSV_PATH = "credentials.csv"

# this function makes the field inputs happen slower, more like if a real person was typing
def slow_typing(element, text, delay=0.3):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def load_users_from_csv(path):
    users = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append({
                "username": row["username"],
                "password": row["password"]
            })
    return users

try:
    print("🔁 Starting CSV-based Demo (Slow)...\n")
    test_users = load_users_from_csv(CSV_PATH)

    for user in test_users:
        driver.get(LOCAL_SITE)
        time.sleep(1)

        slow_typing(driver.find_element(By.ID, "username"), user["username"])
        time.sleep(0.5) # more built in waits just to slow it down for demo purposes
        slow_typing(driver.find_element(By.ID, "password"), user["password"])
        time.sleep(0.5)
        driver.find_element(By.TAG_NAME, "form").submit()

        time.sleep(2)

        if "Multi-Factor Authentication" in driver.page_source:
            print(f"✅ {user['username']} password correct but has MFA")
        elif "Welcome" in driver.page_source:
            print(f"✅ {user['username']} logged in successfully (password only)")
        else:
            print(f"❌ {user['username']} login failed")

        time.sleep(2)

finally:
    driver.quit()

    print("\n Test complete!")
