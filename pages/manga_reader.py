import streamlit as st
import json
from src.translator_tools import load_images_from_uploader

st.set_page_config(page_title="Manga Reader", layout="wide")

st.title("📖 Manga Reader")

st.write("This is a page for viewing translated pages/collections.")
st.write("I will load saved translations and will develop it as a nice and easy reader.")
st.write("Features may include viewing original image, translated text overlay, toggling between original and translated, etc.")

with st.sidebar:
    st.header("📁 Upload Files")
    uploaded_files = st.file_uploader("Upload chapter files (images and translation JSON)", accept_multiple_files=True)
    
    if uploaded_files:
        # Load images
        images_dict = load_images_from_uploader(uploaded_files)
        st.session_state.images_dict = images_dict
        
        # Load translations from JSON - exclude positions JSONs
        json_files = [f for f in uploaded_files 
                     if f.name.lower().endswith(".json") 
                     and not f.name.lower().endswith("_positions.json")]
        
        # Also exclude files with "position" in the name for extra safety
        json_files = [f for f in json_files if "position" not in f.name.lower()]
        
        if json_files:
            # If multiple JSONs, let user choose
            if len(json_files) > 1:
                st.info(f"Found {len(json_files)} JSON files: {[f.name for f in json_files]}")
                selected_json_name = st.selectbox("Select translations file:", [f.name for f in json_files])
                selected_json = next(f for f in json_files if f.name == selected_json_name)
            else:
                selected_json = json_files[0]
            
            try:
                translations = json.load(selected_json)
                st.session_state.translations = translations
                st.success(f"✅ Loaded translations from {selected_json.name}")
            except Exception as e:
                st.error(f"❌ Failed to load JSON: {e}")
                translations = st.session_state.get("translations", {})
        else:
            st.warning("⚠️ No translation JSON file found. Looking for .json files (excluding position files)")
            translations = st.session_state.get("translations", {})
    else:
        images_dict = st.session_state.get("images_dict", {})
        translations = st.session_state.get("translations", {})

st.session_state.pages = list(images_dict.keys()) if images_dict else []


def _render_chapter(pages, images_dict, translations):
    """Render images and translations from session state."""
    if not pages:
        st.info("No pages to display. Upload files to get started.")
        return

    # Get available translation keys for matching
    jp_keys = list(translations.get("jp", {}).keys())
    
    for page_key in pages:
        # Find matching translation key (handle both exact match and suffix match)
        matching_trans_key = None
        if page_key in translations.get("jp", {}):
            matching_trans_key = page_key
        else:
            # Try to find a match by suffix (e.g., "007" matches "test/007")
            for trans_key in jp_keys:
                if trans_key.endswith(page_key) or trans_key.endswith(f"/{page_key}") or trans_key.split("/")[-1] == page_key:
                    matching_trans_key = trans_key
                    break
        
        st.write(f"Page {page_key}")
        col1, col2 = st.columns(2)
        with col1:
            if page_key in images_dict:
                st.image(images_dict[page_key])
            else:
                st.warning(f"Image not found for {page_key}")
        with col2:
            if matching_trans_key:
                # Show JP text and translations if present
                jp_page = translations.get("jp", {}).get(matching_trans_key, {})
                tm_page = translations.get("en", {}).get("translation model", {}).get(matching_trans_key, {})
                llm_page = translations.get("en", {}).get("llm", {}).get(matching_trans_key, {})
                api_page = translations.get("en", {}).get("api", {}).get(matching_trans_key, {})

                for clip_key, jp_text in jp_page.items():
                    st.markdown(f"**{clip_key} (JP):** {jp_text}")
                    if clip_key in tm_page:
                        st.markdown(f"- **Translation model:** {tm_page[clip_key]}")
                    if clip_key in llm_page:
                        st.markdown(f"- **LLM:** {llm_page[clip_key]}")
                    if clip_key in api_page:
                        st.markdown(f"- **API:** {api_page[clip_key]}")
            else:
                st.warning(f"No translations found for {page_key}")


pages = st.session_state.get("pages", [])
images_dict = st.session_state.get("images_dict", {})
translations = st.session_state.get("translations", {})

# Debug info
with st.expander("📊 Debug Info"):
    st.write(f"Pages: {pages}")
    st.write(f"Images dict keys: {list(images_dict.keys())}")
    st.write(f"Translations keys: {list(translations.keys())}")
    if "jp" in translations:
        st.write(f"JP page keys: {list(translations.get('jp', {}).keys())}")

if pages and translations:
    _render_chapter(pages, images_dict, translations)
else:
    if not pages:
        st.info("No pages loaded. Upload images to get started.")
    if not translations:
        st.info("No translations loaded. Upload a translation JSON to get started.")