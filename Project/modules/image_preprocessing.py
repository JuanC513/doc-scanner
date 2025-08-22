#----------------------------------------------------------------
#---------- PREPROCCESS THE IMAGE ----------
#----------------------------------------------------------------

import cv2
import numpy as np

# Grayscale the image
def gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Binarization (binarize/convert an image to black and withe)
def binarization(image):
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return image

# Remove noise in the image
def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

# Make the font thiner
def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

# Make the font thicker
def thick_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

# Apply the preproccesing desired
def apply_preproccesing(image):
    # Grayscale
    prep_image = gray_scale(image)
    cv2.imwrite("temp/1. inverted.jpg", prep_image)

    # Binarization
    prep_image = binarization(prep_image)
    cv2.imwrite("temp/2. bw_image.jpg", prep_image)

    # Remove noise
    prep_image = noise_removal(prep_image)
    cv2.imwrite("temp/3. no_noise.jpg", prep_image)

    # Make font thiner
    # prep_image = thin_font(prep_image)
    # cv2.imwrite("temp/4. eroded_image.jpg", prep_image)

    # Make font thicker
    # prep_image = thick_font(prep_image)
    # cv2.imwrite("temp/5. dilated.jpg", prep_image)

    return prep_image