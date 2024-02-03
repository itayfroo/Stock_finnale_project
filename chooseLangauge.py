import streamlit as st
from googletrans import Translator
def language_chooser():
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'

    st.header(translate_word("Choose a language"))
    language_options = [
        'English', 'Russian', 'Hebrew', 'French', 'Spanish', 
        'German', 'Italian', 'Chinese', 'Japanese', 
        'Arabic', 'Portuguese', 'Dutch', 'Korean', 'Turkish',
        'Swedish', 'Greek', 'Polish', 'Thai', 'Hindi',
        'Czech', 'Finnish', 'Danish', 'Norwegian', 'Indonesian',
        'Romanian', 'Hungarian', 'Bulgarian', 'Vietnamese', 'Malay',
        'Slovak', 'Slovenian', 'Croatian', 'Serbian', 'Ukrainian',
        'Lithuanian', 'Latvian', 'Estonian', 'Albanian', 'Macedonian',
        'Bosnian', 'Montenegrin', 'Georgian', 'Azerbaijani', 'Kazakh',
        'Uzbek', 'Tajik', 'Kyrgyz', 'Turkmen', 'Mongolian',
        'Burmese', 'Khmer', 'Lao', 'Tagalog', 'Malagasy',
        'Swahili', 'Amharic', 'Tigrinya', 'Somali', 'Hausa',
        'Yoruba', 'Igbo', 'Zulu', 'Xhosa', 'Sesotho',
        'Fijian', 'Samoan', 'Tongan', 'Maori', 'Hawaiian',
        'Marshallese', 'Chamorro', 'Palauan', 'Kiribati', 'Nauruan'
    ]
    st.session_state.chosen_language = st.selectbox("Choose a language", language_options)
    st.session_state.chosen_language = st.session_state.chosen_language[:2].lower()




def translate_word(word):
    if 'chosen_language' not in st.session_state:
        st.session_state.chosen_language = 'en'  
    translator = Translator()
    translated_word = translator.translate(word, dest=st.session_state.chosen_language).text
    return translated_word
