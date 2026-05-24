import streamlit as st

# Session state initialize karo
if "count" not in st.session_state:
    st.session_state.count = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Session State Demo")

# Counter
if st.button("Click karo"):
    st.session_state.count += 1

st.write(f"Tumne {st.session_state.count} baar click kiya!")

# Message list
msg = st.text_input("Kuch likho:")
if st.button("Add karo"):
    if msg:
        st.session_state.messages.append(msg)

st.write("Tumhari messages:")
for m in st.session_state.messages:
    st.write(f"• {m}")