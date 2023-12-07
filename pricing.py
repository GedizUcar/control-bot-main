from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_pricing_button():
    print("Starting test for the pricing button.")
    result = "Pricing button works well"
    screenshot_path = None

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://app.percogo.com")
        print("Website loaded successfully.")
    except Exception as e:
        driver.quit()
        print(f"Error loading page: {e}")
        return "Page can't load correctly, Error!!!", None

    wait = WebDriverWait(driver, 5)

    try:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-event="nav-topmenu-pricing"]')))
        button.click()
        print("Pricing button clicked.")
    except Exception as e:
        screenshot_path = "pricing_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        print(f"Error clicking Pricing Button: {e}")
        result = "Cannot click Pricing Button Error!!!"
        return result, screenshot_path

    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label.form-switch')))
        print("Pricing page loaded successfully.")
    except Exception as e:
        screenshot_path = "signup_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        print(f"Pricing Button is working but wrong page is opening: {e}")
        result = "Pricing Button is working but wrong page is opening"
        return result, screenshot_path

    driver.quit()
    return result, None

if __name__ == "__main__":
    test_result, screenshot = test_pricing_button()
    print(f"Test Result: {test_result}")
    if screenshot:
        print(f"Screenshot saved: {screenshot}")
