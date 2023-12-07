from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import threading
from queue import Queue
import asyncio

def start_chrome_with_options():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/local/bin/chrome-linux64/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def selenium_task(q, function, *args, **kwargs):
    try:
        result = function(*args, **kwargs)
        q.put(result)
    except Exception as e:
        q.put(e)

def selenium_test_email():
    print("Starting selenium_test_email function...")
    driver = start_chrome_with_options()
    result = "Email button works well"
    screenshot_path = None

    try:
        driver.get("https://app.percogo.com")
        print("Website loaded successfully.")
    except Exception as e:
        print("Could not load website:", e)
        driver.quit()
        return "Page can't load correctly, Error!!!", None

    wait = WebDriverWait(driver, 10)

    try:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.b-blue')))
        button.click()
        print("First button clicked successfully.")
    except Exception as e:
        screenshot_path = "first_button_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print("Could not click the first button:", e)
        driver.quit()
        result = "Cannot click First Button Error!!!"
        return result, screenshot_path

    driver.quit()
    print("selenium_test_email function completed.")
    return result, None

async def test_email():
    print("test_email coroutine called")
    q = Queue()
    t = threading.Thread(target=selenium_task, args=(q, selenium_test_email))
    t.start()
    t.join()
    result = q.get()
    if isinstance(result, Exception):
        print("An error occurred:", result)
    else:
        print("Result from selenium_test_email:", result)
    return result

# Example usage
if __name__ == "__main__":
    asyncio.run(test_email())
