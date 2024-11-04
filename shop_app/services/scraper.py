from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_product_data(url):
    driver = webdriver.Chrome() 
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

