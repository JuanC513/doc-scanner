import cv2


#----------------------------------------------------------------
#---------- SET UP THE IMAGE ----------
#----------------------------------------------------------------

from modules import set_up_images

images = set_up_images.getImages()

# Use the first image found
image_route = images[0]
img = cv2.imread(image_route)
if img is None:
    raise ValueError("Image could not be loaded.")

#----------------------------------------------------------------
#---------- EXECUTE OCR ----------
#----------------------------------------------------------------

from modules import image_ocr

text_detected = image_ocr.apply_ocr(img)
# print(text_detected) # Check complete text detected

#----------------------------------------------------------------
#---------- SEARCH FOR THE REQUIRED DATA (REGEX) ----------
#----------------------------------------------------------------

from modules import text_regex

# Search order number
order_number = text_regex.search_order_number(text_detected)

# Search the data rows
data_rows = text_regex.search_data_rows(text_detected)

print("\n"*4)

#----------------------------------------------------------------
#---------- CLEAN THE DATA FOUND (REGEX) ----------
#----------------------------------------------------------------

import re

# Clean the line so it is easier to extract the data
def clean_line(line):
    # 1. Remove common specific chars due to OCR noise
    line = re.sub(r'[«=+~—_]', '', line)

    # 2. Remove any non alphanumeric char except some specific
    line = re.sub(r'[^\w\s.,/]', '', line)

    # 3. Remove dots alone between spaces " . " → " "
    line = re.sub(r'\s\.\s', ' ', line)

    # 4. Remove dots at the beggining or the end of the line
    line = re.sub(r'^\.\s*|\s*\.$', '', line.strip())

    # 5. Replace multiple spaces for just one
    line = re.sub(r'\s+', ' ', line)
    print(f'Linea limpiada: {line}')
    return line


#----------------------------------------------------------------
#---------- EXTRACT THE DATA (REGEX) ----------
#----------------------------------------------------------------


def extract_data(line):
    line = clean_line(line)

    # Search the fields using regular expressions
    pattern = re.compile(
        r'(?P<center>\d+)\s+'                       # CeCo
        # r'(?P<line>\d{1,3}/\d)\s+'                # Pos / Line
        r'(?P<line>.*?)\s+'
        r'(?P<material>\d{5,})\s+'                  # Material / Service
        r'(?P<deno>.*?)\s+'                         # Deno (free text before solped)
        r'(?P<solped>\d{6,10})\s+'                  # Solped
        # r'(?P<date>\d{2}.\d{2}.\d{4})\s+'          # Delivery date
        r'(?P<date>\d{2}\.\d{2}\.\d{1,4})\.?\s+'
        r'(?P<UN>.*?)\s+'
        r'(?P<quantity>.*?)\s+'
        r'(?P<unit_value>.*?)\s+'
        r'(?P<vat>\d+[.,]?\d*)\s+'
        r'(?P<subtotal>\d+[.,]?\d*)'
    )

    match = pattern.search(line)
    if match:
        return match.groupdict()
    else:
        print("NOT MATCHED: ", line)
        return None

matched_lines = []
for line in data_rows:
    if line.strip() == "":
        continue
    data = extract_data(line)
    if data:
        matched_lines.append(data)
        print(data)
    else:
        print("Could not be parsed:", line, "\n")


#----------------------------------------------------------------
#---------- PREPARE THE DATA ----------
#----------------------------------------------------------------


from collections import Counter

center_mode = Counter(line['center'] for line in matched_lines).most_common(1)[0][0]

print("\n\n\n\n")

import os
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

# Get data from .env file
PLACE_2282_KEY = os.getenv("PLACE_2282_KEY")
PLACE_2288_KEY = os.getenv("PLACE_2288_KEY")
PLACE_2260_KEY = os.getenv("PLACE_2260_KEY")

places = {
    '2282': PLACE_2282_KEY,
    '2288':	PLACE_2288_KEY,
    '2260':	PLACE_2260_KEY
}

for i, line in enumerate(matched_lines):
    required_fields = ['pedido', 'posicion', 'solped', 'material', 'cantidad', 'subtotal', 'centro', 'denom']
    required_data = ""
    for field in required_fields:
        new_field = ""
        if field == 'pedido':
            new_field = order_number
        elif field == 'posicion':
            new_field = (i+1)*10
        elif field == 'cantidad':
            new_field = 2
        elif field == 'centro':
            new_field = center_mode
        elif field == 'denom':
            new_field = places[center_mode] if center_mode in places else ""
        else:
            new_field = f'{line[field].replace('.','')} '
        
        required_data += f'{new_field} '
    normalized_data = ' '.join(required_data.split())
    print(normalized_data)