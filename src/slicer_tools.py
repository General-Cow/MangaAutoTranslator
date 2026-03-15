import os
import streamlit as st
import streamlit as st
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive window
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Looks like pngs are getting messed up by when displayed in the matplotlib window.
# Seems like it was related to a specific png. Keep an eye on it and see if I need some sort of handling later. 
class MangaTextSlicer:
    def __init__(self, image):
        self.image = image
        self.img_array = np.array(self.image)
        self.boxes = []
        self.current_box = None
        self.start_point = None
        self.fig = None
        self.ax = None
        
    def initialize_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.ax.imshow(self.img_array)
        self.ax.set_title('Click and drag to create text boxes\nPress Enter when done | Backspace to undo last box', 
                         fontsize=12, pad=10)
        
        # Connect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.start_point = (event.xdata, event.ydata)
        
    def on_motion(self, event):
        if self.start_point is None or event.inaxes != self.ax:
            return
            
        if self.current_box is not None:
            self.current_box.remove()
            
        x0, y0 = self.start_point
        width = event.xdata - x0
        height = event.ydata - y0
        
        self.current_box = patches.Rectangle(
            (x0, y0), width, height,
            linewidth=2, edgecolor='red',
            facecolor='none', linestyle='--'
        )
        self.ax.add_patch(self.current_box)
        self.fig.canvas.draw()
        
    def on_release(self, event):
        if self.start_point is None or event.inaxes != self.ax:
            return
            
        x0, y0 = self.start_point
        x1, y1 = event.xdata, event.ydata
        
        x_min = min(x0, x1)
        y_min = min(y0, y1)
        x_max = max(x0, x1)
        y_max = max(y0, y1)
        
        width = x_max - x_min
        height = y_max - y_min
        
        if width > 10 and height > 10:
            box_dict = {
                'x': int(x_min),
                'y': int(y_min),
                'width': int(width),
                'height': int(height)
            }
            self.boxes.append(box_dict)
            
            if self.current_box is not None:
                self.current_box.remove()
                
            rect = patches.Rectangle(
                (x_min, y_min), width, height,
                linewidth=2, edgecolor='lime',
                facecolor='none'
            )
            self.ax.add_patch(rect)
            
            self.ax.text(
                x_min + 5, y_min + 20,
                str(len(self.boxes)),
                color='lime', fontsize=14, weight='bold',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.7)
            )
            
            self.fig.canvas.draw()
        
        self.start_point = None
        self.current_box = None
        
    def on_key(self, event):
        if event.key == 'enter':
            plt.close()
        elif event.key == 'backspace' and len(self.boxes) > 0:
            self.boxes.pop()
            self.redraw()
            
    def redraw(self):
        self.ax.clear()
        self.ax.imshow(self.img_array)
        self.ax.set_title('Click and drag to create text boxes\nPress Enter when done | Backspace to undo last box', 
                         fontsize=12, pad=10)
        
        for i, box in enumerate(self.boxes):
            rect = patches.Rectangle(
                (box['x'], box['y']), box['width'], box['height'],
                linewidth=2, edgecolor='lime',
                facecolor='none'
            )
            self.ax.add_patch(rect)
            
            self.ax.text(
                box['x'] + 5, box['y'] + 20,
                str(i + 1),
                color='lime', fontsize=14, weight='bold',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.7)
            )
        
        self.fig.canvas.draw()
        
    def show(self):
        try:
            self.initialize_plot()
            plt.show(block=True)  # Block until window is closed
            return self.boxes
        except Exception as e:
            st.error(f"Error opening matplotlib window: {e}")
            st.info("Make sure you have tkinter installed. On Linux: `sudo apt-get install python3-tk`")
            return []

    
def text_region_detection(page_path):
    pass


# def slice_grid(page_path, rows=2, cols=2, output_dir=None):
#     os.makedirs(output_dir, exist_ok=True)
#     img = Image.open(page_path)
#     w, h = img.size
#     clips = []
#     base = os.path.splitext(os.path.basename(page_path))[0]
#     for r in range(rows):
#         for c in range(cols):
#             left = int(c * w / cols)
#             upper = int(r * h / rows)
#             right = int((c + 1) * w / cols)
#             lower = int((r + 1) * h / rows)
#             crop = img.crop((left, upper, right, lower))
#             name = f"{base}_r{r}_c{c}.png"
#             out_path = os.path.join(output_dir, name)
#             crop.save(out_path)
#             clips.append(out_path)
#     return clips

# def slice_by_text_regions(page_path, output_dir=None, min_conf=40, pad=8):
#     """
#     Use pytesseract to extract text bounding boxes and save cropped regions.
#     Falls back to a 2x2 grid if no regions detected.
#     """
#     try:
#         import pytesseract
#         from pytesseract import Output
#     except Exception:
#         # pytesseract not available => fallback to grid
#         return slice_grid(page_path, rows=2, cols=2, output_dir=output_dir)

#     os.makedirs(output_dir, exist_ok=True)
#     img = Image.open(page_path)
#     data = pytesseract.image_to_data(img, output_type=Output.DICT, lang='jpn+eng')
#     n = len(data.get('level', []))
#     clips = []
#     base = os.path.splitext(os.path.basename(page_path))[0]

#     for i in range(n):
#         try:
#             conf = float(data['conf'][i])
#         except Exception:
#             conf = -1
#         if conf >= min_conf:
#             left = max(0, int(data['left'][i]) - pad)
#             top = max(0, int(data['top'][i]) - pad)
#             width = int(data['width'][i]) + pad * 2
#             height = int(data['height'][i]) + pad * 2
#             right = min(img.width, left + width)
#             bottom = min(img.height, top + height)
#             crop = img.crop((left, top, right, bottom))
#             name = f"{base}_box{i}.png"
#             out_path = os.path.join(output_dir, name)
#             crop.save(out_path)
#             clips.append(out_path)

#     if not clips:
#         # fallback
#         return slice_grid(page_path, rows=2, cols=2, output_dir=output_dir)
#     return clips