import streamlit as st
from googletrans import Translator
def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'

    st.header(print_word("Choose a language"))
    language_options = ['Russian', 'English', 'Hebrew']
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options)
    st.session_state.chosen_language = st.session_state.chosen_language[:2].lower()




def translate_word(word, chosen_language):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'  
    translator = Translator()
    translated_word = translator.translate(word, dest=st.session_state.chosen_language).text
    return translated_word

def print_word(word):
    if 'chosen_language' in st.session_state:
        translated_word = translate_word(word, st.session_state.chosen_language)
        return translated_word
    else:
        return word