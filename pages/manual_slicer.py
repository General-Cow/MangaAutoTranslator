import streamlit as st
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive window
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
from PIL import Image
# import numpy as np
import json
import io
from pathlib import Path
from src.slicer_tools import MangaTextSlicer

# add bulk download of boxes as clips
# need to fix png display issue in matplotlib window.

# Streamlit App
st.set_page_config(page_title="Manga Text Box Slicer", layout="wide")

st.title("✂️ Manga Text Box Slicer")
st.markdown("Interactive matplotlib-based tool for precise text box selection")

# Initialize session state
if 'boxes' not in st.session_state:
    st.session_state.boxes = []
if 'image' not in st.session_state:
    st.session_state.image = None
if 'image_name' not in st.session_state:
    st.session_state.image_name = None

# Sidebar
with st.sidebar:
    st.header("📁 Upload Image")
    
    uploaded_file = st.file_uploader("Choose a manga image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Load image
        st.session_state.image = Image.open(uploaded_file)
        st.session_state.image_name = uploaded_file.name
        
        # Show preview
        st.image(st.session_state.image, caption="Uploaded Image", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🖱️ Instructions")
        st.info("""
        1. Click **"Open Annotation Tool"** below
        2. A matplotlib window will open
        3. **Click and drag** to draw boxes
        4. **Backspace** to undo last box
        5. **Enter** to finish and return to Streamlit
        """)

# Main area
if st.session_state.image is not None:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Annotation Tool")
        
        if st.button("🎯 Open Annotation Tool", type="primary", use_container_width=True):
            st.warning("⏳ Matplotlib window should open in a new window. Check your taskbar if you don't see it!")
            
            try:
                # Create slicer and show
                slicer = MangaTextSlicer(st.session_state.image)
                boxes = slicer.show()
                
                # Store results
                if boxes:
                    st.session_state.boxes = boxes
                    st.success(f"✅ Created {len(boxes)} text boxes!")
                    st.rerun()
                else:
                    st.info("No boxes were created. The window may have closed without annotations.")
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.markdown("""
                **Troubleshooting:**
                - Make sure tkinter is installed
                - On Windows: Should work by default
                - On Mac: `brew install python-tk`
                - On Linux: `sudo apt-get install python3-tk`
                
                **Alternative:** Try the standalone matplotlib version instead.
                """)
        
        # Show current boxes on image
        if st.session_state.boxes:
            st.markdown("---")
            st.subheader("📦 Annotated Image")
            
            # Draw boxes on image
            img_with_boxes = st.session_state.image.copy()
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img_with_boxes)
            
            for i, box in enumerate(st.session_state.boxes):
                x, y, w, h = box['x'], box['y'], box['width'], box['height']
                draw.rectangle([x, y, x+w, y+h], outline='lime', width=3)
                draw.rectangle([x, y-25, x+35, y], fill='lime')
                draw.text((x+5, y-20), str(i+1), fill='black')
            
            st.image(img_with_boxes, use_container_width=True)
    
    with col2:
        st.subheader("📋 Results")
        
        if st.session_state.boxes:
            st.metric("Total Boxes", len(st.session_state.boxes))
            
            # Show box details
            st.markdown("#### Box Coordinates")
            for i, box in enumerate(st.session_state.boxes):
                with st.expander(f"Box {i+1}"):
                    st.write(f"**Position:** ({box['x']}, {box['y']})")
                    st.write(f"**Size:** {box['width']} × {box['height']} px")
            
            # Export JSON
            st.markdown("---")
            st.markdown("#### 📥 Export Data")
            
            export_data = {
                "image_name": st.session_state.image_name,
                "image_width": st.session_state.image.width,
                "image_height": st.session_state.image.height,
                "boxes": st.session_state.boxes
            }
            
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"{Path(st.session_state.image_name).stem}_boxes.json",
                mime="application/json",
                use_container_width=True
            )
            
            # Slice and preview
            st.markdown("---")
            st.markdown("#### ✂️ Sliced Images")
            
            if st.button("Preview All Slices", use_container_width=True):
                st.session_state.show_slices = True
            
            if st.session_state.get('show_slices', False):
                for i, box in enumerate(st.session_state.boxes):
                    x, y, w, h = box['x'], box['y'], box['width'], box['height']
                    cropped = st.session_state.image.crop((x, y, x+w, y+h))
                    
                    st.image(cropped, caption=f"Box {i+1}", width=200)
                    
                    # Download individual slice
                    buf = io.BytesIO()
                    cropped.save(buf, format='PNG')
                    st.download_button(
                        label=f"⬇️ Download Box {i+1}",
                        data=buf.getvalue(),
                        file_name=f"box_{i+1}.png",
                        mime="image/png",
                        key=f"download_{i}",
                        use_container_width=True
                    )
            
            # Clear button
            st.markdown("---")
            if st.button("🗑️ Clear All Boxes", use_container_width=True):
                st.session_state.boxes = []
                st.session_state.show_slices = False
                st.rerun()
        else:
            st.info("👈 Click 'Open Annotation Tool' to start drawing boxes")

else:
    # Welcome screen
    st.info("👈 Upload a manga image from the sidebar to begin")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📤 Upload")
        st.markdown("Upload your manga page image")
    
    with col2:
        st.markdown("### ✏️ Annotate")
        st.markdown("Draw boxes with matplotlib's interactive tool")
    
    with col3:
        st.markdown("### 💾 Export")
        st.markdown("Download coordinates and sliced images")
