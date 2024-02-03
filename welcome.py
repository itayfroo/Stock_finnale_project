
import streamlit as st
from chooseLangauge import translate_word

def welcome_page():
    st.title(translate_word("Welcome to Stock Analyzer App!"))

    st.write(translate_word(
        "This app allows you to analyze stock prices, make predictions, and explore investment opportunities. "
        "Navigate through the sidebar options to get started."
    ))

    st.subheader(translate_word("Available Pages:"))

    st.markdown(f"- **{translate_word('User Entrance Field')}**: Navigate to the user entrance field to sign up, sign in, or change user information.")
    st.markdown(f"- **{translate_word('Stock Analysis')}**: Explore the Stock Analysis page to analyze stock prices, make predictions, and check investment opportunities.")
    st.markdown(f"- **{translate_word('Choose Language')}**: If you prefer a different language, use this page to choose your preferred language.")

    st.write(translate_word(
        "Feel free to explore the different functionalities and make the most out of the Stock Analyzer App!"
    ))


