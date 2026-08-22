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

# Core Cyberpunk Engine & Falling/Floating Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;600;700&display=swap');

    /* Global styling and background image */
    .stApp {
        background: linear-gradient(rgba(4, 9, 20, 0.9), rgba(4, 9, 20, 0.95)),
                    url('https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #e0f2fe;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Fixed container for flying/falling cyber elements */
    .cyber-particles {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        overflow: hidden;
        pointer-events: none; /* Allows clicking through the animations */
    }

    /* Base styling for falling elements */
    .particle {
        position: absolute;
        font-family: 'Share Tech Mono', monospace;
        color: rgba(0, 240, 255, 0.25);
        user-select: none;
        animation: fall linear infinite;
        text-shadow: 0 0 5px rgba(0, 240, 255, 0.3);
    }

    /* Individual element physics (Speed, size, rotation) */
    .p1 { left: 5%; font-size: 1.2rem; animation-duration: 12s; animation-delay: 0s; }
    .p2 { left: 20%; font-size: 0.9rem; animation-duration: 8s; animation-delay: 3s; color: rgba(112, 0, 255, 0.3); }
    .p3 { left: 35%; font-size: 1.5rem; animation-duration: 15s; animation-delay: 1s; }
    .p4 { left: 50%; font-size: 1rem; animation-duration: 10s; animation-delay: 5s; }
    .p5 { left: 65%; font-size: 2rem; animation-duration: 18s; animation-delay: 2s; color: rgba(255, 0, 122, 0.2); }
    .p6 { left: 80%; font-size: 1.1rem; animation-duration: 9s; animation-delay: 4s; }
    .p7 { left: 90%; font-size: 1.3rem; animation-duration: 14s; animation-delay: 0.5s; }

    /* The Falling Keyframe */
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }

    /* Floating Keyframe for HUD */
    @keyframes floatHolo {
        0%, 100% { transform: translateY(0px); box-shadow: 0 5px 15px rgba(0, 240, 255, 0.1); }
        50% { transform: translateY(-6px); box-shadow: 0 15px 25px rgba(0, 240, 255, 0.25); }
    }

    /* Title Styling */
    .cyber-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.8rem !important;
        font-weight: 700;
        text-align: center;
        color: #fff;
        text-transform: uppercase;
        text-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF, 0 0 40px #00F0FF;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    
    .cyber-subtitle {
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        color: #7000FF;
        font-size: 0.9rem;
        margin-bottom: 30px;
        text-shadow: 0 0 5px #7000FF;
    }

    /* Interactive Upload/Camera Cards */
    div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
        background: rgba(4, 9, 20, 0.7) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 4px !important;
        box-shadow: inset 0 0 20px rgba(0,240,255,0.05);
        padding: 20px !important;
        transition: 0.3s all;
    }
    div[data-testid="stFileUploader"]:hover, div[data-testid="stCameraInput"]:hover {
        border-color: #00F0FF !important;
        box-shadow: inset 0 0 30px rgba(0,240,255,0.15), 0 0 15px rgba(0,240,255,0.3);
    }

    /* Tech-style Tabs */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Share Tech Mono', monospace;
        background: transparent;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0, 240, 255, 0.1) !important;
        border: 1px solid #00F0FF !important;
        border-bottom: none !important;
        color: #00F0FF !important;
    }

    /* Scanner Animation */
    .scanner-box {
        position: relative;
        overflow: hidden;
        border: 2px solid #00F0FF;
        padding: 2px;
        animation: floatHolo 4s ease-in-out infinite;
    }
    .laser-line {
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: #00F0FF;
        box-shadow: 0 0 15px 5px rgba(0, 240, 255, 0.5);
        animation: scan 2s linear infinite alternate;
        z-index: 50;
    }
    @keyframes scan {
        0% { top: 0%; opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { top: 98%; opacity: 0; }
    }

    /* HUD Output Stats */
    .stats-hud {
        display: flex;
        justify-content: space-between;
        background: rgba(0, 0, 0, 0.6);
        border-left: 4px solid #FF007A;
        padding: 10px 15px;
        margin: 15px 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem;
    }

    /* Stealth Signature */
    .stealth-sig {
        text-align: right;
        font-size: 0.5rem;
        font-family: 'Share Tech Mono', monospace;
        color: rgba(255, 255, 255, 0.15);
        margin-top: 50px;
        padding-right: 2px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>

<!-- Injecting the falling tech elements -->
<div class="cyber-particles">
    <div class="particle p1">01101001</div>
    <div class="particle p2">&lt;SYS_OVERRIDE/&gt;</div>
    <div class="particle p3">♦</div>
    <div class="particle p4">YOLOv8_VISION</div>
    <div class="particle p5">[0xFF]</div>
    <div class="particle p6">ERROR_404</div>
    <div class="particle p7">101101</div>
</div>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="cyber-title">Ai face detection web model by Alok and Akash</div>', unsafe_allow_html=True)
st.markdown('<div class="cyber-subtitle">[ NEURAL NETWORK PROCESSING NODE ]</div>', unsafe_allow_html=True)

# Load Model Safety Check
if not os.path.exists("best.pt"):
    st.error("[SYSTEM HALT] 'best.pt' weights missing from memory banks.")
    st.stop()

@st.cache_resource
def load_yolo():
    return YOLO("best.pt")

try:
    model = load_yolo()
except Exception as e:
    st.error(f"[KERNEL PANIC] {e}")
    st.stop()

# Controls
st.markdown("<span style='font-family: \"Share Tech Mono\"; color: #00F0FF;'>[CONFIDENCE_THRESHOLD]</span>", unsafe_allow_html=True)
confidence = st.slider("", min_value=0.1, max_value=1.0, value=0.35, step=0.05, label_visibility="collapsed")

# Cyber Tabs
tab_file, tab_cam = st.tabs(["<UPLOAD_DRIVE>", "<INITIATE_CAMERA>"])

input_image = None

with tab_file:
    uploaded = st.file_uploader("Mount Image File", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        input_image = Image.open(uploaded).convert("RGB")

with tab_cam:
    captured = st.camera_input("Access Optic Sensor", label_visibility="collapsed")
    if captured:
        input_image = Image.open(captured).convert("RGB")

# YOLO Inference
if input_image is not None:
    with st.spinner("EXECUTING NEURAL SCAN..."):
        results = model.predict(source=input_image, conf=confidence, verbose=False)
        annotated_array = results[0].plot()
        output_image = Image.fromarray(annotated_array[..., ::-1])
        detected = len(results[0].boxes)
        
        # Stats HUD Output
        st.markdown(
            f"""
            <div class="stats-hud">
                <span style="color: #FF007A;">> TARGETS_LOCKED:</span>
                <span style="color: #00F0FF; font-weight: bold;">[{detected}]</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display Image with Laser Scanner wrap
        st.markdown('<div class="scanner-box"><div class="laser-line"></div>', unsafe_allow_html=True)
        st.image(output_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Small Loki Signature
st.markdown('<div class="stealth-sig">loki</div>', unsafe_allow_html=True)
