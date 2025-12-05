import os
from manga_ocr import MangaOcr


def ocr_extractor(img="", file_dir="", multi_file=False):
    """
    Extract Japanese Text using MangaOCR.
    
    Args:
        img (str): Path to the image file if only looking at one image.
        file_dir (str): Path to directory containing images to translate.
        multi_file (bool): If True, process all images in the directory.

    Returns:
        list: List of extracted Japanese text
    """

    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
    if multi_file:
        files = [
            f for f in os.listdir(file_dir)
            if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(file_dir, f))
        ]
    else:
        files = [img]
    
    mocr = MangaOcr()
    jp_text_list = [mocr(os.path.join(file_dir, file)) for file in files]

    return jp_text_list