import streamlit as st

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.image("https://via.placeholder.com/150", width=150)
    
    page = st.selectbox("Page:", ["Home", "Chat", "About"])
    
    st.divider()
    st.write("**App Info**")
    st.write("Version: 1.0")
    st.write("Made by: Suhama")

# Main content — page ke hisaab se
if page == "Home":
    st.title("🏠 Home")
    st.write("Welcome to my AI app!")
    
elif page == "Chat":
    st.title("💬 Chat")
    st.write("Chat page yahan hogi!")
    
elif page == "About":
    st.title("ℹ️ About")
    st.write("Yeh app SE Hackathon ke liye bani hai!")