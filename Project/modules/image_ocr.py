#----------------------------------------------------------------
#---------- APPLY OCR ----------
#----------------------------------------------------------------

from set_up_tesseract import pytesseract
from image_preprocessing import apply_preproccesing

def apply_ocr(image):
    # Preproccess the image
    preprocessed_image = apply_preproccesing(image)

    custom_config = r'--oem 3 --psm 6' # Tesseract use Spanish
    ocr_result = pytesseract.image_to_string(preprocessed_image, config=custom_config)

    return (ocr_result)