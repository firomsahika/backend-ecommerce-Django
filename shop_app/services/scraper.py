import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path="chromedriver.exe")

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

def scrape_product_data(url):
    products = []
    # driver = None  

    try:
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        product_elements = driver.find_elements(By.ID, 'product-item')
        print(f"Found {len(product_elements)} product elements.")  # Debug output

        for product in product_elements:
            try:
                name = product.find_element(By.ID, 'product-name').text
                price = product.find_element(By.ID, 'product-price').text
                ram = product.find_element(By.ID, 'product-ram').text

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
