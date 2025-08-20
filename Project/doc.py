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

data_cleaned = text_regex.clean_lines(data_rows)

#----------------------------------------------------------------
#---------- EXTRACT THE DATA (REGEX) ----------
#----------------------------------------------------------------

data_matched = text_regex.match_data(data_cleaned)

#----------------------------------------------------------------
#---------- PREPARE THE DATA ----------
#----------------------------------------------------------------

from modules import centers_info

center_mode = centers_info.get_center_mode(data_matched)
places = centers_info.get_places()

print("\n\n\n\n")

for i, line in enumerate(data_matched):
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

print(f'Usando imagen: {image_route}')