import streamlit as st
from chooseLangauge import translate_word
import json
import textwrap

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True


def load_company_dict():
    try:
        with open(r"texts\stocks.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}
    
    
def load_recom(stock_name):
    try:
        counter = 0
        with open(r"texts\stocks.json", "r") as stocks_file:
            stocks_data = json.load(stocks_file)
            stock_symbol = stocks_data[stock_name]

        with open(r"texts\recommendations.json", "r") as recom_file:
            recom_data = json.load(recom_file)
            for key in recom_data:
                if recom_data[key][0] == stock_symbol and recom_data[key][1].strip():
                    counter += 1
                    stock_initial = key[0:key.index('_')]
                    comment = recom_data[key][1]
                    # Split the comment into words
                    words = comment.split()
                    # Wrap the words after every 8 words
                    wrapped_comment = '\n'.join([' '.join(words[i:i+8]) for i in range(0, len(words), 8)])
                    st.text(f"{stock_initial}: {translate_word(wrapped_comment)}")
                
            if counter == 0:
                st.info(translate_word("No recommendations about this stock yet"))
            else:
                st.caption(translate_word(f"{counter} recommendations found."))
    except Exception as e:
        st.warning(e)




        
company_dict = load_company_dict()
def recommendations():
    st.title(translate_word("Recommendations"))
    stock = st.selectbox(translate_word("Select or enter company name:"), list(company_dict.keys()), index=0).upper()
    st.button(translate_word('Search'), on_click=click_button)
    if st.session_state.clicked:
        load_recom(stock)