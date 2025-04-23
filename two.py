import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to extract price from a PDP
def extract_price(url):
    driver.get(url)
    time.sleep(10)
    try:
        # Wait for the price element to be present
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='product-info-price']//span[2]"))  # Update the XPATH selector
        )
        price_text = price_element.text
        price = re.sub(r'[^\d.]', '', price_text)  # Remove non-numeric characters
    except Exception as e:
        price = 'N/A'
    return price

# Read URLs from CSV and extract prices
with open('URLS US.csv', mode='r') as infile:
    reader = csv.reader(infile)
    headers = next(reader)
    rows = [row for row in reader]

prices = [extract_price(row[0]) for row in rows]

# Write prices and comparison results to the same CSV file
with open('URLS US.csv', mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers + ['PDP Price', 'Result'])
    for row, price in zip(rows, prices):
        result = 'Pass' if row[1] == price else 'Fail'
        writer.writerow(row + [price, result])

# Close the WebDriver
driver.quit()
    