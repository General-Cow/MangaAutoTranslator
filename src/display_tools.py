import streamlit as st
import os


def _render_translations(session_state):
    """Render images and translations from session state."""
    manga_loc = session_state.get("manga_loc", "")
    
    translations = session_state.get("translations", {})
    pages = session_state.get("pages", [])
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
            api_page = translations.get("en", {}).get("api", {}).get(f"pg{page_num}", {})

            for clip_key, jp_text in jp_page.items():
                st.markdown(f"**{clip_key} (JP):** {jp_text}")
                if clip_key in tm_page:
                    st.markdown(f"- **Translation model:** {tm_page[clip_key]}")
                if clip_key in llm_page:
                    st.markdown(f"- **LLM:** {llm_page[clip_key]}")
                if clip_key in api_page:
                    st.markdown(f"- **API:** {api_page[clip_key]}")