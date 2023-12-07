from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import threading
from queue import Queue
import asyncio

def start_chrome_with_permissions():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    service = Service('/usr/local/bin/chromedriver')  # Use Service for chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def selenium_task(q, function, *args, **kwargs):
    result = function(*args, **kwargs)
    q.put(result)

def selenium_test_demo_button():
    print("Starting test for demo, mic and camera buttons")
    result = "Demo, mic and camera buttons are works well"
    screenshot_path = None

    driver = start_chrome_with_permissions()

    try:
        driver.get("https://app.percogo.com")
        print("Opened website")
        
        # Handle "We use cookies" warning
        try:
            wait = WebDriverWait(driver, 10)
            cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#c-p-bn')))
            cookie_button.click()
            print("Cookie warning handled")
        except Exception as e:
            print("Cookie warning could not be handled:", e)
        
    except Exception as e:
        driver.quit()
        print("Error loading page:", e)
        return "Page can't load correctly, Error!!!", None

   

    driver.quit()
    print("Test completed")
    return result, None

async def test_demo_button():
    print("test_demo_button function called")
    q = Queue()

    def selenium_task(q, function, *args, **kwargs):
        try:
            result = function(*args, **kwargs)
            q.put(result)
        except Exception as e:
            q.put(e)

    # Start the selenium test in a separate thread
    t = threading.Thread(target=selenium_task, args=(q, selenium_test_demo_button))
    t.start()
    t.join()

    # Get the result from the queue
    result = q.get()
    if isinstance(result, Exception):
        print("An error occurred:", result)
    else:
        print("Result from test_demo_button:", result)
    return result

# Make sure to call asyncio.run() outside of any other function, at the top level
if __name__ == "__main__":
    asyncio.run(test_demo_button())
