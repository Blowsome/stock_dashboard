import streamlit as st

def show_page():
    st.title("Page 3")
    st.write("Welcome to Page 3!")
    st.slider("Adjust a value", min_value=0, max_value=100)