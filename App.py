import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import os

# Page Configuration
st.set_page_config(
    page_title="Vision System | Alok & Akash",
    page_icon="🤖",
    layout="centered"
)

# --- CLEAN & PROFESSIONAL CSS STYLING ---
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* PROFESSIONAL DARK BACKGROUND */
    .stApp {
        background-color: #0e1117;
        color: #e6edf3; 
        font-family: 'Inter', sans-serif;
    }

    /* CLEAN TITLE - NO GLOW OR GRADIENT SHIFT */
    .clean-title { 
        font-family: 'Inter', sans-serif; 
        font-size: 1.8rem !important; 
        font-weight: 700; 
        text-align: center; 
        color: #ffffff;
        margin-bottom: 25px; 
        letter-spacing: -0.5px;
    }

    /* Professional UI Cards */
    div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] { 
        background: #161b22 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 8px !important; 
        padding: 20px !important; 
        transition: 0.2s ease-in-out; 
    }
    div[data-testid="stFileUploader"]:hover, div[data-testid="stCameraInput"]:hover { 
        border-color: #58a6ff !important; 
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #30363d; }
    .stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; font-size: 0.95rem; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: #1f6feb26 !important; border: 1px solid #1f6feb !important; border-bottom: none !important; color: #58a6ff !important; border-radius: 6px 6px 0 0; }

    /* Stats & Results HUD */
    .stats-hud { display: flex; justify-content: space-between; background: #161b22; border: 1px solid #30363d; border-left: 4px solid #58a6ff; padding: 12px 18px; margin: 15px 0; font-size: 0.95rem; border-radius: 6px; }
    
    /* Subtle Signature */
    .stealth-sig { text-align: right; font-size: 0.75rem; color: #8b949e; margin-top: 40px; padding-right: 5px; user-select: none; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown('<div class="clean-title">AI Face Detection Web Model by Alok and Akash</div>', unsafe_allow_html=True)

# --- MODEL LOADING LOGIC ---
if not os.path.exists("best.pt"):
    st.error("[SYSTEM HALT] 'best.pt' weights missing from repository.")
    st.stop()

@st.cache_resource
def load_yolo():
    return YOLO("best.pt")

try:
    model = load_yolo()
except Exception as e:
    st.error(f"[KERNEL PANIC] {e}")
    st.stop()

# --- CONFIDENCE SLIDER ---
st.markdown("<span style='font-family: \"Inter\"; font-weight: 500; font-size: 0.9rem; color: #8b949e;'>Confidence Threshold</span>", unsafe_allow_html=True)
confidence = st.slider("", min_value=0.1, max_value=1.0, value=0.35, step=0.05, label_visibility="collapsed")

# --- INPUT TABS ---
tab_file, tab_cam = st.tabs(["Upload Image", "Camera Capture"])

input_image = None

with tab_file:
    uploaded = st.file_uploader("Mount Image File", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        input_image = Image.open(uploaded).convert("RGB")

with tab_cam:
    captured = st.camera_input("Access Optic Sensor", label_visibility="collapsed")
    if captured:
        input_image = Image.open(captured).convert("RGB")

# --- PREDICTION & DISPLAY ---
if input_image is not None:
    with st.spinner("Processing image..."):
        results = model.predict(source=input_image, conf=confidence, verbose=False)
        annotated_array = results[0].plot()
        output_image = Image.fromarray(annotated_array[..., ::-1])
        detected = len(results[0].boxes)
        
        st.markdown(
            f"""
            <div class="stats-hud">
                <span style="color: #8b949e;">Faces Detected:</span>
                <span style="color: #58a6ff; font-weight: 600;">{detected}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.image(output_image, use_container_width=True)

st.markdown('<div class="stealth-sig">loki</div>', unsafe_allow_html=True)
