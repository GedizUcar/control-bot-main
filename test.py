import requests
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_site():
    # Use Service object for WebDriver
    

    result = "WebSite is working well"
    screenshot_path = None

    chrome_options = Options()
    chrome_options.binary_location = "/usr/local/bin/chrome-linux64/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--window-size=1920x1080")
    
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    screenshot_path = None

    def siteControl(url):
        print("Checking site:", url)
        hata_kelimeleri = ["Hata", "Error", "Failed", "Unavailable"]

        try:
            response = requests.get(url, timeout=10)
            print("HTTP Status Code:", response.status_code)
            if response.status_code != 200:
                return False, f"HTTP Status Code: {response.status_code}"

            for kelime in hata_kelimeleri:
                if kelime in response.text:
                    print("Error word found in response")
                    return False, "Contain Error Word."

            print("Site check passed")
            return True, "WebSite is working well."
        except requests.RequestException as e:
            print("RequestException occurred:", e)
            return False, f"RequestException: {e}"

    def portControl(host, port_list):
        print("Checking ports for host:", host)
        for port in port_list:
            print("Checking port:", port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print("Port open:", port)
                return True
        print("No open ports found")
        return False

    siteSituation, siteMessage = siteControl("https://app.percogo.com")
    portSituation = portControl("app.percogo.com", [80, 443])

    if not siteSituation:
        screenshot_path = "screenshot.png"
        print("Taking screenshot...")
        driver.save_screenshot(screenshot_path)  # Take screenshot

    driver.quit()

    if screenshot_path:
        return f"WebSite is not responding or contains error Message! ({siteMessage})", screenshot_path
    return "WebSite is working well", None

if __name__ == "__main__":
    # Example usage
    result, screenshot = test_site()
    print(result)
    if screenshot:
        print("Screenshot saved at:", screenshot)
