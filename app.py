"""ImageMotion - Video Generator from Image

A Streamlit application that transforms static images into dynamic animated videos.
"""

import streamlit as st
import os
import time
import tempfile
from datetime import datetime
from PIL import Image

from utils.effects import EFFECT_OPTIONS, EFFECT_MAP
from utils.video_generator import generate_video

# Page configuration
st.set_page_config(
    page_title="ImageMotion - Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    :root {
        --primary: #6366F1;
        --secondary: #8B5CF6;
        --accent: #EC4899;
        --bg-dark: #0F0F23;
        --surface: #1A1A2E;
        --surface-light: #25253D;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --success: #10B981;
        --border: #374151;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #0F0F23 50%, #1A1A2E 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .header {
        text-align: center;
        padding: 2rem 0;
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }
    
    .upload-area {
        border: 2px dashed var(--border);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        background: var(--surface);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-area:hover {
        border-color: var(--primary);
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.2);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .upload-text {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    .preview-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.15);
    }
    
    .preview-title {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .controls-card {
        background: var(--surface);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.15);
    }
    
    .control-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:disabled {
        opacity: 0.5;
        transform: none;
        box-shadow: none;
    }
    
    .success-message {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid var(--success);
        border-radius: 12px;
        padding: 1rem;
        color: var(--success);
        text-align: center;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    .format-badge {
        display: inline-block;
        background: var(--surface-light);
        color: var(--text-secondary);
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        font-size: 0.75rem;
        margin: 0.25rem;
    }
    
    .stSelectbox > div > div {
        background: var(--surface-light);
        border-color: var(--border);
        border-radius: 12px;
    }
    
    .stSlider > div > div > div {
        background: var(--surface-light);
    }
    
    .stSlider label {
        color: var(--text-primary);
    }
    
    div[data-testid="stExpander"] {
        background: var(--surface);
        border-radius: 12px;
    }
    
    .thumbnail-container {
        background: var(--bg-dark);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 200px;
    }
    
    .thumbnail-container img {
        max-width: 100%;
        max-height: 300px;
        border-radius: 8px;
    }
    
    video {
        border-radius: 12px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Initialize session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'output_video' not in st.session_state:
        st.session_state.output_video = None
    if 'is_generating' not in st.session_state:
        st.session_state.is_generating = False
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🎬 ImageMotion</h1>
        <p>Transform static images into dynamic videos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<p class="preview-title">📤 Upload Image</p>', unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Supported formats: PNG, JPG, WEBP (max 10MB)",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            
            # Display image preview
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            
            # Preview section
            st.markdown('<div class="thumbnail-container">', unsafe_allow_html=True)
            st.image(image, caption=f"📷 {uploaded_file.name}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"<p style='color: var(--text-secondary); font-size: 0.875rem; margin-top: 0.5rem;'>"
                       f"📐 {image.width} × {image.height}px | "
                       f"{uploaded_file.size / 1024:.1f} KB</p>", unsafe_allow_html=True)
        
        # Format badges when no file
        if uploaded_file is None:
            st.markdown("""
            <div class="upload-area">
                <div class="upload-icon">☁️</div>
                <p class="upload-text">Drop your image here or click to browse</p>
                <div style="margin-top: 1rem;">
                    <span class="format-badge">PNG</span>
                    <span class="format-badge">JPG</span>
                    <span class="format-badge">WEBP</span>
                    <span class="format-badge">Max 10MB</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="preview-title">🎥 Generated Video</p>', unsafe_allow_html=True)
        
        # Video preview area
        if st.session_state.output_video and os.path.exists(st.session_state.output_video):
            st.video(st.session_state.uploaded_file, format="video/mp4")
            
            # Download button
            with open(st.session_state.output_video, 'rb') as f:
                video_data = f.read()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="⬇️ Download Video",
                data=video_data,
                file_name=f"imagemotion_{timestamp}.mp4",
                mime="video/mp4",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div class="thumbnail-container" style="flex-direction: column; gap: 1rem;">
                <div style="font-size: 3rem;">🎬</div>
                <p style="color: var(--text-secondary);">Generated video will appear here</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Controls section
    st.markdown("<hr style='margin: 2rem 0; border-color: var(--border);'>", unsafe_allow_html=True)
    
    # Animation controls
    st.markdown('<p class="preview-title">⚙️ Animation Settings</p>', unsafe_allow_html=True)
    
    control_col1, control_col2, control_col3 = st.columns(3, gap="large")
    
    with control_col1:
        # Effect selection
        selected_effect = st.selectbox(
            "✨ Effect Type",
            options=EFFECT_OPTIONS,
            index=0,
            help="Choose the animation effect"
        )
        
        # Duration slider
        duration = st.slider(
            "⏱️ Duration",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Video length in seconds"
        )
    
    with control_col2:
        # Zoom level
        zoom_level = st.slider(
            "🔍 Zoom Level",
            min_value=1.0,
            max_value=2.0,
            value=1.2,
            step=0.1,
            help="Maximum zoom intensity"
        )
        
        # FPS selector
        fps = st.selectbox(
            "🎞️ Frame Rate",
            options=[24, 30, 60],
            index=1,
            help="Video frames per second"
        )
    
    with control_col3:
        # Effect preview info
        st.markdown("""
        <div class="controls-card">
            <p style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">
                Current Settings
            </p>
            <ul style="color: var(--text-primary); font-size: 0.875rem; padding-left: 1.25rem; line-height: 1.8;">
                <li>Effect: <span id="effect-name">Ken Burns Zoom In</span></li>
                <li>Duration: <span id="duration-val">3s</span></li>
                <li>Zoom: <span id="zoom-val">1.2x</span></li>
                <li>FPS: <span id="fps-val">30</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    button_col1, button_col2, button_col3 = st.columns([2, 2, 1], gap="large")
    
    with button_col1:
        # Generate button
        generate_disabled = (
            st.session_state.uploaded_file is None or 
            st.session_state.is_generating
        )
        
        if st.button("🚀 Generate Video", disabled=generate_disabled, use_container_width=True):
            if st.session_state.uploaded_file:
                st.session_state.is_generating = True
                st.session_state.progress = 0
                
                # Create progress bar
                progress_bar = st.progress(0, text="Initializing...")
                
                # Save uploaded image to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
                    image = Image.open(st.session_state.uploaded_file)
                    image.save(tmp_img.name)
                    tmp_img_path = tmp_img.name
                
                # Create output temp file
                tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                tmp_output_path = tmp_output.name
                tmp_output.close()
                
                def update_progress(progress):
                    st.session_state.progress = progress
                    progress_bar.progress(progress, text=f"Generating... {int(progress * 100)}%")
                
                # Get effect type
                effect_type = EFFECT_MAP[selected_effect]
                
                # Generate video
                success = generate_video(
                    image_path=tmp_img_path,
                    output_path=tmp_output_path,
                    effect_type=effect_type,
                    duration=duration,
                    zoom_level=zoom_level,
                    fps=fps,
                    progress_callback=update_progress
                )
                
                # Clean up temp input file
                try:
                    os.unlink(tmp_img_path)
                except:
                    pass
                
                progress_bar.progress(100, text="Complete!")
                time.sleep(0.5)
                progress_bar.empty()
                
                if success and os.path.exists(tmp_output_path):
                    st.session_state.output_video = tmp_output_path
                    st.session_state.is_generating = False
                    st.rerun()
                else:
                    st.error("Failed to generate video. Please try again.")
                    st.session_state.is_generating = False
    
    with button_col2:
        # Download button (only show if video exists)
        if st.session_state.output_video and os.path.exists(st.session_state.output_video):
            with open(st.session_state.output_video, 'rb') as f:
                video_data = f.read()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="💾 Download MP4",
                data=video_data,
                file_name=f"imagemotion_{timestamp}.mp4",
                mime="video/mp4",
                use_container_width=True
            )
    
    with button_col3:
        # Reset button
        if st.button("🔄 Reset", use_container_width=True):
            # Clean up temp files
            if st.session_state.output_video and os.path.exists(st.session_state.output_video):
                try:
                    os.unlink(st.session_state.output_video)
                except:
                    pass
            
            st.session_state.uploaded_file = None
            st.session_state.uploaded_image = None
            st.session_state.output_video = None
            st.session_state.is_generating = False
            st.session_state.progress = 0
            st.rerun()
    
    # Footer
    st.markdown("""
    <hr style="margin-top: 3rem; border-color: var(--border);">
    <div class="footer">
        <p>Powered by 🎬 FFmpeg • Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()