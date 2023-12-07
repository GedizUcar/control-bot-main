from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException
from  selenium.common.exceptions import TimeoutException
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def test_button(wait, data_event, expected_element):
    try:
        
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-event='{data_event}']")))
        button.click()
        time.sleep(2)
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, expected_element)))
        return True, "", None
    except NoSuchElementException as e:
        screenshot_path = f"{data_event}_screenshot.png"
        wait._driver.save_screenshot(screenshot_path)
        return False, f"'{data_event}' button is working but wrong page is opening.", screenshot_path
    except ElementNotInteractableException as e:
        screenshot_path = f"{data_event}_screenshot.png"
        wait._driver.save_screenshot(screenshot_path)
        return False, f"Unsuccessful while clicking '{data_event}' button.", screenshot_path
    except Exception as e:
        screenshot_path = f"{data_event}_screenshot.png"
        wait._driver.save_screenshot(screenshot_path)
        return False, f"An error occurred while testing '{data_event}' button.", screenshot_path

def test_buttons():
    errors = []
    screenshot_paths = []
    driver = webdriver.Chrome()
    driver.get('https://app.percogo.com')
    wait = WebDriverWait(driver, 20)

    try:
        success1, message1, screenshot_path1 = test_button(wait, 'nav-topmenu-pricing1', 'label.form-switch')
        if not success1:
            errors.append(message1)
            if screenshot_path1:
                screenshot_paths.append(screenshot_path1)

        success2, message2, screenshot_path2 = test_button(wait, 'nav-topmenu-login', 'div.create-your-hub-description1')
        if not success2:
            errors.append(message2)
            if screenshot_path2:
                screenshot_paths.append(screenshot_path2)
    finally:
        driver.quit()

    if errors:
        return "\n".join(errors), screenshot_paths
    else:
        return "Login and Pricing Buttons are working", None
