from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(current_dir, "chromedriver.exe")
service = Service(executable_path=chromedriver_path)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def scrape_product_data(url):
    products = []
    driver = None  # Ensure driver is initialized to None

    try:
        # Attempt to initialize the driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Find product elements
        product_elements = driver.find_elements(By.ID, 'product-item')
        for product in product_elements:
            try:
                name = product.find_element(By.ID, f'product-name-{product.id}').text
                price = product.find_element(By.ID, f'product-price-{product.id}').text
                ram = product.find_element(By.ID, f'product-ram-{product.id}').text

                products.append({
                    'name': name,
                    'price': price,
                    'ram': ram,
                })
            except Exception as e:
                print(f"Error accessing product details: {e}")

    except Exception as e:
        print(f"Error initializing WebDriver or accessing URL: {e}")

    finally:
        # Ensure driver.quit() is only called if driver was successfully initialized
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing WebDriver: {e}")

    return products
