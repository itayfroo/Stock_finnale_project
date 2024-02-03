import streamlit as st
from google_trans_new import google_translator

def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'

    st.header(print_word("Choose a language"))
    language_options = ['Russian', 'English', 'Hebrew', 'French', 'Spanish']
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options)
    st.session_state.chosen_language = st.session_state.chosen_language[:2].lower()

def translate_word(word, chosen_language):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'
        
    translator = google_translator()
    translated_word = translator.translate(word, lang_tgt=st.session_state.chosen_language)
    return translated_word

def print_word(word):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'
        
    translated_word = translate_word(word, st.session_state.chosen_language)
    return translated_word

# Example usage in Streamlit
word_to_translate = st.text_input("Enter a word:")
language_chooser()

if word_to_translate:
    translated_result = print_word(word_to_translate)
    st.write(f"Original Word: {word_to_translate}")
    st.write(f"Translated Word: {translated_result}")
