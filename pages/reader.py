import streamlit as st
import json
import os

st.set_page_config(page_title="Manga Auto Translator", layout="wide")

st.write("This is a page for viewing translated pages/collections.")
st.write("I will load saved translations and will develop it as a nice and easy reader.")
st.write("Features may include viewing original image, translated text overlay, toggling between original and translated, etc.")

pages_dir = st.text_input("Enter the path to the chapter folder", value="path/to/chapter/folder")
pages = []
try:
    for img in os.listdir(pages_dir):
        pages.append(img)
except FileNotFoundError:    st.error("Directory not found. Please check the path and try again.")
st.session_state.pages = pages

translations_raw = st.file_uploader("Upload translation json here", type=["json"])
if translations_raw is not None:
    translations = json.load(translations_raw)
    st.session_state.translations = translations
else:
    translations = st.session_state.get("translations", {})



def _render_chapter(pages, translations):
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
            st.image(os.path.join(pages_dir, img))
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


if pages and translations:
    _render_chapter(st.session_state.pages, st.session_state.translations)