from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_google_button():
    print("Starting the Google button test...")
    result = "Google button works well"
    screenshot_path = None

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://app.percogo.com")
        print("Website loaded successfully.")

        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.b-blue')))
        button.click()
        print("First button clicked.")

        google_register = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="google"]')))
        print("Google register button is clickable.")
    except Exception as e:
        screenshot_path = "error_screenshot.png"
        driver.save_screenshot(screenshot_path)
        result = f"An error occurred during the test: {e}"
    finally:
        driver.quit()

    return result, screenshot_path


if __name__ == "__main__":
    test_result, screenshot = test_google_button()
    print(f"Test Result: {test_result}")
    if screenshot:
        print(f"Screenshot saved: {screenshot}")
