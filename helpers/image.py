def map_geocoord_to_pixel(geo_coord: tuple, img_size: tuple, bbox: tuple) -> tuple:
    """Map geographic coordinates (latitude, longitude) to pixel coordinates in an image.
    
    This function converts geographic coordinates to pixel coordinates based on the image
    dimensions and the geographic bounding box of the image. The y-axis is reversed since
    latitude increases upwards while pixel coordinates increase downwards.
    
    Args:
        geo_coord (tuple): A tuple of (longitude, latitude) coordinates to convert
        img_size (tuple): A tuple of (width, height) in pixels of the target image
        bbox (tuple): A tuple of (min_lon, min_lat, max_lon, max_lat) defining the
                     geographic bounding box of the image
    
    Returns:
        tuple: A tuple of (x, y) pixel coordinates as integers
    """
    lon, lat = geo_coord
    min_lon, min_lat, max_lon, max_lat = bbox

    x = (lon - min_lon) / (max_lon - min_lon) * img_size[0]
    y = (max_lat - lat) / (max_lat - min_lat) * \
        img_size[1]  # Reverse y axis (lat increases upwards)

    return (int(x), int(y))