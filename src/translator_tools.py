from transformers import pipeline
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI
import streamlit as st
import json
import os
from PIL import Image
from io import BytesIO
from src.ocr_extractor import ocr_extractor, ocr_extractor_crop, text_region_detection


def get_translations(jp_text, translation_model="Helsinki-NLP/opus-mt-ja-en"):
    """
    Translate extracted text to English using translation model.
    
    Args:
        jp_text (str): Extracted Japanese text
        translation_model (str): Translation model to use.
        
    Returns:
        str: Translated English text
    """

    translate_pipe = pipeline("translation", model=translation_model, src_lang="ja", tgt_lang="en")  #src_lang="jpn_Latn", tgt_lang="eng_Latn") # added src_lang and tgt_lang for NLLB models

    translated_text = translate_pipe(jp_text)[0]["translation_text"]
    
    return translated_text


def get_llm_translations(jp_text, llm_model='gemma3:4b'):
    """
    Translate extracted text to English using an LLM.
    
    Args:
        jp_text (str): Extracted Japanese text
        llm_model (str): LLM model to use for translation.
        
    Returns:
        str: Translated English text
    """
       
    response: ChatResponse = chat(model=llm_model, messages=[
        {
            'role': 'system',
            'content': (
                'Translate the following Japanese text to English. '
                'Return ONLY the translated English text. '
                'Do not add notes, explanations, or formatting.'
                        ),
        },
        {
            'role': 'user',
            'content': jp_text,
        },
    ])

    translated_text = response.message.content

    return translated_text


def get_api_translations(jp_text, api_key): # Add parameters as needed for different APIs
    """
    Translate extracted text to English using OpenAI API.
    
    Args:
        jp_text (str): Extracted Japanese text
        api_key (str): The API key for accessing the OpenAI API
        
    Returns:
        str: Translated English text
    """


    client = OpenAI(api_key=api_key)

    response = client.responses.create(
            model="gpt-5",
            reasoning={"effort": "low"},
            instructions="Translate the following Japanese text to English. Return ONLY the translated English text. Do not add notes, explanations, or formatting.",
            input=jp_text,
        )

    translated_text = response.output_text

    return translated_text


def load_images_from_uploader(uploaded_files):
    """
    Load images from Streamlit file_uploader as PIL Image objects.
    
    Args:
        uploaded_files (list): List of UploadedFile objects from st.file_uploader.
        
    Returns:
        dict: Dictionary mapping page keys (e.g., "pg1", "pg2") to PIL Image objects.
    """
    images_dict = {}
    
    if not uploaded_files:
        st.error("No files uploaded for translation.")
        return images_dict
    
    # Filter for image files and sort by name
    image_files = sorted([f for f in uploaded_files 
                         if f.name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"))],
                        key=lambda f: f.name)
    
    for uploaded_file in image_files:
        # Extract page number from filename (e.g., "pg1.png" -> "pg1")
        page_key = os.path.splitext(uploaded_file.name)[0]
        try:
            # Store as PIL Image object for processing
            images_dict[page_key] = Image.open(uploaded_file)
            # Important: need to load the image data into memory before the file handle closes
            images_dict[page_key].load()
        except Exception as e:
            st.error(f"Failed to load image {uploaded_file.name}: {e}")
    
    return images_dict


def _compute_translations(images_dict, uploaded_files, session_state):
    """
    Run OCR and translations on provided PIL Image objects and store results in session state.
    
    Args:
        images_dict (dict): Dictionary mapping page keys (e.g. "pg1", "pg2") to PIL Image objects.
        uploaded_files (list): List of UploadedFile objects from st.file_uploader.
        session_state: Streamlit session state object.
    """
    translations = {"jp": {}, "en": {"translation model": {}, "llm": {}, "api": {}}}
    pages = []

    clipping_style = session_state.get("clipping_style", "Position JSON")
    translation_method = session_state.get("translation_method", "LLM Based")
    translation_model = session_state.get("translation_model", "Helsinki-NLP/opus-mt-ja-en")
    llm_model = session_state.get("llm_model", "gemma3:4b")
    api_key = session_state.get("api_key", "")

    if not images_dict:
        st.error("No images provided for translation.")
        return
    
    # Create a dictionary of uploaded position JSON files for quick lookup
    positions_files = {os.path.splitext(f.name)[0]: f for f in uploaded_files 
                       if f.name.lower().endswith("_positions.json")}

    for page_key, image_obj in images_dict.items():
        pages.append(page_key)
        clip_idx = 1

        translations["jp"][page_key] = {}
        translations["en"]["translation model"][page_key] = {}
        translations["en"]["llm"][page_key] = {}
        translations["en"]["api"][page_key] = {}


        if clipping_style == "Position JSON":
            # Look for the positions file in uploaded files by matching the page key
            positions_file_key = f"{page_key}_positions"
            if positions_file_key not in positions_files:
                continue
            
            positions_uploaded_file = positions_files[positions_file_key]
            try:
                positions = json.load(positions_uploaded_file)
            except Exception as e:
                st.error(f"Failed to load positions file {positions_uploaded_file.name}: {e}")
                continue
            
            for box in positions.get("boxes", []):
                x, y, w, h = box['x'], box['y'], box['width'], box['height']
                jp_text = ocr_extractor_crop(image_obj=image_obj, crop_coords=(x, y, w, h))
                translations["jp"][page_key][f"box{clip_idx}"] = jp_text

                if translation_method == 'LLM Based':
                    llm_translated = get_llm_translations(jp_text, llm_model=llm_model)
                    translations["en"]["llm"][page_key][f"box{clip_idx}"] = llm_translated
                    translations["en"]["llm"]["model used"] = llm_model

                if translation_method == 'Translation Model':
                    translated = get_translations(jp_text, translation_model=translation_model)
                    translations["en"]["translation model"][page_key][f"box{clip_idx}"] = translated
                    translations["en"]["translation model"]["model used"] = translation_model

                if translation_method == "API":
                    api_translated = get_api_translations(jp_text, api_key=api_key)
                    translations["en"]["api"][page_key][f"box{clip_idx}"] = api_translated
                    translations["en"]["api"]["model used"] = "OpenAI API"

                clip_idx += 1

        # deprecated, json preferred.
        # elif clipping_style == "Presliced Clips":
        #     clips_dir = os.path.join(manga_loc, "clips", f"pg{page_num}_clips")
        #     if not os.path.isdir(clips_dir):
        #         continue
        #     for clip in os.listdir(clips_dir):
        #         jp_text = ocr_extractor(img=clip, file_dir=clips_dir)
        #         translations["jp"][f"pg{page_num}"][f"clip{clip_idx}"] = jp_text

        #         if translation_method == 'Translation Model':
        #             translated = get_translations(jp_text, translation_model=translation_model)
        #             translations["en"]["translation model"][f"pg{page_num}"][f"clip{clip_idx}"] = translated
        #             translations["en"]["translation model"]["model used"] = translation_model

        #         if translation_method == 'LLM Based':
        #             llm_translated = get_llm_translations(jp_text, llm_model=llm_model)
        #             translations["en"]["llm"][f"pg{page_num}"][f"clip{clip_idx}"] = llm_translated
        #             translations["en"]["llm"]["model used"] = llm_model

        #         if translation_method == "API":
        #             api_translated = get_api_translations(jp_text, api_key=api_key)
        #             translations["en"]["api"][f"pg{page_num}"][f"box{clip_idx}"] = api_translated
        #             translations["en"]["api"]["model used"] = "OpenAI API"

        #         clip_idx += 1

        elif clipping_style == "Full Page": # Be aware this method is not good. But it is left for use if desired. May work better with better OCR models.
            jp_text = ocr_extractor(image_obj=image_obj)
            translations["jp"][page_key]["full_page"] = jp_text
            if translation_method == 'Translation Model':
                translated = get_translations(jp_text, translation_model=translation_model)
                translations["en"]["translation model"][page_key]["full_page"] = translated
                translations["en"]["translation model"]["model used"] = translation_model

            if translation_method == 'LLM Based':
                llm_translated = get_llm_translations(jp_text, llm_model=llm_model)
                translations["en"]["llm"][page_key]["full_page"] = llm_translated
                translations["en"]["llm"]["model used"] = llm_model

                if translation_method == "API":
                    api_translated = get_api_translations(jp_text, api_key=api_key)
                    translations["en"]["api"][page_key][f"box{clip_idx}"] = api_translated
                    translations["en"]["api"]["model used"] = "OpenAI API"

        elif clipping_style == "Text Region Detection":
            text_region_detection(image_obj)
            break


    st.session_state.translations = translations
    st.session_state.pages = pages
    st.session_state.images_dict = images_dict
    st.session_state.translated = True

    return session_state