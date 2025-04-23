import xml.etree.ElementTree as ET
import csv

# Load and parse the XML file
tree = ET.parse('C:\\Users\\harshil.shukla\\Desktop\\xmll\\AU.xml')  # Replace with your actual XML file path
root = tree.getroot()

# Open a CSV file to write the data
with open('outputttttttt AU.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Link', 'Sale Price'])  # Header row

    # Loop through the XML structure and extract the required tags
    for item in root.findall('.//item'):
        link = item.find('link')
        sale_price = item.find('sale_price')

        if link is not None and sale_price is not None:
            sale_price_text = sale_price.text.replace(' AUD', '')  # Remove 'USD' from sale price
            writer.writerow([link.text, sale_price_text])

print("Data has been successfully written to output.csv.")
