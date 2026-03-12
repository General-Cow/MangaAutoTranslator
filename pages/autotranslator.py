import os
import json
import streamlit as st
from src.ocr_extractor import ocr_extractor, ocr_extractor_crop
from src.slicer_tools import manual_slicing, text_region_detection
from src.translator import get_translations, get_llm_translations
from src.evaluator import eval_translations, reference_wrapper


st.set_page_config(page_title="Manga AutoTranslator", layout="wide")

st.title("💬 Manga AutoTranslator")
st.markdown("Automated JP to EN translation tool for manga pages using OCR, translation models, and LLMs.")

with st.sidebar:
    st.header("⚙ Translation Settings")
    manga_loc = st.text_input("Directory containing manga", placeholder="Input folder path here")

    clipping_style = st.selectbox(
        "Clipping Style",
        ("Presliced Clips", "Position JSON", "Full Page", "Text Region Detection"),
    )
    
    translation_method = st.selectbox('Translation Method', ('Translation Model', 'LLM Based', 'Both', "API"))

    if translation_method in ['Translation Model', 'Both']:
        translation_model = st.selectbox(
            "Translation Model",
            ("Helsinki-NLP/opus-mt-ja-en", "facebook/nllb-200-3.3B", "facebook/nllb-200-distilled-600M"), 
        )
    
    if translation_method in ['LLM Based', 'Both']:
        llm_model = st.selectbox(
            "LLM Model",
            ('gemma3:4b', 'gemma3:12b', 'llama3', "7shi/gemma-2-jpn-translate:2b-instruct-q8_0", "mistral-nemo"),
        )

    if translation_method == "API":
        st.text_input("API Key", placeholder="Enter your API key here")
        # keep playing with openai api. I hate their docs, i hate their docs, i hate their docs.
    
    # May need to rework. Seems that some stuff still needs to be saved or reworked when I swap pages.
    st.session_state.manga_loc = manga_loc
    st.session_state.clipping_style = clipping_style
    st.session_state.translation_method = translation_method
    st.session_state.translation_model = translation_model if 'translation_model' in locals() else None
    st.session_state.llm_model = llm_model if 'llm_model' in locals() else None


def _compute_translations(manga_loc, clipping_style, translation_method, translation_model=None, llm_model=None):
    """Run OCR and translations and store results in session state."""
    translations = {"jp": {}, "en": {"translation model": {}, "llm": {}}}
    pages = []

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

        if clipping_style == "Presliced Clips":
            clips_dir = os.path.join(manga_loc, "clips", f"pg{page_num}_clips")
            if not os.path.isdir(clips_dir):
                continue
            for clip in os.listdir(clips_dir):
                jp_text_list = ocr_extractor(img=clip, file_dir=clips_dir, multi_file=False)
                translations["jp"][f"pg{page_num}"][f"clip{clip_idx}"] = jp_text_list[0]

                if translation_method in ['Translation Model', 'Both']:
                    translated = get_translations(jp_text_list, translation_model=translation_model, concat_sent=False)
                    translations["en"]["translation model"][f"pg{page_num}"][f"clip{clip_idx}"] = translated[0]
                    translations["en"]["translation model"]["model used"] = translation_model

                if translation_method in ['LLM Based', 'Both']:
                    llm_translated = get_llm_translations(jp_text_list, llm_model=llm_model)
                    translations["en"]["llm"][f"pg{page_num}"][f"clip{clip_idx}"] = llm_translated[0]
                    translations["en"]["llm"]["model used"] = llm_model

                clip_idx += 1

        elif clipping_style == "Position JSON":
            json_path = os.path.join(manga_loc, "positions", f"pg{page_num}_positions.json")
            if not os.path.isfile(json_path):
                continue
            with open(json_path, "r") as f:
                positions = json.load(f)
            for box in positions.get("boxes", []):
                x, y, w, h = box['x'], box['y'], box['width'], box['height']
                jp_text_list = ocr_extractor_crop(img=img, file_dir=pages_dir, crop_coords=(x, y, w, h))
                translations["jp"][f"pg{page_num}"][f"box{clip_idx}"] = jp_text_list[0]

                if translation_method in ['Translation Model', 'Both']:
                    translated = get_translations(jp_text_list, translation_model=translation_model, concat_sent=False)
                    translations["en"]["translation model"][f"pg{page_num}"][f"box{clip_idx}"] = translated[0]
                    translations["en"]["translation model"]["model used"] = translation_model

                if translation_method in ['LLM Based', 'Both']:
                    llm_translated = get_llm_translations(jp_text_list, llm_model=llm_model)
                    translations["en"]["llm"][f"pg{page_num}"][f"box{clip_idx}"] = llm_translated[0]
                    translations["en"]["llm"]["model used"] = llm_model
                clip_idx += 1

        elif clipping_style == "Full Page":
            manual_slicing(os.path.join(manga_loc, f"pages/pg{page_num}"))
            break

        elif clipping_style == "Text Region Detection":
            text_region_detection(os.path.join(manga_loc, f"pages/pg{page_num}"))
            break

    st.session_state.translations = translations
    st.session_state.pages = pages
    st.session_state.translated = True


def _render_translations(manga_loc):
    """Render images and translations from session state."""
    translations = st.session_state.get("translations", {})
    pages = st.session_state.get("pages", [])
    if not pages:
        return

    for img in pages:
        page_num = img.split(".")[0].split("pg")[1]
        st.write(f"Page {page_num}")
        col1, col2 = st.columns(2)
        with col1:
            st.image(os.path.join(manga_loc, "pages", img))
        with col2:
            # Show JP text and translations if present
            jp_page = translations.get("jp", {}).get(f"pg{page_num}", {})
            tm_page = translations.get("en", {}).get("translation model", {}).get(f"pg{page_num}", {})
            llm_page = translations.get("en", {}).get("llm", {}).get(f"pg{page_num}", {})

            for clip_key, jp_text in jp_page.items():
                st.markdown(f"**{clip_key} (JP):** {jp_text}")
                if clip_key in tm_page:
                    st.markdown(f"- **Translation model:** {tm_page[clip_key]}")
                if clip_key in llm_page:
                    st.markdown(f"- **LLM:** {llm_page[clip_key]}")


if st.button("Translate Manga", key="translate_manga"):
    # compute translations and store in session state
    _compute_translations(manga_loc, clipping_style, translation_method,
                          translation_model=(translation_model if 'translation_model' in globals() else None),
                          llm_model=(llm_model if 'llm_model' in globals() else None))

# If translations exist in session state, render them and provide download
if st.session_state.get("translated", False):
    # Provide a download button that uses the session_state data so reruns keep the UI
    st.download_button(
        "Download Translations",
        data=json.dumps(st.session_state.get("translations", {}), ensure_ascii=False, indent=4),
        file_name="translations.json", # Consider making this more descriptive, e.g. models used and timestamp
        mime="application/json",
        key="download_translations",
    )

    _render_translations(manga_loc)



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
