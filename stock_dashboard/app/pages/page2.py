import streamlit as st

def show_page():
    st.title("Page 2")
    st.write("Welcome to Page 2!")
    name = st.text_input("What's your name?")
    if name:
        st.write(f"Hello, {name}!")