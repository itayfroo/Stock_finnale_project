from chooseLangauge import translate_word
import streamlit as st
from login import Users


if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


def homepage():
    user = Users()
    st.title(translate_word("User Authentication System"))
    from signIn import end
    page = st.sidebar.radio(translate_word("Navigation"), [translate_word("Sign Up"),translate_word("Change info") ,translate_word("Sign In")])

    if page == translate_word("Sign Up"):
        st.header(translate_word("Sign Up"))
        username = st.text_input(translate_word("Enter your username:"))
        password = st.text_input(translate_word("Enter your password:"), type="password")
        
        st.button(translate_word('Sign up'), on_click=click_button)
        if st.session_state.clicked:
            user.sign_up(username, password)

    elif page == translate_word("Change info"):
        st.header(translate_word("Change info"))
        username = st.text_input(translate_word("Enter your username:"))
        password = st.text_input(translate_word("Enter your password:"), type="password")
        st.button(translate_word('Change info'), on_click=click_button)
        if st.session_state.clicked:
            if user.sign_in(username, password):
                pass
    
    else:
        st.header(translate_word("Sign in"))
        username = st.text_input(translate_word("Enter your username:"))
        password = st.text_input(translate_word("Enter your password:"), type="password")
        st.button(translate_word('Sign in'), on_click=click_button)
        if st.session_state.clicked:
            if end(username, password):
                pass