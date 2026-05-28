import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import base64
from PIL import Image
import json
from datetime import datetime

load_dotenv(r"C:\Users\Suhama\Desktop\Hackathon\.env")
client = Groq(api_key=os.getenv("GROQ_KEY"))

def analyze_plant(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    image_data = base64.b64encode(image_bytes).decode("utf-8")
    file_type = uploaded_file.type
    
    prompt = """
    Tum ek expert plant pathologist ho Pakistan ke liye.
    Is plant ki image dekho aur yeh batao:
    
    1. PLANT TYPE: Kaun sa plant hai?
    2. HEALTH STATUS: Healthy hai ya bimaar?
    3. DISEASE: Agar bimari hai to kya hai?
    4. SEVERITY: Mild / Moderate / Severe
    5. TREATMENT: Kya karna chahiye? (Pakistani market mein available medicines)
    6. PREVENTION: Future mein kaise bachayein?
    
    Jawab Urdu aur English mix mein do.
    Kisaan samajh sake aisi simple language use karo.
    """
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{file_type};base64,{image_data}"}
                },
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.choices[0].message.content

# ==================
# APP
# ==================
st.set_page_config(
    page_title="Plant Doctor Pakistan",
    page_icon="🌱",
    layout="centered"
)

with st.sidebar:
    st.title("🌱 Plant Doctor")
    st.write("AI-powered plant disease detection")
    st.divider()
    st.write("**Kaise use karein:**")
    st.write("1. Plant ki photo lo")
    st.write("2. Upload karo")
    st.write("3. Diagnose dabao")
    st.write("4. Treatment padhein")
    st.divider()
    st.caption("SE Hackathon 2026")

st.title("🌱 Plant Doctor Pakistan")
st.write("Apne plant ki photo upload karo — AI batayegi kya masla hai!")

uploaded = st.file_uploader(
    "Plant ki photo yahan upload karo:",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(Image.open(uploaded), caption="Tumhari plant", use_column_width=True)
    
    with col2:
        st.metric("File Size", f"{uploaded.size // 1024} KB")
        st.metric("Format", uploaded.type.split("/")[1].upper())
        
        if st.button("🔬 Diagnose Karo!", type="primary", use_container_width=True):
            with st.spinner("AI plant dekh rahi hai... 🔍"):
                try:
                    result = analyze_plant(uploaded)
                    st.session_state.last_result = result
                except Exception as e:
                    st.error(f"Error: {e}")
    
    if "last_result" in st.session_state:
        st.divider()
        st.subheader("📋 Doctor Ki Report:")
        st.markdown(st.session_state.last_result)
        
        if st.button("📥 Report Save Karo"):
            report = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "result": st.session_state.last_result
            }
            try:
                with open("reports.json", "r") as f:
                    reports = json.load(f)
            except:
                reports = []
            reports.append(report)
            with open("reports.json", "w") as f:
                json.dump(reports, f, indent=4)
            st.success("✅ Report save ho gayi!")
else:
    st.info("👆 Upar apni plant ki photo upload karo!")
    
    st.divider()
    st.subheader("🌿 Kaunsi plants detect kar sakta hai?")
    
    plants = st.columns(4)
    plants[0].success("🌾 Wheat\nGandum")
    plants[1].success("🌽 Corn\nMakka")
    plants[2].success("🍅 Tomato\nTamaatar")
    plants[3].success("🌶️ Chilli\nMirch")