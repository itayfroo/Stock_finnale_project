from googletrans import LANGUAGES, Translator
import streamlit as st

def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'  # Set default language to English
    language_options = list(LANGUAGES.values())
    language_options.remove('english') # Remove English from the list
    language_options.insert(0, 'english') # Insert English at the beginning
    default_language = st.session_state.chosen_language
    default_language_index = language_options.index(default_language) if default_language in language_options else 0
    new_language = st.selectbox("Choose a language", language_options, index=default_language_index)
    if new_language != st.session_state.chosen_language:
        st.session_state.chosen_language = new_language
        st.cache_resource.clear()  
        st.rerun()



@st.cache_resource
def translate_word(word):
    try:
        if 'chosen_language' not in st.session_state:
            st.session_state.chosen_language = 'en'  
        translator = Translator()
        translated_word = translator.translate(word, dest=st.session_state.chosen_language).text
        return translated_word
    except: return word