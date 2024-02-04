from googletrans import LANGUAGES, Translator
import streamlit as st
def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'default_language'
    st.header("Choose a language")
    language_options = list(LANGUAGES.values())
    default_language_index = language_options.index('english') if 'english' in language_options else 0
    new_language = st.selectbox("Choose a language", language_options, index=default_language_index)
    if new_language != st.session_state.chosen_language:
        st.session_state.chosen_language = new_language
        st.cache_data.clear()  
        st.experimental_rerun()
    

@st.cache_data
def translate_word(word):
    translator = Translator()
    translated_word = translator.translate(word, dest=st.session_state.chosen_language).text
    return translated_word