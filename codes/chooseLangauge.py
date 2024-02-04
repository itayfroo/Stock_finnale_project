from googletrans import LANGUAGES, Translator
import streamlit as st
@st.cache
def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'
    global lang
    st.header("Choose a language")
    language_options = list(LANGUAGES.values())
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options)
    st.session_state.chosen_language = get_language_code(st.session_state.chosen_language)

def get_language_code(language_name):
    return next((code for code, name in LANGUAGES.items() if name == language_name), 'en')
@st.cache
def translate_word(word):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'
    
    translator = Translator()
    dest_language = st.session_state.chosen_language
    try:
        translated_word = translator.translate(word, dest=dest_language).text
        return translated_word
    except Exception as e:
        st.error(f"Translation error: {e}")
        return word  