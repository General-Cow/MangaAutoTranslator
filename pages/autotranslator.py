import os
import json
import streamlit as st
from src.translator_tools import _compute_translations, load_images_from_uploader
from src.display_tools import _render_translations

st.set_page_config(page_title="Manga AutoTranslator", layout="wide")

st.title("💬 Manga AutoTranslator")
st.markdown("Automated JP to EN translation tool for manga pages using OCR, translation models, and LLMs.")

with st.sidebar:
    st.header("⚙ Translation Settings")
    # manga_loc = st.text_input("Directory containing manga", placeholder="Input folder path here")
    manga_loc = st.file_uploader(label="Select directory containing manga chapter", accept_multiple_files="directory")

    clipping_style = st.selectbox(
        "Clipping Style",
        ("Position JSON", "Presliced Clips", "Full Page", "Text Region Detection"),
    )
    
    # Easy OCR is shockingly bad. May not bother looking for other OCR models as MangaOCR seems to work well.
    # ocr_model = st.selectbox(
    #     "OCR Model",
    #     ("MangaOCR", "EasyOCR"),
    # )

    translation_method = st.selectbox('Translation Method', ('LLM Based', 'Translation Model', "API"))

    if translation_method == 'LLM Based':
        llm_model = st.selectbox(
            "LLM Model",
            ('gemma3:4b', 'gemma3:12b', 'gemma3:27b',  'llama3', 'qwen2.5:14b', "7shi/gemma-2-jpn-translate:2b-instruct-q8_0", "mistral-nemo"),
        )

    if translation_method == 'Translation Model':
        translation_model = st.selectbox(
            "Translation Model",
            ("Helsinki-NLP/opus-mt-ja-en", "facebook/nllb-200-3.3B", "facebook/nllb-200-distilled-600M"), 
        )

    if translation_method == "API":
        api_key = st.text_input("API Key", placeholder="Enter your API key here", type="password")
        # keep playing with openai api. I hate their docs, i hate their docs, i hate their docs.
    
    # May need to rework. Seems that some stuff still needs to be saved or reworked when I swap pages.
    st.session_state.manga_loc = manga_loc
    st.session_state.clipping_style = clipping_style
    st.session_state.translation_method = translation_method
    st.session_state.translation_model = translation_model if 'translation_model' in locals() else None
    st.session_state.llm_model = llm_model if 'llm_model' in locals() else None
    st.session_state.api_key = api_key if 'api_key' in locals() else None
    

### Main page logic
button_col1, button_col2, button_col3 = st.columns(3)

with button_col1:
    with st.container(horizontal_alignment="center"):
        if st.button("Translate Manga", key="translate_manga"):
            images_dict = load_images_from_uploader(st.session_state.manga_loc)
            st.session_state = _compute_translations(images_dict, st.session_state.manga_loc, st.session_state)

# If translations exist in session state, render them and provide download
if st.session_state.get("translated", False):
    # Provide a download button that uses the session_state data so reruns keep the UI.
    with button_col2:
        with st.container(horizontal_alignment="center"):
            st.download_button(
                "Download Translations",
                data=json.dumps(st.session_state.get("translations", {}), ensure_ascii=False, indent=4),
                file_name="translations.json", # Consider making this more descriptive, e.g. models used and timestamp
                mime="application/json",
                key="download_translations",
        )
    with button_col3:
        with st.container(horizontal_alignment="center"):
            st.button("Reset Page", key="reset_page", type="primary", on_click=lambda: st.session_state.clear())

    _render_translations(st.session_state)

else:
    # Welcome screen
    st.info("👈 Enter the path to your manga images to translate in the sidebar to begin")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📁 Enter Path")
        st.markdown("Enter the folder path to your images")
    with col2:
        st.markdown("### 🧰 Options")
        st.markdown("Customize translation and slicing options")
    with col3:
        st.markdown("### 💾 Export")
        st.markdown("Download translations paired to your images")
