from googletrans import LANGUAGES, Translator
import streamlit as st
def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'
    st.header("Choose a language")
    language_options = list(LANGUAGES.values())
    default_language_index = language_options.index('English') if 'English' in language_options else 0
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options, index=default_language_index)
    st.session_state.chosen_language = get_language_code(st.session_state.chosen_language)

    

def get_language_code(language_name):
    return next((code for code, name in LANGUAGES.items() if name == language_name), 'en')
@st.cache_data()       
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