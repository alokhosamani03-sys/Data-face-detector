import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import os

# Page Configuration
st.set_page_config(
    page_title="CyberVision Lab | Alok & Akash",
    page_icon="⚡",
    layout="centered"
)

# Custom Cyberpunk & Animated Sci-Fi HUD Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Body & Animated Cyber Grid Background */
    .stApp {
        background: 
            radial-gradient(circle at 50% 10%, rgba(0, 240, 255, 0.12), transparent 45%),
            radial-gradient(circle at 85% 90%, rgba(121, 40, 202, 0.18), transparent 50%),
            linear-gradient(180deg, #030712 0%, #080d1a 50%, #030712 100%),
            linear-gradient(rgba(0, 240, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.04) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px;
        background-position: center, center, center, center center, center center;
        color: #E2E8F0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Keyframe Animations */
    @keyframes neonFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes radarPulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.7); }
        70% { box-shadow: 0 0 0 14px rgba(0, 240, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
    }

    @keyframes laserSweep {
        0% { top: 0%; opacity: 0.8; }
        50% { opacity: 1; }
        100% { top: 96%; opacity: 0.8; }
    }

    @keyframes holoFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
    }

    /* Animated Dynamic Title */
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.85rem !important;
        font-weight: 800;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #00F0FF, #7000FF, #FF007A, #00F0FF);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neonFlow 5s linear infinite;
        margin-bottom: 4px;
        padding-top: 8px;
    }

    .cyber-subtitle {
        font-family: 'JetBrains Mono', monospace;
        text-align: center;
        color: #00F0FF;
        font-size: 0.78rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        opacity: 0.85;
        margin-bottom: 24px;
    }

    /* Live HUD Status Card */
    .hud-panel {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(10, 18, 38, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 12px;
        padding: 14px 22px;
        margin-bottom: 20px;
        animation: holoFloat 4s ease-in-out infinite;
        box-shadow: 0 8px 32px rgba(0, 240, 255, 0.1);
    }

    .status-beacon {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #00F0FF;
        border-radius: 50%;
        margin-right: 8px;
        animation: radarPulse 2s infinite;
    }

    /* Glowing Animated Cards for Upload & Camera */
    div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
        background: rgba(10, 18, 38, 0.6) !important;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 240, 255, 0.25) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        transition: all 0.35s ease;
        position: relative;
    }

    div[data-testid="stFileUploader"]:hover, div[data-testid="stCameraInput"]:hover {
        border-color: #00F0FF !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.28);
        transform: scale(1.01);
    }

    /* Sci-Fi Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        justify-content: center;
        border-bottom: 1px solid rgba(0, 240, 255, 0.15);
        padding-bottom: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', sans-serif;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 8px;
        color: #94A3B8;
        padding: 8px 20px;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.2), rgba(112, 0, 255, 0.3)) !important;
        border-color: #00F0FF !important;
        color: #00F0FF !important;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.4);
    }

    /* Result Target Counter */
    .target-box {
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.12), rgba(112, 0, 255, 0.2));
        border: 1px solid #00F0FF;
        border-radius: 10px;
        padding: 12px 18px;
        margin: 18px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }

    /* Scanning Overlay Laser Bar */
    .scanner-container {
        position: relative;
        overflow: hidden;
        border-radius: 12px;
        border: 1px solid rgba(0, 240, 255, 0.4);
    }

    .scanner-laser {
        position: absolute;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00F0FF, #FFFFFF, #00F0FF, transparent);
        box-shadow: 0 0 15px #00F0FF, 0 0 25px #00F0FF;
        animation: laserSweep 2.5s ease-in-out infinite alternate;
        z-index: 10;
        pointer-events: none;
    }

    /* Tiny Stealth Signature */
    .stealth-sig {
        text-align: right;
        font-size: 0.55rem;
        font-family: 'JetBrains Mono', monospace;
        color: rgba(0, 240, 255, 0.3);
        letter-spacing: 2px;
        margin-top: 45px;
        padding-right: 5px;
        user-select: none;
    }

    /* Hide Default Chrome */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Cyber Header
st.markdown('<div class="cyber-title">Ai face detection web model by Alok and Akash</div>', unsafe_allow_html=True)
st.markdown('<div class="cyber-subtitle">// NEURAL ENGINE ONLINE • YOLOV8 ARCHITECTURE //</div>', unsafe_allow_html=True)

# Status HUD Panel
st.markdown("""
<div class="hud-panel">
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; display: flex; align-items: center;">
        <span class="status-beacon"></span>CORE STATUS: READY
    </div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #00F0FF;">
        LATENCY: &lt;15ms
    </div>
</div>
""", unsafe_allow_html=True)

# Model Loader
if not os.path.exists("best.pt"):
    st.error("Model weights file 'best.pt' was not found in repository root.")
    st.stop()

@st.cache_resource
def load_yolo():
    return YOLO("best.pt")

try:
    model = load_yolo()
except Exception as err:
    st.error(f"Inference engine failure: {err}")
    st.stop()

# Controls
confidence = st.slider("TARGET CONFIDENCE SENSITIVITY", min_value=0.1, max_value=1.0, value=0.35, step=0.05)

# Input Tabs
tab_gallery, tab_live = st.tabs(["[ ⚡ GALLERY FEED ]", "[ 📷 LIVE SENSOR ]"])

input_image = None

with tab_gallery:
    uploaded = st.file_uploader("Upload Frame", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        input_image = Image.open(uploaded).convert("RGB")

with tab_live:
    captured = st.camera_input("Capture Frame", label_visibility="collapsed")
    if captured:
        input_image = Image.open(captured).convert("RGB")

# Detection Pipeline
if input_image is not None:
    with st.spinner("RUNNING NEURAL PASS..."):
        results = model.predict(source=input_image, conf=confidence, verbose=False)
        annotated_array = results[0].plot()
        output_image = Image.fromarray(annotated_array[..., ::-1])
        
        detected_count = len(results[0].boxes)
        
        # Result HUD
        st.markdown(
            f"""
            <div class="target-box">
                <div>DETECTION STATUS: <span style="color:#00F0FF; font-weight:700;">PROCESSED</span></div>
                <div>FACES IDENTIFIED: <span style="color:#00F0FF; font-weight:700; font-size:1.1rem;">[{detected_count}]</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Laser-scanned Output Image
        st.markdown('<div class="scanner-container"><div class="scanner-laser"></div>', unsafe_allow_html=True)
        st.image(output_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Micro Signature
st.markdown('<div class="stealth-sig">loki</div>', unsafe_allow_html=True)
