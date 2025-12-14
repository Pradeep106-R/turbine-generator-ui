import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# --- CONFIGURATION ---
# Replace with your ACTUAL ngrok URL every time you restart ngrok
API_URL = "https://tania-unirritable-venturously.ngrok-free.dev/generate"
API_KEY = "TURBINE-SECRET-999"

st.set_page_config(page_title="HCL Turbine Inspector AI", layout="wide")

st.title("🎨 Turbine Blade Image Generator")
st.write("Professional Industrial AI Imaging Suite")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Generation Settings")
    user_prompt = st.text_area("Detailed Prompt", "Industrial photography of a turbine blade, high detail, minor surface rust")
    image_count = st.slider("Number of Images to Generate", 1, 4, 1)
    
    st.divider()
    generate_btn = st.button("🚀 Generate Images", type="primary")

# --- MAIN UI LOGIC ---
if generate_btn:
    with st.spinner(f"Requesting {image_count} image(s) from GPU... Please wait."):
        try:
            payload = {
                "prompt": user_prompt,
                "num_images": image_count
            }
            headers = {
                "x-api-key": API_KEY,
                "Content-Type": "application/json"
            }
            
            # Request to your ngrok backend
            response = requests.post(API_URL, headers=headers, json=payload, timeout=600)
            
            if response.status_code == 200:
                results = response.json()["outputs"]
                
                # Create columns for the images
                cols = st.columns(len(results))
                
                for idx, img_b64 in enumerate(results):
                    with cols[idx]:
                        # Decode and show image
                        img_bytes = base64.b64decode(img_b64)
                        st.image(img_bytes, caption=f"Generation {idx+1}", use_container_width=True)
                        
                        # Individual download button
                        st.download_button(
                            label=f"💾 Download #{idx+1}",
                            data=img_bytes,
                            file_name=f"turbine_image_{idx+1}.png",
                            mime="image/png",
                            key=f"dl_{idx}"
                        )
                st.success("✅ All images generated successfully!")
            else:
                st.error(f"Backend Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Connection Failed. Is ngrok running? Error: {e}")