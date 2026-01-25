import streamlit as st
from chooseLangauge import translate_word
import json
from handleRecom import Recommendations, load_company_dict

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True

def recommendations():
    with open("texts/stocks.json" ,'r') as file:
        data = json.load(file)
    st.title(translate_word("Recommendations"))
    stock = st.selectbox(translate_word("Select or enter company name:"), list(load_company_dict().keys()), index=0).upper()
    st.button(translate_word('Search'), on_click=click_button)
    if st.session_state.clicked:
        try:
            st.image(f"company_logos/{data[stock].lower()}.png", width=200)
            st.caption(stock)
        except:
            try:
                st.image(f"company_logos/{data[stock].lower()}.jpg", width=200)
                st.caption(stock)
            except:
                st.caption("No images available")
        Recommendations(stock)
