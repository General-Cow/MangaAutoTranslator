import streamlit as st
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive window
from PIL import Image, ImageDraw
import json
import io
from pathlib import Path
from src.slicer_tools import MangaTextSlicer
import zipfile

# Streamlit App
st.set_page_config(page_title="Manga Text Box Slicer", layout="wide")

st.title("✂️ Manga Text Box Slicer")
st.markdown("Interactive matplotlib-based tool for precise text box selection - Batch Edition")

# Initialize session state
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = {}
if 'current_image_index' not in st.session_state:
    st.session_state.current_image_index = 0
if 'annotations' not in st.session_state:
    st.session_state.annotations = {}  # {image_name: boxes}
if 'image_names_order' not in st.session_state:
    st.session_state.image_names_order = []

# Sidebar
with st.sidebar:
    st.header("📁 Upload Images")
    
    uploaded_files = st.file_uploader("Choose manga images", type=["png", "jpg", "jpeg", "bmp", "gif", "webp"], accept_multiple_files=True)
    
    if uploaded_files:
        # Load all images
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_images:
                st.session_state.uploaded_images[uploaded_file.name] = Image.open(uploaded_file)
                st.session_state.image_names_order.append(uploaded_file.name)
        
        # Show batch progress
        st.markdown("---")
        st.subheader("📊 Batch Progress")
        total_images = len(st.session_state.image_names_order)
        annotated_count = sum(1 for name in st.session_state.image_names_order if name in st.session_state.annotations)
        
        st.metric("Progress", f"{annotated_count}/{total_images} annotated")
        
        # Progress bar
        progress = annotated_count / total_images if total_images > 0 else 0
        st.progress(progress)
        
        # Image list with status
        st.markdown("#### Images to Process")
        for idx, name in enumerate(st.session_state.image_names_order):
            status = "✅" if name in st.session_state.annotations else "⏳"
            if st.button(f"{status} {name}", key=f"select_{idx}"):
                st.session_state.current_image_index = idx
                st.rerun()

# Main area
if st.session_state.uploaded_images:
    current_image_name = st.session_state.image_names_order[st.session_state.current_image_index]
    current_image = st.session_state.uploaded_images[current_image_name]
    current_boxes = st.session_state.annotations.get(current_image_name, [])
    
    # Header with progress
    col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
    with col_header1:
        st.subheader(f"📋 {current_image_name}")
    with col_header2:
        st.metric("Image", f"{st.session_state.current_image_index + 1}/{len(st.session_state.image_names_order)}")
    with col_header3:
        st.metric("Boxes", len(current_boxes))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Annotation Tool")
        
        if st.button("🎯 Open Annotation Tool", type="primary", use_container_width=True, key="open_annotation_tool"):
            st.warning("⏳ Matplotlib window should open in a new window. Check your taskbar if you don't see it!")
            
            try:
                # Create slicer and show
                slicer = MangaTextSlicer(current_image)
                boxes = slicer.show()
                
                # Store results
                if boxes:
                    st.session_state.annotations[current_image_name] = boxes
                    st.success(f"✅ Created {len(boxes)} text boxes for {current_image_name}!")
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
                """)
        
        # Show current boxes on image
        if current_boxes:
            st.markdown("---")
            st.subheader("📦 Annotated Image")
            
            # Draw boxes on image
            img_with_boxes = current_image.copy()
            draw = ImageDraw.Draw(img_with_boxes)
            
            for i, box in enumerate(current_boxes):
                x, y, w, h = box['x'], box['y'], box['width'], box['height']
                draw.rectangle([x, y, x+w, y+h], outline='lime', width=3)
                draw.rectangle([x, y-25, x+35, y], fill='lime')
                draw.text((x+5, y-20), str(i+1), fill='black')
            
            st.image(img_with_boxes, use_container_width=True)
    
    with col2:
        st.subheader("📋 Results")
        
        if current_boxes:
            st.metric("Total Boxes", len(current_boxes))
            
            # Show box details
            st.markdown("#### Box Coordinates")
            for i, box in enumerate(current_boxes):
                with st.expander(f"Box {i+1}"):
                    st.write(f"**Position:** ({box['x']}, {box['y']})")
                    st.write(f"**Size:** {box['width']} × {box['height']} px")
            
            # Export single image JSON
            st.markdown("---")
            st.markdown("#### 📥 Export Current")
            
            export_data = {
                "image_name": current_image_name,
                "image_width": current_image.width,
                "image_height": current_image.height,
                "boxes": current_boxes
            }
            
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"{Path(current_image_name).stem}_positions.json",
                mime="application/json",
                use_container_width=True
            )
            
            # Clear button
            if st.button("🗑️ Clear Boxes", use_container_width=True, key="clear_boxes"):
                st.session_state.annotations[current_image_name] = []
                st.rerun()
        else:
            st.info("👈 Click 'Open Annotation Tool' to start drawing boxes")
    
    # Navigation buttons
    st.markdown("---")
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        if st.session_state.current_image_index > 0:
            if st.button("⬅️ Previous", use_container_width=True, key="nav_previous"):
                st.session_state.current_image_index -= 1
                st.rerun()
    
    with nav_col2:
        if st.session_state.current_image_index < len(st.session_state.image_names_order) - 1:
            if st.button("Next ➡️", use_container_width=True, key="nav_next"):
                st.session_state.current_image_index += 1
                st.rerun()
    
    with nav_col3:
        if st.session_state.current_image_index < len(st.session_state.image_names_order) - 1:
            if st.button("Skip ⏭️", use_container_width=True, key="nav_skip"):
                st.session_state.current_image_index += 1
                st.rerun()
    
    with nav_col4:
        pass
    
    # Batch export section
    st.markdown("---")
    st.subheader("📦 Batch Export")
    
    annotated_images = {name: st.session_state.annotations[name] 
                       for name in st.session_state.image_names_order 
                       if name in st.session_state.annotations}
    
    if annotated_images:
        st.info(f"✅ Ready to export {len(annotated_images)}/{len(st.session_state.image_names_order)} images")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Download all JSONs as zip
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for image_name, boxes in annotated_images.items():
                    image_obj = st.session_state.uploaded_images[image_name]
                    export_data = {
                        "image_name": image_name,
                        "image_width": image_obj.width,
                        "image_height": image_obj.height,
                        "boxes": boxes
                    }
                    json_filename = f"{Path(image_name).stem}_positions.json"
                    zip_file.writestr(json_filename, json.dumps(export_data, indent=2))
            zip_buffer.seek(0)
            st.download_button(
                label="📥 Download All JSONs (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="position_jsons.zip",
                mime="application/zip",
                use_container_width=True,
                key="download_all_jsons_zip"
            )
        
        with col_export2:
            # Download combined JSON
            combined_data = {}
            for image_name, boxes in annotated_images.items():
                image_obj = st.session_state.uploaded_images[image_name]
                combined_data[image_name] = {
                    "image_width": image_obj.width,
                    "image_height": image_obj.height,
                    "boxes": boxes
                }
            st.download_button(
                label="📄 Download Combined JSON",
                data=json.dumps(combined_data, indent=2),
                file_name="all_annotations.json",
                mime="application/json",
                use_container_width=True,
                key="download_combined_json"
            )
    else:
        st.warning("⚠️ Annotate at least one image to enable batch export")

else:
    # Welcome screen
    st.info("👈 Upload manga images from the sidebar to begin batch annotation")
