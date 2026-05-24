import streamlit as st

st.title("💬 Chat Demo")

# Chat history session state mein
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Purani messages dikhao
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Kuch likho...")

if user_input:
    # User message add karo
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    # Fake AI response — abhi ke liye
    ai_response = f"Tumne likha: '{user_input}' — AI yahan hogi!"
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": ai_response
    })

    st.rerun()  # Page refresh karo naye messages ke saath