import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO

# Page config
st.set_page_config(page_title="AI Face Detector", layout="centered")

st.title("👤 AI Face Detection Web Model by Alok and Akash")
st.write("Upload an image or take a camera snap to detect faces using YOLOv8.")

# Load model
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# Confidence slider
confidence = st.slider("Detection Confidence", min_value=0.1, max_value=1.0, value=0.35, step=0.05)

# Image uploader / Camera input
uploaded_file = st.file_uploader("Upload Image or Take Photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file).convert("RGB")
    
    # Run YOLO prediction
    results = model.predict(source=image, conf=confidence, verbose=False)
    
    # Render bounding boxes
    annotated_array = results[0].plot()
    output_image = Image.fromarray(annotated_array[..., ::-1])
    
    # Display result
    num_faces = len(results[0].boxes)
    st.success(f"🎯 Total Faces Detected: {num_faces}")
    st.image(output_image, caption="Detection Result", use_container_width=True)
  
