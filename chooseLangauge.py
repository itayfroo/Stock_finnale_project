import streamlit as st
from googletrans import Translator
def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'

    st.header(translate_word("Choose a language"))
    language_options = [ 'English','Russian','Hebrew']
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options)
    st.session_state.chosen_language = st.session_state.chosen_language[:2].lower()




def translate_word(word):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'  
    translator = Translator()
    translated_word = translator.translate(word, dest=st.session_state.chosen_language).text
    return translated_word
