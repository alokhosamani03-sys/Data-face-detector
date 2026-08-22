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

# 1. CSS STYLES
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;600;700&display=swap');

    .stApp {
        background: linear-gradient(rgba(4, 9, 20, 0.70), rgba(4, 9, 20, 0.95)),
                    url('https://images.unsplash.com/photo-1531746790731-6c087fecd65a?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center top; background-attachment: fixed;
        color: #e0f2fe; font-family: 'Rajdhani', sans-serif;
    }

    .cyber-particles { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 999; pointer-events: none; overflow: hidden; }
    .particle { position: absolute; font-family: 'Share Tech Mono', monospace; font-weight: bold; color: rgba(0, 255, 255, 0.5); text-shadow: 0 0 10px rgba(0, 255, 255, 0.8); animation: fall linear infinite; }

    .p1 { left: 10%; font-size: 1.2rem; animation-duration: 12s; animation-delay: 0s; }
    .p2 { left: 30%; font-size: 1.5rem; animation-duration: 8s; animation-delay: 2s; color: rgba(255, 0, 122, 0.6); text-shadow: 0 0 10px #FF007A; }
    .p3 { left: 50%; font-size: 2.2rem; animation-duration: 15s; animation-delay: 1s; }
    .p4 { left: 70%; font-size: 1.1rem; animation-duration: 10s; animation-delay: 5s; }
    .p5 { left: 85%; font-size: 1.8rem; animation-duration: 11s; animation-delay: 3s; color: rgba(112, 0, 255, 0.6); }

    .roam-box { position: absolute; width: 120px; height: 120px; border: 2px dashed rgba(0, 255, 255, 0.3); border-radius: 8px; display: flex; justify-content: center; align-items: center; font-family: 'Share Tech Mono', monospace; color: rgba(0, 255, 255, 0.2); font-size: 1rem; box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.1); animation: roam 18s ease-in-out infinite alternate; }
    .roam-box-2 { position: absolute; width: 80px; height: 80px; border: 2px solid rgba(255, 0, 122, 0.2); animation: roam2 25s ease-in-out infinite alternate-reverse; color: rgba(255, 0, 122, 0.2); }

    .roam-box::after, .roam-box-2::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: rgba(0, 255, 255, 0.7); box-shadow: 0 0 10px rgba(0, 255, 255, 0.8); animation: internal-scan 2s linear infinite; }
    .roam-box-2::after { background: rgba(255, 0, 122, 0.7); box-shadow: 0 0 10px rgba(255, 0, 122, 0.8); }

    @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { transform: translateY(110vh) rotate(15deg); opacity: 0; } }
    @keyframes roam { 0% { top: 10%; left: 5%; transform: scale(1); border-color: rgba(0,255,255,0.3); color: rgba(0,255,255,0.2); } 30% { top: 60%; left: 30%; transform: scale(1.2); } 50% { border-color: #00FFFF; color: #00FFFF; box-shadow: 0 0 30px rgba(0,255,255,0.4); text-shadow: 0 0 10px #00FFFF; } 70% { top: 20%; left: 70%; transform: scale(0.8); border-color: rgba(0,255,255,0.3); color: rgba(0,255,255,0.2); } 100% { top: 80%; left: 85%; transform: scale(1.1); } }
    @keyframes roam2 { 0% { top: 80%; left: 10%; transform: scale(1.5) rotate(-10deg); } 40% { top: 30%; left: 60%; transform: scale(1) rotate(0deg); border-color: #FF007A; color: #FF007A; box-shadow: 0 0 30px rgba(255,0,122,0.4); } 100% { top: 15%; left: 80%; transform: scale(0.9) rotate(10deg); } }
    @keyframes internal-scan { 0% { top: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 95%; opacity: 0; } }
    @keyframes floatHolo { 0%, 100% { transform: translateY(0px); box-shadow: 0 5px 15px rgba(0, 255, 255, 0.1); } 50% { transform: translateY(-6px); box-shadow: 0 15px 25px rgba(0, 255, 255, 0.3); } }

    .cyber-title { font-family: 'Share Tech Mono', monospace; font-size: 1.8rem !important; font-weight: 700; text-align: center; color: #fff; text-transform: uppercase; text-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF; margin-bottom: 5px; letter-spacing: -0.5px; }
    .cyber-subtitle { text-align: center; font-family: 'Share Tech Mono', monospace; color: #7000FF; font-size: 0.9rem; margin-bottom: 30px; text-shadow: 0 0 5px #7000FF; }

    div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] { background: rgba(4, 9, 20, 0.7) !important; border: 1px solid rgba(0, 255, 255, 0.3) !important; border-radius: 4px !important; box-shadow: inset 0 0 20px rgba(0,255,255,0.05); padding: 20px !important; transition: 0.3s all; position: relative; z-index: 10; }
    div[data-testid="stFileUploader"]:hover, div[data-testid="stCameraInput"]:hover { border-color: #00FFFF !important; box-shadow: inset 0 0 30px rgba(0,255,255,0.2), 0 0 15px rgba(0,255,255,0.4); }

    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #334155; }
    .stTabs [data-baseweb="tab"] { font-family: 'Share Tech Mono', monospace; background: transparent; color: #64748b; }
    .stTabs [aria-selected="true"] { background: rgba(0, 255, 255, 0.1) !important; border: 1px solid #00FFFF !important; border-bottom: none !important; color: #00FFFF !important; }

    .scanner-box { position: relative; overflow: hidden; border: 2px solid #00FFFF; padding: 2px; animation: floatHolo 4s ease-in-out infinite; z-index: 10; }
    .laser-line { position: absolute; top: 0; left: 0; right: 0; height: 2px; background: #00FFFF; box-shadow: 0 0 15px 5px rgba(0, 255, 255, 0.6); animation: scan 2s linear infinite alternate; z-index: 50; }
    @keyframes scan { 0% { top: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 98%; opacity: 0; } }

    .stats-hud { display: flex; justify-content: space-between; background: rgba(0, 0, 0, 0.6); border-left: 4px solid #FF007A; padding: 10px 15px; margin: 15px 0; font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; }
    .stealth-sig { text-align: right; font-size: 0.5rem; font-family: 'Share Tech Mono', monospace; color: rgba(255, 255, 255, 0.15); margin-top: 50px; padding-right: 2px; user-select: none; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 2. HTML ANIMATIONS (Notice how there are zero spaces on the left here)
st.markdown("""
<div class="cyber-particles">
<div class="roam-box">[■_■]</div>
<div class="roam-box roam-box-2">[TARGET]</div>
<div class="particle p1">[0_0] SCAN</div>
<div class="particle p2">&lt;FACE_DETECT/&gt;</div>
<div class="particle p3">[-_-]</div>
<div class="particle p4">YOLOv8_VISION</div>
<div class="particle p5">[👁️_👁️]</div>
</div>
""", unsafe_allow_html=True)

# 3. APP LOGIC
st.markdown('<div class="cyber-title">Ai face detection web model by Alok and Akash</div>', unsafe_allow_html=True)
st.markdown('<div class="cyber-subtitle">[ NEURAL NETWORK PROCESSING NODE ]</div>', unsafe_allow_html=True)

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

st.markdown("<span style='font-family: \"Share Tech Mono\"; color: #00F0FF; position: relative; z-index: 10;'>[CONFIDENCE_THRESHOLD]</span>", unsafe_allow_html=True)
confidence = st.slider("", min_value=0.1, max_value=1.0, value=0.35, step=0.05, label_visibility="collapsed")

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

if input_image is not None:
    with st.spinner("EXECUTING NEURAL SCAN..."):
        results = model.predict(source=input_image, conf=confidence, verbose=False)
        annotated_array = results[0].plot()
        output_image = Image.fromarray(annotated_array[..., ::-1])
        detected = len(results[0].boxes)
        
        st.markdown(
            f"""
            <div class="stats-hud">
                <span style="color: #FF007A;">> TARGETS_LOCKED:</span>
                <span style="color: #00FFFF; font-weight: bold;">[{detected}]</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown('<div class="scanner-box"><div class="laser-line"></div>', unsafe_allow_html=True)
        st.image(output_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="stealth-sig">loki</div>', unsafe_allow_html=True)
