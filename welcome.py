import streamlit as st
from chooseLangauge import translate_word,language_chooser

def welcome_page():
    st.title(translate_word("🚀 Welcome to Stock Analyzer App!"))

    st.image("icons8-stock-48.png", width=200)  

    st.write(translate_word(
        "Explore the world of stocks with our powerful Stock Analyzer App! This app provides you with tools to analyze stock prices, make predictions, and discover investment opportunities. "
        "Navigate through the sidebar options to get started."
    ))

    st.subheader(translate_word("📚 Available Pages:"))

    st.markdown(f"- **{translate_word('User Entrance Field')}**: {translate_word('Navigate to the user entrance field to sign up, sign in, or change user information.')}")
    st.markdown(f"- **{translate_word('Stock Analysis')}**:  {translate_word('Explore the Stock Analysis page to analyze stock prices, make predictions, and check investment opportunities.')}")
    st.markdown(f"- **{translate_word('Choose Language')}**:  {translate_word('If you prefer a different language, use this page to choose your preferred language.')}")

    st.write(translate_word(
        "Feel free to explore the different functionalities and make the most out of the Stock Analyzer App! 📊📈"
    ))
    file_path = r"C:\Users\user\Documents\Stock_finnale_project\code.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        with st.expander("Show Code"):
            st.text(text)

    except UnicodeDecodeError:
        st.error(f"Unable to decode the content of the file: {file_path}")



