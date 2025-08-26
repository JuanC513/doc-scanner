#----------------------------------------------------------------
#---------- SET UP THE IMAGE ----------
#----------------------------------------------------------------

import cv2
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

print("\n"*3)

#----------------------------------------------------------------
#---------- GET CENTERS INFO ----------
#----------------------------------------------------------------

from modules import centers_info

center_mode = centers_info.get_center_mode(data_matched)
places = centers_info.get_places()

#----------------------------------------------------------------
#---------- PREPARE THE DATA ----------
#----------------------------------------------------------------

from modules import prepare_data

data_prepared = prepare_data.format_data(data_matched)
prepare_data.show_data(data_prepared, order_number, center_mode, places)

#----------------------------------------------------------------
#---------- VERIFY THE DATA (OPTIONAL) ----------
#----------------------------------------------------------------

img_id = image_route.rsplit("\\")[-1].removesuffix('.jpg')
print(f'Usando imagen: {img_id}')

from modules import ocr_verification
final_ocr = {
    'order_number': order_number,
    'rows': data_matched
}
ocr_verification.evaluate_ocr(final_ocr, img_id)