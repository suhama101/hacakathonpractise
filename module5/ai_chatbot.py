import streamlit as st
from groq import Groq
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(r"C:\Users\Suhama\Desktop\Hackathon\.env")
client = Groq(api_key=os.getenv("GROQ_KEY"))

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")

with st.sidebar:
    st.title("📚 Study Buddy")
    subject = st.selectbox("Subject:", ["General", "Mathematics", "Physics", "Computer Science"])
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()

st.title("📚 AI Study Buddy")
st.caption("Koi bhi sawaal poochho!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Sawaal likho...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hun..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"Tum ek Pakistani {subject} teacher ho. Urdu/English mix mein jawab do."},
                        *st.session_state.messages
                    ]
                )
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")