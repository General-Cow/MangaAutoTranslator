import os
from PIL import Image
from manga_ocr import MangaOcr

def ocr_extractor(image_obj):
    """
    Extract Japanese Text using MangaOCR.
    
    Args:
        image_obj (PIL.Image): PIL Image object to extract text from.

    Returns:
        str: Extracted Japanese text
    """
    
    if not isinstance(image_obj, Image.Image):
        raise ValueError(f"Expected PIL Image object, got {type(image_obj)}")

    mocr = MangaOcr()
    jp_text = mocr(image_obj)

    return jp_text
    

def ocr_extractor_crop(image_obj, crop_coords=(0, 0, 0, 0)):
    """
    Extract Japanese Text using MangaOCR with cropping.
    
    Args:
        image_obj (PIL.Image): PIL Image object to extract text from.
        crop_coords (tuple): Coordinates for cropping in the format (x, y, width, height).

    Returns:
        str: Extracted Japanese text
    """

    if not isinstance(image_obj, Image.Image):
        raise ValueError(f"Expected PIL Image object, got {type(image_obj)}")
    
    x, y, w, h = crop_coords
    box = (x, y, x + w, y + h)
    region = image_obj.crop(box)

    mocr = MangaOcr()
    jp_text = mocr(region)

    return jp_text


def text_region_detection(image_obj):
    """
    Detect text regions in a PIL Image object.
    
    Args:
        image_obj (PIL.Image): PIL Image object to detect text regions from.
    """
    if not isinstance(image_obj, Image.Image):
        raise ValueError(f"Expected PIL Image object, got {type(image_obj)}")
    pass