#----------------------------------------------------------------
#---------- PREPROCCESS THE IMAGE ----------
#----------------------------------------------------------------

import cv2

def gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_preproccesing(image):
    prep_image = gray_scale(image)
    # cv2.imwrite("temp/1. inverted.jpg", prep_image)

    return prep_image