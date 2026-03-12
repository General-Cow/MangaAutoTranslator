import streamlit as st

st.title("MangaAutoTranslator")
st.markdown("MangaAutoTranslator is a complete pipeline for translating manga. It inlcudes preprocessing, OCR, translation, and a viewer.")

st.header("Features")

st.markdown("- **Preprocessing**: Clean up and prepare manga images for OCR.")
st.markdown("- **OCR**: Extract text from manga images using advanced OCR techniques.")
st.markdown("- **Translation**: Translate extracted text into different languages using state-of-the-art translation models.")
st.markdown("- **Viewer**: View translated manga with an intuitive interface.")

st.header("Getting Started")
st.markdown("To get started, navigate to the different pages using the sidebar:")
st.markdown("- **Auto Translator**: Upload manga images and get translations.")
st.markdown("- **Manual Slicer**: Manually slice manga images for better OCR results.")
st.markdown("- **Reader**: View your translated manga in a reader format.")
