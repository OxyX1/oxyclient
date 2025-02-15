import json
from lxml import etree

# Load XML file
xml_file = 'dist/gui/data.xml'
xml_tree = etree.parse(xml_file)

# Create a dictionary from the XML
def xml_to_dict(element):
    result = {}
    for child in element:
        result[child.tag] = xml_to_dict(child) if len(child) > 0 else child.text
    return result

# Convert the XML data to a dictionary
data_dict = xml_to_dict(xml_tree.getroot())

# Convert the dictionary to JSON
json_data = json.dumps(data_dict, indent=4)

# Save to a JSON file
with open('server_data.json', 'w') as json_file:
    json_file.write(json_data)

print("XML has been converted to JSON!")
