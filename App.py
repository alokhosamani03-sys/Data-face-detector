import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import os

# Page configuration
st.set_page_config(
    page_title="AI Vision Lab | Alok & Akash",
    page_icon="💠",
    layout="centered"
)

# Custom High-End Futuristic & Cyber Glassmorphic Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Background Setup */
    .stApp {
        background: linear-gradient(135deg, rgba(8, 12, 22, 0.90) 0%, rgba(13, 20, 36, 0.94) 100%),
                    url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #E2E8F0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Animated Header */
    @keyframes textGlow {
        0%, 100% { filter: drop-shadow(0 0 12px rgba(0, 240, 255, 0.45)); }
        50% { filter: drop-shadow(0 0 24px rgba(121, 40, 202, 0.7)); }
    }

    .main-title {
        font-size: 2.1rem !important;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #00F0FF, #7000FF, #FF007A);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textGlow 4s ease-in-out infinite;
        margin-bottom: 2px;
        padding-top: 10px;
        letter-spacing: -0.5px;
    }

    .sub-title {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 28px;
    }

    /* Glassmorphism Containers */
    div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 240, 255, 0.18) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    div[data-testid="stFileUploader"]:hover, div[data-testid="stCameraInput"]:hover {
        border-color: rgba(0, 240, 255, 0.5) !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.15);
        transform: translateY(-2px);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        justify-content: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        color: #94A3B8;
        padding: 8px 18px;
        font-size: 0.9rem;
        transition: all 0.25s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(112, 0, 255, 0.25)) !important;
        border-color: #00F0FF !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.25);
    }

    /* Detection Counter Pill */
    .hud-badge {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(10, 25, 47, 0.85);
        border-left: 3px solid #00F0FF;
        border-radius: 8px;
        padding: 12px 18px;
        margin: 16px 0;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.06);
    }

    .hud-badge span {
        color: #00F0FF;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Micro Signature */
    .stealth-sig {
        text-align: right;
        font-size: 0.55rem;
        font-family: 'JetBrains Mono', monospace;
        color: rgba(148, 163, 184, 0.28);
        letter-spacing: 2px;
        text-transform: lowercase;
        margin-top: 50px;
        padding-right: 8px;
        user-select: none;
    }

    /* Hide Streamlit Native Overlays */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Custom Header Section
st.markdown('<div class="main-title">Ai face detection web model by Alok and Akash</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Neural Engine • YOLOv8 Vision Architecture</div>', unsafe_allow_html=True)

# Model Loader
if not os.path.exists("best.pt"):
    st.error("Model weights ('best.pt') missing in root repository.")
    st.stop()

@st.cache_resource
def load_yolo():
    return YOLO("best.pt")

try:
    model = load_yolo()
except Exception as err:
    st.error(f"Engine initialization fault: {err}")
    st.stop()

# Controls
confidence = st.slider("Detection Sensitivity (Confidence)", min_value=0.1, max_value=1.0, value=0.35, step=0.05)

# Selection Interface
tab_upload, tab_camera = st.tabs(["[ 📁 Gallery Upload ]", "[ 📸 Neural Camera ]"])

input_image = None

with tab_upload:
    uploaded = st.file_uploader("Select high-res image source", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        input_image = Image.open(uploaded).convert("RGB")

with tab_camera:
    captured = st.camera_input("Capture sensor frame", label_visibility="collapsed")
    if captured:
        input_image = Image.open(captured).convert("RGB")

# Inference Pipeline
if input_image is not None:
    with st.spinner("Processing neural inference..."):
        results = model.predict(source=input_image, conf=confidence, verbose=False)
        annotated_array = results[0].plot()
        output_image = Image.fromarray(annotated_array[..., ::-1])
        
        detected_count = len(results[0].boxes)
        
        # HUD Output display
        st.markdown(
            f"""
            <div class="hud-badge">
                <div>SYSTEM STATUS: <span style="color:#22c55e;">ONLINE</span></div>
                <div>FACES RECOGNIZED: <span>{detected_count}</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.image(output_image, use_container_width=True)

# Micro Signature
st.markdown('<div class="stealth-sig">loki</div>', unsafe_allow_html=True)
