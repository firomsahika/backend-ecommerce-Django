from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_product_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required in some environments
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get(url)
    time.sleep(2) 

    products = []
    try:
        product_elements = driver.find_elements(By.ID, 'product-item')
        for product in product_elements:
            name = driver.find_element(By.ID, f'product-name-{product.id}').text
            price = driver.find_element(By.ID, f'product-price-{product.id}').text
            ram = driver.find_element(By.ID, f'product-ram-{product.id}').textt

            products.append({
                'name': name,
                'price': price,
                'ram': ram,
            })
    finally:
        driver.quit()
    
    return products

