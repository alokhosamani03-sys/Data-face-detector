import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import os

# Page configuration
st.set_page_config(
    page_title="AI Face Detection | Alok & Akash",
    page_icon="⚡",
    layout="centered"
)

# Custom Modern Futuristic CSS
st.markdown("""
<style>
    /* Global background and typography */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sleek Title Gradient */
    .main-title {
        font-size: 2.2rem !important;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #00C6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        padding-top: 10px;
    }
    
    .sub-title {
        text-align: center;
        color: #94A3B8;
        font-size: 0.95rem;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }

    /* Modern Card Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Result Badge */
    .detection-badge {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: #000;
        font-weight: 600;
        font-size: 1rem;
        padding: 10px 18px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.2);
    }
    
    /* Subtle Micro-Signature */
    .signature {
        text-align: right;
        font-size: 0.62rem;
        color: rgba(148, 163, 184, 0.4);
        font-style: italic;
        letter-spacing: 1.5px;
        margin-top: 40px;
        padding-right: 5px;
        user-select: none;
    }
    
    /* Hide Streamlit default menu & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-title">AI face detection web model by Alok and Akash</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">⚡ Real-time edge inference powered by YOLOv8</div>', unsafe_allow_html=True)

# Check for model file
if not os.path.exists("best.pt"):
    st.error("⚠️ Error: 'best.pt' weights file not found in repository.")
    st.stop()

@st.cache_resource
def load_model():
    return YOLO("best.pt")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Controls
confidence = st.slider("🎯 Confidence Threshold", min_value=0.1, max_value=1.0, value=0.35, step=0.05)

# Selection Tabs
tab1, tab2 = st.tabs(["📁 Choose from Gallery", "📸 Live Camera Snap"])

image = None

with tab1:
    uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

with tab2:
    camera_file = st.camera_input("Snap a live selfie")
    if camera_file is not None:
        image = Image.open(camera_file).convert("RGB")

# Detection Process
if image is not None:
    with st.spinner("Analyzing faces..."):
        results = model.predict(source=image, conf=confidence, verbose=False)
        annotated_array = results[0].plot()
        output_image = Image.fromarray(annotated_array[..., ::-1])
        
        num_faces = len(results[0].boxes)
        
        # Display Result
        st.markdown(f'<div class="detection-badge">🎯 Faces Detected: {num_faces}</div>', unsafe_allow_html=True)
        st.image(output_image, use_container_width=True)

# Subtle signature at bottom-right
st.markdown('<div class="signature">built by loki</div>', unsafe_allow_html=True)
