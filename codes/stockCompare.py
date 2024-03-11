import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import json
from chooseLangauge import translate_word
import datetime
import random
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
    
    
def rating():
    st.subheader(translate_word("Rating"))
    st.markdown(translate_word("Please rate this stock (1-5 stars):"))
    rating = st.empty()
    stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
    user_rating = rating.radio(" ", stars,key='⭐⭐⭐⭐⭐')
    return user_rating


def display_stock_values(stock_symbol1, stock_value1, stock_symbol2, stock_value2):
    fig = go.Figure(data=[
        go.Bar(name=translate_word("Stock Value"), x=[stock_symbol1, stock_symbol2], y=[stock_value1, stock_value2])
    ])
    fig.update_layout(title=translate_word("Stock Values Today"), xaxis_title=translate_word("Stock Symbol"), yaxis_title=translate_word("Stock Value (USD)"))
    st.plotly_chart(fig)


@st.cache_data
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as yf_error:
        st.error(translate_word(f"Error retrieving data: {yf_error}"))
        return None


def plot_stock_comparison(stock_data1, stock_data2, stock1="stock1", stock2="stock2"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data1.index, y=stock_data1['Close'], mode='lines', name=f'{stock1}'))
    fig.add_trace(go.Scatter(x=stock_data2.index, y=stock_data2['Close'], mode='lines', name=f'{stock2}'))
    fig.update_layout(title=translate_word('Stock Price Comparison'), xaxis_title=translate_word('Date'), yaxis_title=translate_word('Stock Price (USD)'))
    st.plotly_chart(fig)


def investment_return(stock_data, start_value=100):
    start_price = stock_data['Close'].iloc[0]
    end_price = stock_data['Close'].iloc[-1]
    percent_change = ((end_price - start_price) / start_price)
    end_value = start_value * (1 + percent_change)
    return end_value


def plot_investment_return(stock_data1, stock_data2, stock_symbol1, stock_symbol2):
    investment1 = investment_return(stock_data1)
    investment2 = investment_return(stock_data2)
    labels = [stock_symbol1, stock_symbol2]
    values = [investment1, investment2]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    from israelcities import colors
    chosen =[]
    while len(chosen)!=3:
        rnd =random.randint(0,6)
        if colors[rnd] not in chosen:
            chosen.append(colors[rnd])
    fig.update_traces(marker=dict(colors=[chosen[0], chosen[1]]))
    st.button(translate_word('Change colors'), on_click=click_button)
    fig.update_layout(
        title=translate_word('Return on each stock: 100$'),
        legend=dict(
            orientation="v",
            x=0,
            y=0.5,
            traceorder="normal",
            title_font_family="Arial",
            font=dict(family="Arial", size=12, color=chosen[2]),
            itemsizing="constant",
            itemwidth=90,  
            itemclick=False,  
            bgcolor="rgba(0, 0, 0, 0)",  
            bordercolor="rgba(0,0,0,0)",
            borderwidth=0        
        )
    )
    st.plotly_chart(fig)
    
    
def Compare():
    st.title(translate_word("Stock Comparison"))
    with open("texts/stocks.json", "r") as json_file:
        stocks_dict = json.load(json_file)
    stock_symbol1 = st.selectbox(translate_word("Select the first stock:"), list(stocks_dict.keys()))
    stock_symbol2 = st.selectbox(translate_word("Select the second stock:"), list(stocks_dict.keys()), index=list(stocks_dict.keys()).index("APPLE"))
    min_date = datetime.date(2020, 1, 1)
    max_date = datetime.datetime.now() - datetime.timedelta(days=16)
    start_date = st.date_input(translate_word("Select start date:"),
                            min_value=min_date,
                            max_value=max_date,
                            value=min_date)
    end_date = datetime.datetime.now().date()

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
                
                display_stock_values(stock_symbol1, stock_data1['Close'][-1], stock_symbol2, stock_data2['Close'][-1])
                change1 = PrecentChange(stock_data1['Close'])
                change2 = PrecentChange(stock_data2['Close'])
                st.subheader(translate_word("Comparison Table"))
                comparison_data = {
                    translate_word(f"since {start_date}"): [translate_word("Max Close"), translate_word("Min Close"), translate_word("Average Close"), translate_word(f"Percent Of Change")],
                    stock_symbol1: [f"{stock_data1['Close'].max():.2f}", f"{stock_data1['Close'].min():.2f}", f"{stock_data1['Close'].mean():.2f}", f"{change1.precentChange():.2f}%"],
                    stock_symbol2: [f"{stock_data2['Close'].max():.2f}", f"{stock_data2['Close'].min():.2f}", f"{stock_data2['Close'].mean():.2f}", f"{change2.precentChange():.2f}%"]
                }
                
                stocks = [symbol1,symbol2]
                df_comparison = pd.DataFrame(comparison_data)
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.text(f"""Real time updated
                            
                            
                            
                            Table
                            """) 
                    st.table(df_comparison)
                     
                with col2:
                    st.text("")  
                    plot_investment_return(stock_data1, stock_data2, stock_symbol1, stock_symbol2)
                st.title(translate_word("Recommendation"))
                username = st.text_input(translate_word("Enter your recommender name"))
                stock_recommend = st.selectbox(translate_word("Which stock do you recommend?"), stocks, index=list(stocks).index(bigger)) 
                recommendation = st.text_area(translate_word("Leave a comment"))
                rate = rating()
                st.button(translate_word('Send'), on_click=click_button)
                if st.session_state.clicked:
                    if update_recom(username,stock_recommend,recommendation,rate) is True:
                        st.success("Comment uploaded.")  
                recommendations()       
            else:
                st.warning(translate_word("Failed to fetch data for one or both of the stocks. Please try again."))
        else:
            st.warning(translate_word("Please select both stocks."))



from recommendations import recommendations    
    
def update_recom(username, stock_symbol, comment,rating='⭐⭐⭐⭐⭐'):
    try:    
        if username !="" and comment !="":
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
            try:
                data[f"{username}_{stock_symbol}"] = [stock_symbol, comment,rating]

                with open(r"texts\recommendations.json", "w") as json_file:
                    json.dump(data, json_file)
                return True
            except:
                return False
    except:
        return False
def pages():
    page = translate_word("Comparation")
    if page == translate_word("Comparation"):
        Compare()
        
if __name__ == "__main__":
    pages()
