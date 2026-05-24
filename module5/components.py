import streamlit as st

# ==================
# TEXT COMPONENTS
# ==================
st.title("Yeh Title Hai")
st.header("Yeh Header Hai")
st.subheader("Yeh Subheader Hai")
st.write("Normal text — kuch bhi likh sakte ho")
st.markdown("**Bold**, *italic*, aur `code` bhi!")

# ==================
# INPUT COMPONENTS
# ==================
st.divider()  # Line

name = st.text_input("Naam:")
age = st.number_input("Umar:", min_value=1, max_value=100)
city = st.selectbox("Sheher:", ["Lahore", "Karachi", "Islamabad", "Peshawar"])
agree = st.checkbox("Main agree karta hun")
slider_val = st.slider("Marks:", 0, 100, 50)

# ==================
# BUTTON
# ==================
if st.button("Submit"):
    st.success(f"Naam: {name}, Umar: {age}, Sheher: {city}")
    st.info(f"Marks: {slider_val}")
    if agree:
        st.balloons()  # 🎈 celebration!

# ==================
# METRICS
# ==================
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Students", "150", "+10")
col2.metric("Average", "78%", "+5%")
col3.metric("Pass Rate", "92%", "+2%")