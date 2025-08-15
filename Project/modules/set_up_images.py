#----------------------------------------------------------------
#---------- SET UP THE IMAGES ----------
#----------------------------------------------------------------

import glob
import os

def getImages():    
    # Search for all .jpg files in current directory
    images = glob.glob(os.path.join(os.getcwd(), "*.jpg"))

    if not images:
        raise FileNotFoundError("Images with extention .jpg not found in the directory.")
    
    return images