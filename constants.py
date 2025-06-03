import os
from dotenv import load_dotenv

load_dotenv()

w, h = 400, 400
MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY")
MAPBOX_STYLE_URL = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"