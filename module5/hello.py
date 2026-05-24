import streamlit as st

st.title("Mera Pehla Streamlit App! 🎉")
st.write("Yeh Python se bana hai — koi HTML nahi!")

name = st.text_input("Apna naam likho:")

if name:
    st.success(f"Assalam o Alaikum, {name}! 👋")