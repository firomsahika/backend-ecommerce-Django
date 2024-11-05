import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Use the os module to get the current directory and construct the path to chromedriver.exe
current_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')

# Initialize the ChromeDriver service
service = Service(executable_path=chromedriver_path)

def scrape_product_data(url):
    products = []
    driver = None  # Initialize driver to None

    try:
    
        # chrome_options = Options()
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")

      
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
        return {"error": str(e)}  # Return error information

    finally:
        # Ensure driver.quit() is only called if driver was successfully initialized
        if driver is not None:  # Only try to quit if driver is not None
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing WebDriver: {e}")

    return products  # Return the list of products
