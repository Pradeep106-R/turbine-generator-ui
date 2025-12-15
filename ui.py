import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# --- CONFIGURATION ---
API_URL = "https://tania-unirritable-venturously.ngrok-free.dev/generate"
API_KEY = "TURBINE-SECRET-999"

st.set_page_config(page_title="HCL Turbine Inspector AI", layout="wide")

# Initialize Session State for images so they persist
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []

st.title("🎨 Turbine Blade Image Generator")
st.write("Professional Industrial AI Imaging Suite")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Generation Settings")
    user_prompt = st.text_area("Detailed Prompt", "Industrial photography of a turbine blade, high detail, minor surface rust")
    image_count = st.slider("Number of Images", 1, 20, 1)
    
    st.divider()
    st.subheader("⚙️ Advanced Settings")
    gen_steps = st.slider("Inference Steps", 10, 50, 20)
    gen_guidance = st.slider("Guidance Scale", 1.0, 15.0, 7.5, 0.5)
    
    st.divider()
    generate_btn = st.button("🚀 Generate Images", type="primary")

# --- GENERATION LOGIC ---
if generate_btn:
    with st.spinner(f"Processing {image_count} image(s)..."):
        try:
            payload = {
                "prompt": user_prompt,
                "num_images": image_count,
                "steps": gen_steps,
                "guidance_scale": gen_guidance
            }
            headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=2000)
            
            if response.status_code == 200:
                # Save the new results to session state
                st.session_state.generated_images = response.json()["outputs"]
                st.success(f"✅ {len(st.session_state.generated_images)} images generated!")
            else:
                st.error(f"Backend Error: {response.text}")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

# --- DISPLAY LOGIC (Always runs) ---
# This part stays visible even after clicking download buttons
if st.session_state.generated_images:
    cols_per_row = 3
    results = st.session_state.generated_images
    
    for i in range(0, len(results), cols_per_row):
        row_images = results[i : i + cols_per_row]
        cols = st.columns(cols_per_row)
        
        for idx, img_b64 in enumerate(row_images):
            global_idx = i + idx
            with cols[idx]:
                img_bytes = base64.b64decode(img_b64)
                st.image(img_bytes, caption=f"Result {global_idx+1}", use_container_width=True)
                
                # Download button now uses "on_click=None" behavior implicitly
                # but because data is in session_state, it won't vanish.
                st.download_button(
                    label=f"💾 Download #{global_idx+1}",
                    data=img_bytes,
                    file_name=f"turbine_{global_idx+1}.png",
                    mime="image/png",
                    key=f"dl_{global_idx}"
                )
