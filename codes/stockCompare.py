import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import json
from chooseLangauge import translate_word


class PrecentChange():
    def __init__(self,values):
        self.value = values
        
        
    def precentChange(self):
        start_price = self.value.iloc[0]
        end_price = self.value.iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        return percent_change
        
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True
    
    
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data
    except yf.YFinanceError as yf_error:
        st.error(translate_word(f"Error retrieving data: {yf_error}"))
        return None

def plot_stock_comparison(stock_data1, stock_data2, stock1="stock1", stock2="stock2"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data1.index, y=stock_data1['Close'], mode='lines', name=f'{stock1}'))
    fig.add_trace(go.Scatter(x=stock_data2.index, y=stock_data2['Close'], mode='lines', name=f'{stock2}'))
    fig.update_layout(title=translate_word('Stock Price Comparison'), xaxis_title=translate_word('Date'), yaxis_title=translate_word('Stock Price (USD)'))
    st.plotly_chart(fig)

def Compare():
    st.title(translate_word("Stock Comparison"))

    # Load stocks from stocks.json
    with open("texts/stocks.json", "r") as json_file:
        stocks_dict = json.load(json_file)

    # Select dropdown for first stock symbol
    stock_symbol1 = st.selectbox(translate_word("Select the first stock:"), list(stocks_dict.keys()))

    # Select dropdown for second stock symbol
    stock_symbol2 = st.selectbox(translate_word("Select the second stock:"), list(stocks_dict.keys()), index=list(stocks_dict.keys()).index("APPLE"))

    start_date = st.date_input(translate_word("Select start date:"), pd.to_datetime('2020-01-01'))
    end_date = st.date_input(translate_word("Select end date:"), pd.to_datetime('today'))

    st.button(translate_word('Compare'), on_click=click_button)
    if st.session_state.clicked:

        symbol1 = stocks_dict.get(stock_symbol1)
        symbol2 = stocks_dict.get(stock_symbol2)
        if symbol1 and symbol2:
            stock_data1 = get_stock_data(symbol1, start_date, end_date)
            stock_data2 = get_stock_data(symbol2, start_date, end_date)
            if stock_data1 is not None and stock_data2 is not None:
                plot_stock_comparison(stock_data1, stock_data2, stock_symbol1, stock_symbol2)
                
                if max(stock_data1['Close'][-1],stock_data2['Close'][-1]) == stock_data1['Close'][-1]:
                    st.success(translate_word(f"{stock_symbol1}'s value today: {stock_data1['Close'][-1]:.2f}$"))
                    st.error(translate_word(f"{stock_symbol2}'s value today: {stock_data2['Close'][-1]:.2f}$"))
                    bigger = symbol1
                else:
                    st.success(translate_word(f"{stock_symbol2}'s value today: {stock_data2['Close'][-1]:.2f}$"))
                    st.error(translate_word(f"{stock_symbol1}'s value today: {stock_data1['Close'][-1]:.2f}$"))  
                    bigger = symbol2
                change1 = PrecentChange(stock_data1['Close'])
                change2 = PrecentChange(stock_data2['Close'])
                
                st.subheader(translate_word("Comparison Table"))
                comparison_data = {
                    "Attribute": [translate_word("Max Close"), translate_word("Min Close"), translate_word("Average Close"), translate_word("Percent Change")],
                    stock_symbol1: [f"{stock_data1['Close'].max():.2f}", f"{stock_data1['Close'].min():.2f}", f"{stock_data1['Close'].mean():.2f}", f"{change1.precentChange():.2f}%"],
                    stock_symbol2: [f"{stock_data2['Close'].max():.2f}", f"{stock_data2['Close'].min():.2f}", f"{stock_data2['Close'].mean():.2f}", f"{change2.precentChange():.2f}%"]
                }
                
                
                stocks = [symbol1,symbol2]
                df_comparison = pd.DataFrame(comparison_data)
                st.table(df_comparison)
                st.title(translate_word("Recomendation"))
                username = st.text_input(translate_word("Enter your recommender name"))
                stock_recommend = st.selectbox(translate_word("Which stock do you recommend?"), stocks, index=list(stocks).index(bigger)) 
                recommendation = st.text_area(translate_word("Leave a comment"))
                st.button(translate_word('Send'), on_click=click_button)
                if st.session_state.clicked:
                    update_recom(username,stock_recommend,recommendation)
                
                
            else:
                st.warning(translate_word("Failed to fetch data for one or both of the stocks. Please try again."))
        else:
            st.warning(translate_word("Please select both stocks."))


from recommendations import recommendations    
    
def update_recom(username="default", stock_symbol="NVIDIA", comment=""):
    try:
        with open(r"texts\recommendations.json", "r") as json_file:
            # Check if the file is empty
            if json_file.read().strip() == '':
                data = {}
            else:
                json_file.seek(0)  
                data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[f"{username}_{stock_symbol}"] = [stock_symbol, comment]

    with open(r"texts\recommendations.json", "w") as json_file:
        json.dump(data, json_file)
    
def pages():
    page = st.sidebar.radio(translate_word("Navigation"), [translate_word("Comparation"),translate_word("Recommendations")])
    if page == translate_word("Comparation"):
        Compare()
    elif page==translate_word("Recommendations"):
        recommendations()

if __name__ == "__main__":
    pages()
