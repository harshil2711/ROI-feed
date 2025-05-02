import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# === Part 1: Count base URLs and update CSV ===

csv_path = 'C:\\Users\\harshil.shukla\\Desktop\\xmll\\Combination result\\UKCOMB.csv'

# Load CSV using pandas
df = pd.read_csv(csv_path)
url_col = df.columns[0]

# Extract base URLs
df['base_url'] = df[url_col].str.split('?').str[0]
url_counts = df['base_url'].value_counts()

# Add/Update Count column
df['Count'] = ''
for base in url_counts.index:
    main_url_index = df[(df[url_col] == base)].index
    if not main_url_index.empty:
        df.at[main_url_index[0], 'Count'] = url_counts[base]

# Drop helper column
df.drop(columns=['base_url'], inplace=True)

# Save updated DataFrame back to CSV
df.to_csv(csv_path, index=False)

# === Part 2: Run Selenium scraping ===

# Load CSV data into list of rows
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = list(csv.reader(f))

# Ensure header has at least 7 columns
if len(reader[0]) < 7:
    reader[0] += [''] * (7 - len(reader[0]))

# Setup Chrome
options = Options()
options.add_argument("--headless=chrome")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-features=VizDisplayCompositor")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Set headers
reader[0][2:7] = ["Standard Dim Count", "Fabric Count", "Color Count", "Total Combination", "Result"]

# Count total rows that need processing and have no query params in URL
total_valid_rows = 0
already_processed = 0

for row in reader[1:]:
    url = row[0]
    result = row[6] if len(row) > 6 else ''

    if url and '?' not in url:
        total_valid_rows += 1
        if result not in (None, ''):
            already_processed += 1

X = already_processed
Y = total_valid_rows

for i in range(1, len(reader)):
    row = reader[i]
    if len(row) < 7:
        row += [''] * (7 - len(row))

    count_val = row[1]
    result_val = row[6]

    if count_val not in (None, '', '0') and result_val not in (None, ''):
        continue

    url = row[0]
    url_comb_value = row[1]
    if not url or not url_comb_value:
        continue

    try:
        driver.get(url)
        time.sleep(2)

        std_dim_count = 0
        fabric_count = 0
        color_count = 0

        try:
            std_dim_elements = driver.find_elements(By.XPATH, "//ul[@class='standard-dimensions']//li")
            std_dim_count = len(std_dim_elements)
            if std_dim_count == 0:
                std_dim_count = 1
        except:
            pass

        fabric_xpaths = [
            "//ul[contains(@class,'fabric-option')]//li[@data-fabric-id]",
            "//ul[@class='fabric-option ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all']//li",
        ]

        for xpath in fabric_xpaths:
            fabric_elements = driver.find_elements(By.XPATH, xpath)
            if fabric_elements:
                fabric_count = len(fabric_elements)
                break

        color_xpaths = [
            "//div[@class='all-color-section']//li",
            "//ul[@class='color-option']//li",
            "//ul[@class='color-option pattern-selection']//li"
        ]

        for xpath in color_xpaths:
            color_elements = driver.find_elements(By.XPATH, xpath)
            if color_elements:
                color_count = len(color_elements)
                break

        row[2] = std_dim_count
        row[3] = fabric_count
        row[4] = color_count

        if std_dim_count:
            total_comb = std_dim_count * color_count + 1
        else:
            total_comb = color_count + 1

        row[5] = total_comb

        try:
            if int(url_comb_value) == total_comb:
                row[6] = "PASS"
            else:
                row[6] = "FAIL"
        except:
            row[6] = "FAIL"

        print(f"✅ {url} | StdDim: {std_dim_count} | Fabrics: {fabric_count} | Colors: {color_count} | Comb: {total_comb} | Result: {row[6]}")
        X += 1
        print(f"✔️ Processed {X}/{Y} URLs")

    except Exception as e:
        print(f"❌ Failed: {url}")
        print(str(e))
        row[2:7] = ["ERROR"] * 5
        X += 1
        print(f"✔️ Processed {X}/{Y} URLs")

# Save and quit
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reader)

driver.quit()
