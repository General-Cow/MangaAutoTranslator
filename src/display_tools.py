import streamlit as st


def _render_translations(session_state):
    """Render images and translations from session state."""
    
    translations = session_state.get("translations", {})
    pages = session_state.get("pages", [])
    if not pages:
        return

    for page_key in pages:
        st.write(f"Page {page_key}")
        col1, col2 = st.columns(2)
        with col1:
            # Get the image from the images dict in session state
            images_dict = session_state.get("images_dict", {})
            if images_dict and page_key in images_dict:
                st.image(images_dict[page_key])
            else:
                st.warning(f"Image not found for page {page_key}. Available pages: {list(images_dict.keys())}")
        with col2:
            # Show JP text and translations if present
            jp_page = translations.get("jp", {}).get(page_key, {})
            tm_page = translations.get("en", {}).get("translation model", {}).get(page_key, {})
            llm_page = translations.get("en", {}).get("llm", {}).get(page_key, {})
            api_page = translations.get("en", {}).get("api", {}).get(page_key, {})

            for clip_key, jp_text in jp_page.items():
                st.markdown(f"**{clip_key} (JP):** {jp_text}")
                if clip_key in tm_page:
                    st.markdown(f"- **Translation model:** {tm_page[clip_key]}")
                if clip_key in llm_page:
                    st.markdown(f"- **LLM:** {llm_page[clip_key]}")
                if clip_key in api_page:
                    st.markdown(f"- **API:** {api_page[clip_key]}")