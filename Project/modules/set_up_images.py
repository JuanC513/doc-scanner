#----------------------------------------------------------------
#---------- SET UP THE IMAGES ----------
#----------------------------------------------------------------

import glob
import os

def getImages():    
    # Route to the "imgs" directory
    img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "imgs")

    # Search for all .jpg files in the directory
    images = glob.glob(os.path.join(img_dir, "*.jpg"))

    if not images:
        raise FileNotFoundError("Images with extention .jpg not found in the directory.")
    
    return images