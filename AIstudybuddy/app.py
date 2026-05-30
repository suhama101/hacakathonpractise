import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import base64
import json
from datetime import datetime
from PIL import Image

# ==================
# SETUP
# ==================
load_dotenv(r"C:\Users\Suhama\Desktop\Hackathon\.env")
client = Groq(api_key=os.getenv("GROQ_KEY"))

HISTORY_FILE = "history.json"

# ==================
# HELPER FUNCTIONS
# ==================

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_to_history(subject, question, answer):
    history = load_history()
    history.append({
        "subject": subject,
        "question": question,
        "answer": answer,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M")
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def ask_ai(messages, subject):
    system = f"""
    Tum "Study Buddy" ho — Pakistan ke students ka AI teacher.
    Subject: {subject}
    
    Rules:
    - Hamesha Urdu aur English mix mein jawab do
    - Simple examples do — Pakistani context mein
    - Step by step explain karo
    - Student ko encourage karo
    - Agar math hai to steps clearly dikhao
    """
    
    full_messages = [{"role": "system", "content": system}] + messages
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=full_messages,
        max_tokens=1000
    )
    return response.choices[0].message.content

def analyze_image_question(uploaded_file, question):
    image_bytes = uploaded_file.getvalue()
    image_data = base64.b64encode(image_bytes).decode("utf-8")
    file_type = uploaded_file.type
    
    prompt = f"""
    Tum ek Pakistani teacher ho.
    Is image ko dekho aur yeh karo: {question}
    
    Urdu aur English mix mein jawab do.
    Step by step explain karo.
    """
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{file_type};base64,{image_data}"
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.choices[0].message.content

# ==================
# PAGE CONFIG
# ==================
st.set_page_config(
    page_title="AI Study Buddy Pakistan",
    page_icon="📚",
    layout="wide"
)

# ==================
# CUSTOM CSS
# ==================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a472a, #2d6a4f);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: #f0f7f4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2d6a4f;
        margin: 0.5rem 0;
    }
    .stats-card {
        background: #e8f4f8;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================
# SIDEBAR
# ==================
with st.sidebar:
    st.markdown("# 📚 Study Buddy")
    st.markdown("*Pakistan ka AI Teacher*")
    st.divider()
    
    # Subject selection
    subject = st.selectbox(
        "📖 Subject:",
        [
            "General",
            "Mathematics",
            "Physics", 
            "Chemistry",
            "Biology",
            "Computer Science",
            "English",
            "Urdu"
        ]
    )
    
    st.divider()
    
    # Mode selection
    mode = st.radio(
        "🎯 Mode:",
        ["💬 Chat", "📸 Image Q&A", "📊 History"]
    )
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Chat Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Stats
    history = load_history()
    st.metric("Total Sawaal", len(history))
    
    st.divider()
    st.caption("SE Hackathon 2026")
    st.caption("CUST Islamabad")

# ==================
# MAIN HEADER
# ==================
st.markdown("""
<div class="main-header">
    <h1>📚 AI Study Buddy Pakistan</h1>
    <p>Har sawaal ka jawab — Har subject mein — Bilkul free!</p>
</div>
""", unsafe_allow_html=True)

# ==================
# SESSION STATE
# ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================
# MODE: CHAT
# ==================
if mode == "💬 Chat":
    
    # Welcome message
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            st.write(f"Assalam o Alaikum! 👋 Main tumhara **{subject}** teacher hun. Koi bhi sawaal poochho — main step by step samjhaunga!")
    
    # Chat history dikhao
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_input = st.chat_input(f"💬 {subject} ka sawaal likho...")
    
    if user_input:
        # User message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hun... 🤔"):
                try:
                    answer = ask_ai(st.session_state.messages, subject)
                    st.markdown(answer)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    # History mein save
                    save_to_history(subject, user_input, answer)
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==================
# MODE: IMAGE Q&A
# ==================
elif mode == "📸 Image Q&A":
    
    st.subheader("📸 Image se Sawaal Poochho")
    st.write("Math problem, diagram, ya koi bhi image upload karo — AI solve karega!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded = st.file_uploader(
            "Image upload karo:",
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded:
            st.image(Image.open(uploaded), caption="Tumhari image", use_column_width=True)
    
    with col2:
        if uploaded:
            img_question = st.text_area(
                "Sawaal likho:",
                placeholder="Is problem ko solve karo...\nIs diagram ko explain karo...\nIs image mein kya hai?",
                height=100
            )
            
            quick = st.selectbox(
                "Ya quick select karo:",
                [
                    "Custom sawaal",
                    "Is math problem ko solve karo — step by step",
                    "Is diagram ko explain karo",
                    "Is image mein kya hai?",
                    "Is text ko read karke summarize karo"
                ]
            )
            
            final_question = img_question if quick == "Custom sawaal" else quick
            
            if st.button("🔍 Analyze Karo!", type="primary", use_container_width=True):
                if final_question:
                    with st.spinner("AI dekh rahi hai... 👁️"):
                        try:
                            result = analyze_image_question(uploaded, final_question)
                            
                            st.divider()
                            st.subheader("📋 AI Ka Jawab:")
                            st.markdown(result)
                            
                            save_to_history(
                                f"{subject} (Image)",
                                final_question,
                                result
                            )
                            st.success("✅ History mein save ho gaya!")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                else:
                    st.warning("Pehle sawaal likho!")
        else:
            st.info("👈 Pehle image upload karo!")

# ==================
# MODE: HISTORY
# ==================
elif mode == "📊 History":
    
    st.subheader("📊 Tumhari Study History")
    
    history = load_history()
    
    if not history:
        st.info("Abhi koi history nahi — pehle kuch sawaal poochho!")
    else:
        # Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sawaal", len(history))
        
        subjects_used = list(set(h["subject"] for h in history))
        col2.metric("Subjects", len(subjects_used))
        col3.metric("Aaj Ke Sawaal", 
            len([h for h in history if h["date"] == datetime.now().strftime("%Y-%m-%d")])
        )
        
        st.divider()
        
        # Filter
        filter_subject = st.selectbox(
            "Subject filter:",
            ["Sab"] + subjects_used
        )
        
        filtered = history if filter_subject == "Sab" else [
            h for h in history if h["subject"] == filter_subject
        ]
        
        # History dikhao
        for item in reversed(filtered[-20:]):
            with st.expander(f"📝 [{item['date']} {item['time']}] {item['subject']} — {item['question'][:50]}..."):
                st.write("**Sawaal:**", item["question"])
                st.divider()
                st.write("**AI Ka Jawab:**")
                st.markdown(item["answer"])
        
        st.divider()
        if st.button("🗑️ Sari History Delete Karo", type="secondary"):
            with open(HISTORY_FILE, "w") as f:
                json.dump([], f)
            st.success("History clear ho gayi!")
            st.rerun()