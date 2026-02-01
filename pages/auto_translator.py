import os
import streamlit as st
from src.ocr_extractor import ocr_extractor
from src.slicer_tools import manual_slicing, text_region_detection
from src.translator import get_translations, get_llm_translations
from src.evaluator import eval_translations, reference_wrapper


st.set_page_config(page_title="Manga Auto Translator", layout="wide")

st.title("💬 Manga Auto Translator")
st.markdown("Automated JP to EN translation tool for manga pages using OCR, translation models, and LLMs.")

# Integrate the use of the json files to get the clips.
# Custom models/translation tools.
# Keep playing with models. Not very good so far.
# Incorporate evaluation tools later.


with st.sidebar:
    st.header("⚙ Translation Settings")
    manga_loc = st.text_input("Directory containing manga", placeholder="Input folder path here")
# Include options for translation models, translation style (llm based vs translation model based), and other stuff.
# Consider putting filepath entry here. Probably then need to make a click through thing in the main app area.
# Then either display as you go and or collect inputs and do all at once.

    # Will need to implement if statements later. After rework for by page display
    clipping_style = st.selectbox(
        "Clipping Style",
        ("Presliced Clips", "Manual Slicing", "Text Region Detection"),
    )

    # consider adding OCR model selection later. Will need to rework src/ocr_extractor.py then to include multiple options.
    
    translation_method = st.selectbox('Translation Method', ('Translation Model', 'LLM Based', 'Both'))

    if translation_method in ['Translation Model', 'Both']:
        translation_model = st.selectbox(
            "Translation Model",
            ("Helsinki-NLP/opus-mt-ja-en", "facebook/nllb-200-3.3B", "facebook/nllb-200-distilled-600M"), # add custom option?
        )
    
    if translation_method in ['LLM Based', 'Both']:
        llm_model = st.selectbox(
            "LLM Model",
            ('gemma3:4b', 'gemma3:12b', "7shi/gemma-2-jpn-translate:2b-instruct-q8_0", "mistral-nemo"), # add custom option?
        )


if st.button("Translate Manga"):

# need to rework so it automates multiple pages and clips. See Junko manga rework.
    for img in os.listdir(f"{manga_loc}/pages/"):

        with st.container():
            page_num = img.split(".")[0].split("pg")[1]
            st.write(f"Page {page_num}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(f"{manga_loc}/pages/{img}")

            # regex to extract page number from img name.


            # Likely turn col two into a function to handle different clipping styles.
            # Will need to add features such as number of slices. Here or later add a feature to review clips before translation?
            with col2:
                if clipping_style == "Presliced Clips":
                        for clip in os.listdir(f"{manga_loc}/clips/pg{page_num}_clips/"):
                            jp_text_list = ocr_extractor(img=clip, file_dir=f"{manga_loc}/clips/pg{page_num}_clips/", multi_file=False)
                            st.write(jp_text_list[0])

                            if translation_method in ['Translation Model', 'Both']:
                                translated = get_translations(jp_text_list, translation_model=translation_model, concat_sent=False)
                                st.write("Translation model: ", translated[0])
                            if translation_method in ['LLM Based', 'Both']:                                        
                                llm_translated = get_llm_translations(jp_text_list, llm_model=llm_model)
                                st.write("LLM: ", llm_translated[0])


                elif clipping_style == "Manual Slicing":
                # implement later, first.
                    st.write("Manual slicing not implemented yet. Recommend creating presliced clips using the Manual SLicer page for now.")
                    manual_slicing(f"{manga_loc}/pages/pg{page_num}")
                    break
                    
                elif clipping_style == "Text Region Detection":
                # implement later. Likely use pytesseract or similar.
                    st.write("Text Region Detection not implemented yet.")
                    text_region_detection(f"{manga_loc}/pages/pg{page_num}")
                    break
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
