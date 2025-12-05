import os
import streamlit as st
from src.ocr_extractor import ocr_extractor
from src.slicer import presliced_clips, manual_slicing, text_region_detection
from src.translator import get_translations, get_llm_translations
from src.evaluator import eval_translations, reference_wrapper

st.set_page_config(page_title="Manga Auto Translator", layout="wide")

st.title("Manga Auto Translator")
# st.write("Upload an image or a folder of images containing Japanese text, and get the translated English text!")

# uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif", "webp"])
# if uploaded_file:

# idea have a directory for clips to translate and pages to display.
# try columns in streamlit to show image and text side by side.

# Add page slicing tab/page. Likely just integrate python-manga-slicer as a page. Either way I have my workflow.


# st.button("Translate Manga")
with st.sidebar:
    st.header("Translation Settings")
    manga_loc = st.text_input("Directory containing manga", placeholder="Input folder path here")
# Include options for translation models, translation style (llm based vs translation model based), and other stuff.
# Consider putting filepath entry here. Probably then need to make a click through thing in the main app area.
# Then either display as you go and or collect inputs and do all at once.

    # Will need to implement if statements later. After rework for by page display
    st.write("Text clipping style.")
    clipping_style = st.selectbox(
        "Clipping Style",
        ("Presliced Clips", "Manual Slicing", "Text Region Detection"),
    )
    # st.write("Select translation model and options.")
    # translation_model = st.sidebar.selectbox(



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
            # Will need to add features such as number of slices. Here or later add a feature to review clips before translation?            with col2:
            with col2:
                if clipping_style == "Presliced Clips":
                    presliced_clips(page_num, manga_loc)

                elif clipping_style == "Manual Slicing":
                # implement later, first.
                    st.write("Manual slicing not implemented yet.")
                    manual_slicing(f"{manga_loc}/pages/pg{page_num}")
                    break
                    
                elif clipping_style == "Text Region Detection":
                # implement later. Likely use pytesseract or similar.
                    st.write("Text Region Detection not implemented yet.")
                    text_region_detection(f"{manga_loc}/pages/pg{page_num}")
                    break

