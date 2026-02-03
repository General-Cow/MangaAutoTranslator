import streamlit as st

home_page = st.Page("pages/home.py", title="Home", icon="🏠")
translation_page = st.Page("pages/autotranslator.py", title="Auto Translator", icon="💬")
slicer_page = st.Page("pages/manual_slicer.py", title="Manual Slicer", icon="✂️")
reader_page = st.Page("pages/reader.py", title="Reader", icon="📖")

pg = st.navigation([home_page, translation_page, slicer_page, reader_page])
pg.run()