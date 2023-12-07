from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import asyncio

def start_chrome_with_options():
    chrome_options = Options()
    # Add any Chrome options you need here
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def test_login_button():
    print("Starting test_login_button function...")
    result = "Login button works well"
    screenshot_path = None

    driver = start_chrome_with_options()

    try:
        driver.get("https://app.percogo.com")
        print("Page loaded successfully.")
    except Exception as e:
        driver.quit()
        print(f"Error loading page: {e}")
        return "Page can't load correctly, Error!!!", None

    wait = WebDriverWait(driver, 5)

    try:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-event="nav-topmenu-login"]')))
        print("Login button found and clickable.")
        button.click()
    except Exception as e:
        screenshot_path = "login_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        print(f"Error clicking Login Button: {e}")
        result = "Cannot click Login Button Error!!!"
        return result, screenshot_path

    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.create-your-hub-description')))
        print("Login successful, correct page loaded.")
    except Exception as e:
        screenshot_path = "login_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        print(f"Login Button is working but wrong page is opening: {e}")
        result = "Login Button is working but wrong page is opening"
        return result, screenshot_path

    driver.quit()
    print(result)
    return result, None

# If you want to make it an async function, you can do the following
async def async_test_login_button():
    return test_login_button()

# Example usage
if __name__ == "__main__":
    test_result, screenshot = asyncio.run(async_test_login_button())
    print(f"Test Result: {test_result}, Screenshot: {screenshot if screenshot else 'No Screenshot'}")
