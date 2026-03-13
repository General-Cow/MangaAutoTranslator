import os
from PIL import Image
from manga_ocr import MangaOcr


def ocr_extractor(img="", file_dir=""):
    """
    Extract Japanese Text using MangaOCR.
    
    Args:
        img (str): Path to the image file if only looking at one image.
        file_dir (str): Path to directory containing images to translate.
        multi_file (bool): If True, process all images in the directory.

    Returns:
        list: List of extracted Japanese text
    """
    
    if not img.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")):
        raise ValueError(f"Invalid image file: {img}. Supported formats: .png, .jpg, .jpeg, .bmp, .gif, .webp")

    mocr = MangaOcr()
    jp_text = mocr(os.path.join(file_dir, img))

    return jp_text
    

def ocr_extractor_crop(img="", file_dir="", crop_coords=(0, 0, 0, 0)):
    """
    Extract Japanese Text using MangaOCR with cropping.
    
    Args:
        img (str): Path to the image file.
        file_dir (str): Path to directory containing the image.
        crop_coords (tuple): Coordinates for cropping in the format (x, y, width, height).

    Returns:
        list: List of extracted Japanese text
    """

    if not img.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")):
        raise ValueError(f"Invalid image file: {img}. Supported formats: .png, .jpg, .jpeg, .bmp, .gif, .webp")
    
    mocr = MangaOcr()
    x, y, w, h = crop_coords
    box = (x, y, x + w, y + h)
    region = Image.open(os.path.join(file_dir, img)).crop(box)
    jp_text = mocr(region)

    return jp_text