import streamlit as st
from chooseLangauge import translate_word
import json


if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True

#class number 1 - Handles recommendations displays
class Recommendations():

    
    def __init__(self,stock):
        self.company_dict = Recommendations.load_company_dict()
        self.stock_name = stock
        self.sum =0
        self.counter=0
        self.load_recom()
        self.printAverage()
        
        
    def load_company_dict():
        try:
            with open(r"texts\stocks.json", "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}
        
    
    def printAverage(self):
        stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
        average = int(self.sum /self.counter)
        st.write(translate_word(f"Average is: {stars[average-1]}"))
       
       
    def MarkDownCode(name,comment,rate,date):
            try:
                with st.expander(name):
                    st.subheader("Comment")
                    st.text(comment)
                    st.subheader(f'Rating: {rate}')
                    st.subheader(f"Date: {date}")
            except UnicodeDecodeError:
                st.error(f"An error loading the comment: {UnicodeDecodeError}")
              
              
    def average(self,rate):
        stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
        if rate == stars[0]:
            self.sum+=1
        
        if rate == stars[1]:
            self.sum+=2
            
        if rate == stars[2]:
            self.sum+=3
            
        if rate == stars[3]:
            self.sum+=4
            
        if rate == stars[4]:
            self.sum+=5

                               
    def load_recom(self):
        try:
            counter = 0
            with open(r"texts\stocks.json", "r") as stocks_file:
                stocks_data = json.load(stocks_file)
                stock_symbol = stocks_data[self.stock_name]
            with open(r"texts\recommendations.json", "r") as recom_file:
                recom_data = json.load(recom_file)
                for key in recom_data:
                    if recom_data[key][0] == stock_symbol and recom_data[key][1].strip():
                        counter += 1
                        stock_initial = key[0:key.index('_')]
                        comment = recom_data[key][1]
                        try:
                            rating = recom_data[key][2]
                        except:
                            rating = '⭐⭐⭐⭐☆'
                        Recommendations.average(self,rating)
                        words = comment.split()
                        try:
                            date=recom_data[key][3][:10]
                        except:
                            date='Two years ago'
                        wrapped_comment = '\n'.join([' '.join(words[i:i+8]) for i in range(0, len(words), 8)])
                        Recommendations.MarkDownCode(stock_initial,f"{translate_word(wrapped_comment)}",rating,date)
                        self.counter+=1
                if counter == 0:
                    st.info(translate_word("No recommendations about this stock yet"))
                else:
                    st.caption(translate_word(f"{counter} recommendations found."))
        except Exception as e:
            st.warning(e) 
    
    
def recommendations():
    st.title(translate_word("Recommendations"))
    company_dict = Recommendations.load_company_dict()
    stock = st.selectbox(translate_word("Select or enter company name:"), list(company_dict.keys()), index=0).upper()
    st.button(translate_word('Search'), on_click=click_button)
    if st.session_state.clicked:
        Recommendations(stock)
