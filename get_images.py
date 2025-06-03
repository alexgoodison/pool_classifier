import requests
from PIL import Image, ImageDraw
from shapely.geometry import Polygon
import itertools
import json
import random
from helpers.image import map_geocoord_to_pixel

# ---- CONSTANTS ----
from constants import w, h, MAPBOX_API_KEY, MAPBOX_STYLE_URL
sample_size = 1000

# Collect parcels
all_parcels = []

with open('la_parcels_ogr2ogr.json', 'r') as file:
    for line in itertools.islice(file, 10000, 1500000):
        line = line.strip()[:-1]

        try:
            json_object = json.loads(line)  # type, properties, geometry
            all_parcels.append(json_object)
        except json.JSONDecodeError:
            print("Error decoding JSON line")


# Loop over random sample of parcels
selected_parcels = random.sample(all_parcels, sample_size)

for parcel in selected_parcels:
    ain = parcel.get("properties").get("AIN")

    try:
        parcel_boundary = parcel.get("geometry")
        latitude = parcel.get("properties").get("CENTER_LAT")
        longitude = parcel.get("properties").get("CENTER_LON")

        # Calculate square bbox to fit boundary
        min_lon, min_lat, max_lon, max_lat = Polygon(parcel_boundary['coordinates'][0]).bounds
        width = max_lon - min_lon
        height = max_lat - min_lat

        # Use the larger of width or height to define the side length of the square
        side_length = max(width, height)

        center_lon = (min_lon + max_lon) / 2
        center_lat = (min_lat + max_lat) / 2

        half_side = side_length / 2
        bbox = [
            center_lon - half_side,  # min_lon
            center_lat - half_side,  # min_lat
            center_lon + half_side,  # max_lon
            center_lat + half_side   # max_lat
        ]

        url = (
            MAPBOX_STYLE_URL,
            f"{bbox}/"
            f"{w}x{h}?"
            f"access_token={MAPBOX_API_KEY}"
        )
        print(url)
        response = requests.get(url)
        with open(f"assets/unsorted/satellite/{ain}.jpg", 'wb') as file:
            file.write(response.content)

        polygon_coords = parcel_boundary['coordinates'][0]
        polygon = Polygon([map_geocoord_to_pixel(coord, (w, h), bbox)
                          for coord in polygon_coords])

        # Load the 400x400 image
        image = Image.open(f"assets/unsorted/satellite/{ain}.jpg")
        mask = Image.new('L', (w, h), 0)  # Create a blank mask
        draw = ImageDraw.Draw(mask)

        # Draw the polygon onto the mask
        draw.polygon(list(polygon.exterior.coords), outline=1, fill=255)

        # Apply the mask to the image
        masked_image = Image.composite(
            image, Image.new('RGB', (w, h), (0, 0, 0)), mask)

        # Save the masked image
        masked_image.save(f'assets/unsorted/masked/{ain}.jpg')
    except:
        print(f">> Error with {ain}")
