import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import base64
from PIL import Image

load_dotenv(r"C:\Users\Suhama\Desktop\Hackathon\.env")
client = Groq(api_key=os.getenv("GROQ_KEY"))

def analyze_image(uploaded_file, question):
    # File bytes lo
    image_bytes = uploaded_file.getvalue()
    image_data = base64.b64encode(image_bytes).decode("utf-8")
    
    # Format nikalo
    file_type = uploaded_file.type  # image/jpeg ya image/png
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{file_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )
    
    return response.choices[0].message.content

# ==================
# PAGE CONFIG
# ==================
st.set_page_config(
    page_title="AI Image Analyzer",
    page_icon="👁️",
    layout="wide"
)

st.title("👁️ AI Image Analyzer")
st.caption("Koi bhi image upload karo — AI batayegi!")

# ==================
# SIDEBAR — Mode Select
# ==================
with st.sidebar:
    st.title("⚙️ Settings")
    
    mode = st.selectbox(
        "Mode choose karo:",
        [
            "🔍 General Analysis",
            "🌱 Plant Doctor",
            "🍕 Food Identifier",
            "📊 Chart/Graph Reader",
            "📝 Text Reader (OCR)",
            "❓ Custom Question"
        ]
    )
    
    st.divider()
    st.caption("Supported: JPG, PNG, JPEG")

# ==================
# MAIN CONTENT
# ==================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Image Upload")
    uploaded_file = st.file_uploader(
        "Image upload karo",
        type=["jpg", "jpeg", "png"],
        help="JPG ya PNG image select karo"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Tumhari image", use_column_width=True)

with col2:
    st.subheader("🤖 AI Analysis")
    
    if uploaded_file:
        # Mode ke hisaab se question
        if mode == "🔍 General Analysis":
            question = "Is image mein kya hai? Detail mein batao. Urdu aur English mix mein jawab do."
        elif mode == "🌱 Plant Doctor":
            question = "Is plant mein koi bimari ya problem hai? Kya diagnosis hai aur kya treatment honi chahiye? Urdu/English mein batao."
        elif mode == "🍕 Food Identifier":
            question = "Yeh kaunsa khana hai? Ingredients kya hain? Approximate calories batao. Urdu/English mein."
        elif mode == "📊 Chart/Graph Reader":
            question = "Is chart ya graph mein kya data hai? Key insights kya hain? English mein explain karo."
        elif mode == "📝 Text Reader (OCR)":
            question = "Is image mein jo bhi text hai woh extract karke do. Exact text likho."
        else:  # Custom
            question = st.text_area(
                "Apna sawaal likho:",
                placeholder="Is image ke bare mein kya jaanna chahte ho?"
            )
        
        if st.button("🔍 Analyze Karo!", type="primary"):
            if mode == "❓ Custom Question" and not question:
                st.warning("Pehle sawaal likho!")
            else:
                with st.spinner("AI dekh rahi hai... 👁️"):
                    try:
                        result = analyze_image(uploaded_file, question)
                        
                        st.success("Analysis Complete!")
                        st.markdown("### 📋 AI Ka Jawab:")
                        st.markdown(result)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    else:
        st.info("👈 Pehle image upload karo!")

# ==================
# EXAMPLES SECTION
# ==================
st.divider()
st.subheader("💡 Try Karo:")

ex1, ex2, ex3 = st.columns(3)
with ex1:
    st.info("🌱 Plant ki photo → Disease detect")
with ex2:
    st.info("🍕 Food photo → Calories pata karo")
with ex3:
    st.info("📝 Receipt photo → Text extract karo")