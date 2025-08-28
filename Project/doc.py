# All parts are divided

#----------------------------------------------------------------
#---------- EXECUTE OCR ----------
#----------------------------------------------------------------

from modules import image_ocr

def execute_ocr(img):
    text_detected = image_ocr.apply_ocr(img)
    # print(text_detected) # Check complete text detected
    return text_detected

#----------------------------------------------------------------
#---------- SEARCH FOR THE REQUIRED DATA (REGEX) ----------
#----------------------------------------------------------------

from modules import text_regex

def search_data(text):
    # Search order number
    order_number = text_regex.search_order_number(text)

    # Search the data rows
    data_rows = text_regex.search_data_rows(text)
    
    return {'order_number': order_number, 'data_rows': data_rows}

#----------------------------------------------------------------
#---------- CLEAN THE DATA FOUND (REGEX) ----------
#----------------------------------------------------------------

def clean_data(data):
    data_cleaned = text_regex.clean_lines(data)
    return data_cleaned

#----------------------------------------------------------------
#---------- EXTRACT THE DATA (REGEX) ----------
#----------------------------------------------------------------

def extract_data(data):
    data_matched = text_regex.match_data(data)
    return data_matched

#----------------------------------------------------------------
#---------- GET CENTERS INFO ----------
#----------------------------------------------------------------

from modules import centers_info

def get_centers_info(data):
    center_mode = centers_info.get_center_mode(data)
    places = centers_info.get_places()
    return {'center_mode': center_mode, 'places': places}

#----------------------------------------------------------------
#---------- PREPARE THE DATA ----------
#----------------------------------------------------------------

from modules import prepare_data

def prepare_the_data(data):
    data_prepared = prepare_data.format_data(data)
    return data_prepared

#----------------------------------------------------------------
#---------- VERIFY THE DATA (OPTIONAL) ----------
#----------------------------------------------------------------

from modules import ocr_verification

def verify_data(data, order_number, img_id):

    final_ocr = {
        'order_number': order_number,
        'rows': data
    }
    is_correct = ocr_verification.evaluate_ocr(final_ocr, img_id)
    return is_correct

#----------------------------------------------------------------
#---------- APPLY ALL IN A IMAGE ----------
#----------------------------------------------------------------

def process_image_script(img, img_id):
    text_detected = execute_ocr(img)
    data_searched = search_data(text_detected)
    order_number, data_rows = data_searched['order_number'], data_searched['data_rows']
    # print("\n"*1)

    data_cleaned = clean_data(data_rows)
    # for line in data_cleaned:
    #     print(f'Linea limpiada: {line}')

    data_matched = extract_data(data_cleaned)

    centers_info = get_centers_info(data_matched)
    center_mode, places = centers_info['center_mode'], centers_info[ 'places']

    data_prepared = prepare_the_data(data_matched)
    # prepare_data.show_data(data_prepared, order_number, center_mode, places)

    # Optional
    print(f'Usando Imagen: {img_id}')
    is_correct = verify_data(data_prepared, order_number, img_id)
    return is_correct

#----------------------------------------------------------------
#---------- SET UP THE IMAGE ----------
#----------------------------------------------------------------

import cv2
import os
from modules import set_up_images

def run_multiple():
    IMAGES_PROCESS = set_up_images.getImages()

    # Put here the images to use
    # IMAGES_PROCESS = ['img004.jpg', 'img005.jpg', 'img006.jpg', 'img007.jpg', 'img008.jpg', 'img009.jpg', 'img010.jpg']
    IMAGES_PROCESS = ['img009.jpg', 'img007.jpg']
    is_testing = False

    # Find the images and apply the process
    correct = []

    base_route = os.path.dirname(__file__)
    for image in IMAGES_PROCESS:
        image_route = os.path.join(base_route, "imgs", image)
        img_id = image_route.rsplit("\\")[-1].removesuffix('.jpg')

        img = cv2.imread(image_route)
        if img is None:
            print(f'❌ Image: {img_id} could not be loaded.')
            continue

        is_correct = process_image_script(img, img_id)

        if is_correct:
            correct.append('✅')
        else:
            correct.append('❌')
    
    if not is_testing:
        return
    for i, element in enumerate(IMAGES_PROCESS):
        print(f' {element}: {correct[i]}')

run_multiple()