from transformers import pipeline
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI
import streamlit as st
import json
import os
from src.ocr_extractor import ocr_extractor, ocr_extractor_crop
from src.slicer_tools import text_region_detection


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

# def _compute_translations(manga_loc, clipping_style, translation_method, translation_model=None, llm_model=None, api_key=None):
def _compute_translations(session_state):
    """Run OCR and translations and store results in session state."""
    translations = {"jp": {}, "en": {"translation model": {}, "llm": {}, "api": {}}}
    pages = []

    manga_loc = session_state.get("manga_loc", "")
    clipping_style = session_state.get("clipping_style", "Position JSON")
    translation_method = session_state.get("translation_method", "LLM Based")
    translation_model = session_state.get("translation_model", "Helsinki-NLP/opus-mt-ja-en")
    llm_model = session_state.get("llm_model", "gemma3:4b")
    api_key = session_state.get("api_key", "")

    pages_dir = os.path.join(manga_loc, "pages")
    if not os.path.isdir(pages_dir):
        st.error("Pages directory not found. Check the 'Directory containing manga' path.")
        return

    for img in os.listdir(pages_dir):
        pages.append(img)
        clip_idx = 1
        page_num = img.split(".")[0].split("pg")[1]

        translations["jp"][f"pg{page_num}"] = {}
        translations["en"]["translation model"][f"pg{page_num}"] = {}
        translations["en"]["llm"][f"pg{page_num}"] = {}
        translations["en"]["api"][f"pg{page_num}"] = {}


        if clipping_style == "Position JSON":
            json_path = os.path.join(manga_loc, "positions", f"pg{page_num}_positions.json")
            if not os.path.isfile(json_path):
                continue
            with open(json_path, "r") as f:
                positions = json.load(f)
            for box in positions.get("boxes", []):
                x, y, w, h = box['x'], box['y'], box['width'], box['height']
                jp_text = ocr_extractor_crop(img=img, file_dir=pages_dir, crop_coords=(x, y, w, h))
                translations["jp"][f"pg{page_num}"][f"box{clip_idx}"] = jp_text

                if translation_method == 'LLM Based':
                    llm_translated = get_llm_translations(jp_text, llm_model=llm_model)
                    translations["en"]["llm"][f"pg{page_num}"][f"box{clip_idx}"] = llm_translated
                    translations["en"]["llm"]["model used"] = llm_model

                if translation_method == 'Translation Model':
                    translated = get_translations(jp_text, translation_model=translation_model)
                    translations["en"]["translation model"][f"pg{page_num}"][f"box{clip_idx}"] = translated
                    translations["en"]["translation model"]["model used"] = translation_model

                if translation_method == "API":
                    api_translated = get_api_translations(jp_text, api_key=api_key)
                    translations["en"]["api"][f"pg{page_num}"][f"box{clip_idx}"] = api_translated
                    translations["en"]["api"]["model used"] = "OpenAI API"

                clip_idx += 1


        elif clipping_style == "Presliced Clips":
            clips_dir = os.path.join(manga_loc, "clips", f"pg{page_num}_clips")
            if not os.path.isdir(clips_dir):
                continue
            for clip in os.listdir(clips_dir):
                jp_text = ocr_extractor(img=clip, file_dir=clips_dir)
                translations["jp"][f"pg{page_num}"][f"clip{clip_idx}"] = jp_text

                if translation_method == 'Translation Model':
                    translated = get_translations(jp_text, translation_model=translation_model)
                    translations["en"]["translation model"][f"pg{page_num}"][f"clip{clip_idx}"] = translated
                    translations["en"]["translation model"]["model used"] = translation_model

                if translation_method == 'LLM Based':
                    llm_translated = get_llm_translations(jp_text, llm_model=llm_model)
                    translations["en"]["llm"][f"pg{page_num}"][f"clip{clip_idx}"] = llm_translated
                    translations["en"]["llm"]["model used"] = llm_model

                if translation_method == "API":
                    api_translated = get_api_translations(jp_text, api_key=api_key)
                    translations["en"]["api"][f"pg{page_num}"][f"box{clip_idx}"] = api_translated
                    translations["en"]["api"]["model used"] = "OpenAI API"

                clip_idx += 1

        elif clipping_style == "Full Page": # Be aware this method is not good. But it is left for use if desired. May work better with better OCR models.
            jp_text = ocr_extractor(img=img, file_dir=pages_dir, multi_file=False)
            translations["jp"][f"pg{page_num}"]["full_page"] = jp_text
            if translation_method == 'Translation Model':
                translated = get_translations(jp_text, translation_model=translation_model)
                translations["en"]["translation model"][f"pg{page_num}"]["full_page"] = translated
                translations["en"]["translation model"]["model used"] = translation_model

            if translation_method == 'LLM Based':
                llm_translated = get_llm_translations(jp_text, llm_model=llm_model)
                translations["en"]["llm"][f"pg{page_num}"]["full_page"] = llm_translated
                translations["en"]["llm"]["model used"] = llm_model

                if translation_method == "API":
                    api_translated = get_api_translations(jp_text, api_key=api_key)
                    translations["en"]["api"][f"pg{page_num}"][f"box{clip_idx}"] = api_translated
                    translations["en"]["api"]["model used"] = "OpenAI API"

        elif clipping_style == "Text Region Detection":
            text_region_detection(os.path.join(manga_loc, f"pages/pg{page_num}"))
            break


    st.session_state.translations = translations
    st.session_state.pages = pages
    st.session_state.translated = True

    return session_state