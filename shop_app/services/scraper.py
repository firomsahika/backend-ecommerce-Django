from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Set up Chrome service and options
service = Service(executable_path="chromedriver.exe")
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")

def scrape_product_data(url):
    products = []
    driver = None  # Initialize driver to None

    try:
        # Initialize Chrome driver with options
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(5)  # Adjust the wait time as needed

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
        print(f"Error initializing WebDriver: {e}")
    finally:
        # Only attempt to quit the driver if it was successfully initialized
        if driver:
            driver.quit()

    return products
