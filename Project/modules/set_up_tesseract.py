#----------------------------------------------------------------
#---------- SET UP TESSERACT ----------
#----------------------------------------------------------------

import os
import pytesseract
import shutil

# Try to use tesseract (from PATH)

tesseract_en_path = shutil.which("tesseract")

if tesseract_en_path:
    # It is in PATH
    print(f"✅ Using Tesseract from PATH: {tesseract_en_path}")
    pytesseract.pytesseract.tesseract_cmd = tesseract_en_path
else:
    # Search it locally in the project
    local_route = os.path.join(os.getcwd(), "tesseract", "tesseract.exe")
    if os.path.exists(local_route):
        print(f"✅ Using Tesseract from local route: {local_route}")
        pytesseract.pytesseract.tesseract_cmd = local_route
    else:
        raise FileNotFoundError(
            "❌ Tesseract not found.\n"
            "Be sure it is installed and in PATH, or put tesseract.exe in './tesseract/'"
        )