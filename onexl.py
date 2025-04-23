import xml.etree.ElementTree as ET
from openpyxl import Workbook

# Load and parse the XML file
tree = ET.parse('C:\\Users\\harshil.shukla\\Desktop\\xmll\\usa.xml')  # Replace with your actual XML file path
root = tree.getroot()

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "US Data"

# Write header row
ws.append(['Link', 'Sale Price'])

# Loop through the XML structure and extract the required tags
for item in root.findall('.//item'):
    link = item.find('link')
    sale_price = item.find('sale_price')

    if link is not None and sale_price is not None:
        sale_price_text = sale_price.text.replace(' USD', '')  # Remove 'AUD'
        # ws.append([link.text, sale_price_text])
        ws.append([link.text,float(sale_price_text.replace(',', ''))])

# Save the Excel file
output_path = 'C:\\Users\\harshil.shukla\\Desktop\\xmll\\output_US.xlsx'
wb.save(output_path)

print("Data has been successfully written to Excel:", output_path)
