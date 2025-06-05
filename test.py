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
    print("🔁 Starting Demo...\n")
    test_users = load_users_from_csv(CSV_PATH)

    for user in test_users:
        driver.get(LOCAL_SITE)
        time.sleep(1)

        # lots of ways to do select and interact with elements, including name, id, class, query selector...
        driver.find_element(By.ID, "username").send_keys(user["username"])
        driver.find_element(By.ID, "password").send_keys(user["password"])
        driver.find_element(By.TAG_NAME, "form").submit()

        # wait for page to potentially change. other, better ways to do this such as waiting for 
        # elements to appear or even become interactable. here we are just checking for text to appear on
        # the page and pass/fail using that
        time.sleep(1)
        if "Multi-Factor Authentication" in driver.page_source:
            print(f"✅ {user['username']} password correct but has MFA")
        elif "Welcome" in driver.page_source:
            print(f"✅ {user['username']} logged in successfully (password only)")
        else:
            print(f"❌ {user['username']} login failed")

finally:
    driver.quit()

    print("\n Test complete!")
    # instead of printing to terminal could instead write results to a new csv or something even more fancy. 
