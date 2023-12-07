from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import time 
import threading
from queue import Queue
import asyncio
def start_chrome_with_permissions():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/local/bin/chrome-linux64/chrome" 
    
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    service = Service('/usr/local/bin/chromedriver')  
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def selenium_task(q,function,*args,**kwargs):
    result =function(*args,**kwargs)
    q.put(result)

def selenium_test_demo_button():
    result = "Demo , mic and camera buttons are works well"
    screenshot_path = None

    driver = start_chrome_with_permissions()

    try:
        driver.get("https://app.percogo.com")
        
       
        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#c-p-bn')))
            cookie_button.click()
        except Exception as e:
            
            pass
        
    except Exception as e:
        driver.quit()
        return f"Page can't load correctly, Error!!!", None

    wait = WebDriverWait(driver, 10)

   
    try:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.b-purple')))
        button.click()
    except Exception as e:
        screenshot_path = "first_button_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        result = f"Cannot click First Button Error!!!"
        return result, screenshot_path

    
    try:
        new_window_handle = [handle for handle in driver.window_handles if handle != driver.current_window_handle][0]
        driver.switch_to.window(new_window_handle)
    except Exception as e:
        screenshot_path = "switch_window_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        result = f"Cannot switch to the new window Error!!!"
        return result, screenshot_path

   
    try:
        mic_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="mic icon"]')))
        mic_button.click()
        camera_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="camera icon"]')))
        camera_button.click()
    except Exception as e:
        screenshot_path = "mic_camera_button_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        result = f"Cannot click Mic or Camera Button Error!!!"
        return result, screenshot_path

    
    try:
        join_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.perculus-button-container')))
        join_button.click()

        
        try:
            skip_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.introjs-skipbutton')))
            skip_button.click()

           
            try:
                 print("Waiting for the break button to be visible...")
                 break_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.btn-break')))
                 print("Break button is visible.")
            except Exception as e:
                screenshot_path = "leave_button_screenshot.png"
                driver.save_screenshot(screenshot_path)
                driver.quit()
                result = f"Leave button not found Error!!!"
                return result, screenshot_path

        except Exception as e:
            screenshot_path = "skip_button_screenshot.png"
            driver.save_screenshot(screenshot_path)
            driver.quit()
            result = f"Cannot click Skip Button Error!!!"
            return result, screenshot_path

    except Exception as e:
        screenshot_path = "final_button_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        result = f"Cannot click Final Button Error!!!"
        return result, screenshot_path


    driver.quit()
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

    
    t = threading.Thread(target=selenium_task, args=(q, selenium_test_demo_button))
    t.start()
    t.join()

    
    result = q.get()
    if isinstance(result, Exception):
        print("An error occurred:", result)
    else:
        print("Result from test_demo_button:", result)
    return result


if __name__ == "__main__":
    asyncio.run(test_demo_button())





