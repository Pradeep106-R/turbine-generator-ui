import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# --- CONFIGURATION ---
API_URL = "https://tania-unirritable-venturously.ngrok-free.dev/generate"
API_KEY = "TURBINE-SECRET-999"

st.set_page_config(page_title="HCL Turbine Inspector AI", layout="wide")

st.title("🎨 Turbine Blade Image Generator")
st.write("Professional Industrial AI Imaging Suite")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Generation Settings")
    user_prompt = st.text_area("Detailed Prompt", "Industrial photography of a turbine blade, high detail, minor surface rust")
    
    # Updated: Limit set to 20
    image_count = st.slider("Number of Images", 1, 20, 1)
    
    st.divider()
    st.subheader("⚙️ Advanced Settings")
    # New: Advanced Parameters
    gen_steps = st.slider("Inference Steps", 10, 50, 20, help="Higher = better quality but slower")
    gen_guidance = st.slider("Guidance Scale", 1.0, 15.0, 7.5, 0.5, help="How closely to follow the prompt")
    
    st.divider()
    generate_btn = st.button("🚀 Generate Images", type="primary")

# --- MAIN UI LOGIC ---
if generate_btn:
    with st.spinner(f"Processing {image_count} image(s)... This may take a while for large batches."):
        try:
            payload = {
                "prompt": user_prompt,
                "num_images": image_count,
                "steps": gen_steps,
                "guidance_scale": gen_guidance
            }
            headers = {
                "x-api-key": API_KEY,
                "Content-Type": "application/json"
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=2000)
            
            if response.status_code == 200:
                results = response.json()["outputs"]
                
                # Logic: Display in a grid of 3 columns
                cols_per_row = 3
                for i in range(0, len(results), cols_per_row):
                    row_images = results[i : i + cols_per_row]
                    cols = st.columns(cols_per_row)
                    
                    for idx, img_b64 in enumerate(row_images):
                        global_idx = i + idx
                        with cols[idx]:
                            img_bytes = base64.b64decode(img_b64)
                            st.image(img_bytes, caption=f"Result {global_idx+1}", use_container_width=True)
                            
                            st.download_button(
                                label=f"💾 Download #{global_idx+1}",
                                data=img_bytes,
                                file_name=f"turbine_{global_idx+1}.png",
                                mime="image/png",
                                key=f"dl_{global_idx}"
                            )
                st.success(f"✅ {len(results)} images generated successfully!")
            else:
                st.error(f"Backend Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Connection Failed. Ensure ngrok and main.py are running. Error: {e}")
