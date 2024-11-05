from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


service = Service(executable_path="chromedriver.exe")



def scrape_product_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")
    

    products = []
    try:
        driver = webdriver.Chrome(service=service) 
        driver.get(url)
        time.sleep(3) 
        product_elements = driver.find_elements(By.ID, 'product-item')
        for product in product_elements:
            name = driver.find_element(By.ID, f'product-name-{product.id}').text
            price = driver.find_element(By.ID, f'product-price-{product.id}').text
            ram = driver.find_element(By.ID, f'product-ram-{product.id}').text

            products.append({
                'name': name,
                'price': price,
                'ram': ram,
            })
    finally:
        driver.quit()
    
    return products

