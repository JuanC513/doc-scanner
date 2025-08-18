#----------------------------------------------------------------
#---------- APPLY OCR ----------
#----------------------------------------------------------------

from . import set_up_tesseract
from . import image_preprocessing

def apply_ocr(image):
    # Preproccess the image
    preprocessed_image = image_preprocessing.apply_preproccesing(image)

    custom_config = r'--oem 3 --psm 6' # Tesseract use Spanish
    ocr_result = set_up_tesseract.pytesseract.image_to_string(preprocessed_image, config=custom_config)

    return (ocr_result)