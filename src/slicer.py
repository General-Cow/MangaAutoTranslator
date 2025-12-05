import os
import streamlit as st
# from PIL import Image
from src.ocr_extractor import ocr_extractor
from src.translator import get_translations, get_llm_translations

def presliced_clips(page_num, manga_loc):
    for clip in os.listdir(f"{manga_loc}/clips/pg{page_num}_clips/"):
        test = ocr_extractor(img=clip, file_dir=f"{manga_loc}/clips/pg{page_num}_clips/", multi_file=False)
                        # test = ocr_extractor(img=uploaded_file.name, file_dir="./data/Junko_manga", multi_file=False)
        st.write(test[0])

        translated = get_translations(test, translation_model="Helsinki-NLP/opus-mt-ja-en", concat_sent=False)
        st.write("Translation model: ", translated[0])
                        
        llm_translated = get_llm_translations(test, llm_model='gemma3:12b')
        st.write("LLM: ", llm_translated[0])


def manual_slicing(page_path):
    pass
    
def text_region_detection(page_path):
    pass


# def slice_grid(page_path, rows=2, cols=2, output_dir=None):
#     os.makedirs(output_dir, exist_ok=True)
#     img = Image.open(page_path)
#     w, h = img.size
#     clips = []
#     base = os.path.splitext(os.path.basename(page_path))[0]
#     for r in range(rows):
#         for c in range(cols):
#             left = int(c * w / cols)
#             upper = int(r * h / rows)
#             right = int((c + 1) * w / cols)
#             lower = int((r + 1) * h / rows)
#             crop = img.crop((left, upper, right, lower))
#             name = f"{base}_r{r}_c{c}.png"
#             out_path = os.path.join(output_dir, name)
#             crop.save(out_path)
#             clips.append(out_path)
#     return clips

# def slice_by_text_regions(page_path, output_dir=None, min_conf=40, pad=8):
#     """
#     Use pytesseract to extract text bounding boxes and save cropped regions.
#     Falls back to a 2x2 grid if no regions detected.
#     """
#     try:
#         import pytesseract
#         from pytesseract import Output
#     except Exception:
#         # pytesseract not available => fallback to grid
#         return slice_grid(page_path, rows=2, cols=2, output_dir=output_dir)

#     os.makedirs(output_dir, exist_ok=True)
#     img = Image.open(page_path)
#     data = pytesseract.image_to_data(img, output_type=Output.DICT, lang='jpn+eng')
#     n = len(data.get('level', []))
#     clips = []
#     base = os.path.splitext(os.path.basename(page_path))[0]

#     for i in range(n):
#         try:
#             conf = float(data['conf'][i])
#         except Exception:
#             conf = -1
#         if conf >= min_conf:
#             left = max(0, int(data['left'][i]) - pad)
#             top = max(0, int(data['top'][i]) - pad)
#             width = int(data['width'][i]) + pad * 2
#             height = int(data['height'][i]) + pad * 2
#             right = min(img.width, left + width)
#             bottom = min(img.height, top + height)
#             crop = img.crop((left, top, right, bottom))
#             name = f"{base}_box{i}.png"
#             out_path = os.path.join(output_dir, name)
#             crop.save(out_path)
#             clips.append(out_path)

#     if not clips:
#         # fallback
#         return slice_grid(page_path, rows=2, cols=2, output_dir=output_dir)
#     return clips