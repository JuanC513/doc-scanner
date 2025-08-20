#----------------------------------------------------------------
#---------- CENTERS INFO ----------
#----------------------------------------------------------------

import os
from dotenv import load_dotenv
from collections import Counter

# Get the mode for the center atribute in data
def get_center_mode(data):
    return Counter(line['center'] for line in data).most_common(1)[0][0]

def get_places():
    # Load env variables from .env
    load_dotenv()

    # Get data from .env file
    PLACE_2282_KEY = os.getenv("PLACE_2282_KEY")
    PLACE_2288_KEY = os.getenv("PLACE_2288_KEY")
    PLACE_2260_KEY = os.getenv("PLACE_2260_KEY")

    return {
        '2282': PLACE_2282_KEY,
        '2288':	PLACE_2288_KEY,
        '2260':	PLACE_2260_KEY
    }