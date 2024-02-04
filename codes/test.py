import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
import time  
import datetime
import random
import json
from chooseLangauge import translate_word,language_chooser
check = False

data=[]

api_keys = ['MNI5T6CU7KLSFJA8', 'QJFF49AEUN6NX884', '9ZZWS60Q2CZ6JYUK', 'ZX5XTAKCAXGAYNBG', "XUKT2LY2NIC35B83","9XZBYP0RSJFMOT4L"
            ,"L485NGI7NK2M6VFT","PS74H4D0OXVW2M22","X7RFFB0EHKNTH25O","EEINBBF6PX2GAO02","FLTAY1Z6W73ZVRQB","JDZLDTK95XWAYVEP"
            ,"QOHMIEDH92482YHC","ZL7O0XZCYX1QQAIB"]
api_key = api_keys[random.randint(0,len(api_keys)-1)]  

def get_stock_symbol_from_json(company_name):
    try:
        with open(r"C:\Users\user\Documents\Stock_finnale_project\texts\stocks.json", "r") as json_file:
            data = json.load(json_file)
            if company_name in data:
                return data[company_name]
    except FileNotFoundError:
        pass  
    except json.JSONDecodeError:
        pass  

    return None
def update_stock_symbol_in_json(company_name, stock_symbol):
    try:
        with open(r"C:\Users\user\Documents\Stock_finnale_project\texts\stocks.json", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[company_name] = stock_symbol

    with open(r"C:\Users\user\Documents\Stock_finnale_project\texts\stocks.json", "w") as json_file:
        json.dump(data, json_file)
def get_stock_symbol(company_name):
    global api_key

    stock_symbol = get_stock_symbol_from_json(company_name)

    if stock_symbol:
        return stock_symbol

    base_url = "https://www.alphavantage.co/query"
    function = "SYMBOL_SEARCH"

    params = {
        "function": function,
        "keywords": company_name,
        "apikey": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "bestMatches" in data and data["bestMatches"]:
            stock_symbol = data["bestMatches"][0]["1. symbol"].upper()

       
            update_stock_symbol_in_json(company_name, stock_symbol)

            return stock_symbol
    except Exception as e:
        st.error(f"Error: {e}")

    return None
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
    
        if stock_data.empty:
            st.warning("No data available for the specified date range.")
            return None
        
       
        if stock_data.isnull().values.any():
            st.warning("Data contains missing values. Please check the data for completeness.")
            return None

        return stock_data
    except yf.YFinanceError as yf_error:
       
        if "No timezone found, symbol may be delisted" in str(yf_error):
            st.warning(f"Error retrieving data: {yf_error}. The symbol may be delisted.")
        else:
            st.error(f"Error retrieving data: {yf_error}")
        
        return None
def plot_stock_data(stock_data,start_date):
    fig = px.line(stock_data, x=stock_data.index, y='Close', title=translate_word(f'Stock Prices Over since: {start_date}'))
    fig.update_xaxes(title_text=translate_word('Date'))
    fig.update_yaxes(title_text=translate_word('Stock Price (USD)'))
    st.plotly_chart(fig)
    
@st.cache_data(experimental_allow_widgets=True)               
def predict_tomorrows_stock_value_linear_regression(stock_data):
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']

    model = LinearRegression()
    model.fit(X, y)

    tomorrow = X.iloc[[-1]]['Days'].values[0] + 1
    predicted_value = model.predict([[tomorrow]])[0]
    check1 = True
    return predicted_value

@st.cache_data(experimental_allow_widgets=True)               
def predict_tomorrows_stock_value_lstm(stock_data):
    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))

    seq_length = 10
    sequences, labels = [], []
    for i in range(len(data_normalized) - seq_length):
        seq = data_normalized[i:i + seq_length]
        label = data_normalized[i + seq_length]
        sequences.append(seq)
        labels.append(label)

    X_train, y_train = np.array(sequences), np.array(labels)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    model.fit(X_train, y_train, epochs=50, batch_size=32)

    last_sequence = data_normalized[-seq_length:]
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    predicted_value = model.predict(last_sequence)
    predicted_value = scaler.inverse_transform(predicted_value.reshape(1, -1))[0, 0]
    check =True
    return predicted_value

from longtexts import linear_Regression,display_lstm_info

st.set_page_config(
    page_title="Stocks analyzer",
    page_icon=r"icons8-stock-48.png",
    
)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def load_company_dict():
    try:
        with open(r"C:\Users\user\Documents\Stock_finnale_project\texts\stocks.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

company_dict = load_company_dict()
def stockanalyzer():
    st.title(translate_word("Stock Analyzer"))
    company_name = st.selectbox(translate_word("Select or enter company name:"), list(company_dict.keys()), index=0).upper()
    min_date = datetime.date(2020, 1, 1)
    max_date = datetime.datetime.now() - datetime.timedelta(days=16)
    start_date = st.date_input(translate_word("Select start date:"),
                               min_value=min_date,
                               max_value=max_date,
                               value=min_date)

    end_date = datetime.datetime.now().date() 

    st.button(translate_word('Analyze'), on_click=click_button)
    if st.session_state.clicked:
        if company_name =="":
            st.warning(translate_word("You have to enter a stock or a company name."))
        else:
            if company_name.upper() == "APPLE" or company_name.upper() == "AAPL" or company_name.upper() == "APLE":
                stock_symbol = "AAPL"
            elif company_name.upper() == "NVDA" or company_name.upper() == "NVIDIA" or company_name.upper() == "NVIDA":
                stock_symbol = "NVDA"
            else:
                with st.spinner(translate_word("Fetching stock symbol...")):
                    stock_symbol = get_stock_symbol(company_name)
            if stock_symbol:
                st.title(translate_word("Stock Price Visualization App"))
                st.write(translate_word(f"Displaying stock data for {stock_symbol}"))

                with st.spinner(translate_word("Fetching stock data...")):
                    stock_data = get_stock_data(stock_symbol, start_date, end_date)

                if stock_data is not None:
                    plot_stock_data(stock_data,start_date)
                    lowest_point = stock_data['Close'].min()
                    highest_point = stock_data['Close'].max()
                    today_point = stock_data['Close'][-1]
                    chart_data = pd.DataFrame({
                                                    'Date': stock_data.index,
                                                    'Stock Price': stock_data['Close'],
                                                    'Lowest Point': lowest_point,
                                                    'Highest Point': highest_point
                                            })
                    st.line_chart(chart_data.set_index('Date'))
                    st.info(translate_word(f"Today's Stock Price: {round(today_point, 2)}$"))
                    st.success(translate_word(f"Highest Stock Price: {round(highest_point, 2)}$"))
                    st.warning(translate_word(f"Lowest Stock Price: {round(lowest_point, 2)}$"))
                    try:
                        with st.spinner(translate_word("Performing predictions...")):
                            predicted_value_lr = predict_tomorrows_stock_value_linear_regression(stock_data)
                            predicted_value_lstm = predict_tomorrows_stock_value_lstm(stock_data)
                            time.sleep(1)  

                        st.write(translate_word(f"Approximate tomorrow's stock value (Linear Regression): {predicted_value_lr:.2f}$"))
                        st.write(translate_word(f"Approximate tomorrow's stock value (LSTM): {predicted_value_lstm:.2f}$"))

                        with st.expander(translate_word("💡 What is LSTM?")):
                            display_lstm_info()

                        with st.expander(translate_word("💡 What is Linear Regression?")):
                            st.write(translate_word("Linear Regression Simulation:"))
                            linear_Regression(stock_data)              
                    except:
                        st.warning(translate_word("Not enough info for an AI approximation, please try an earlier date."))
                    investment(stock_symbol,stock_data,start_date)
            else:
                st.warning(translate_word(f"Stock doesn't exist.\ntry again or check your input.")) 
def investment(stock_symbol,stock_data,start_date):
    st.title(translate_word("Investment"))
    if stock_data is not None:
        value = st.slider(translate_word("If you were to invest:"), min_value=100, max_value=5000, value=100, step=50,key = "level1")
        start_price = stock_data['Close'].iloc[0]
        end_price = stock_data['Close'].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        potential_returns = value * (1 + percent_change / 100)
        st.write(translate_word(f"If you invest {value:.2f}$ in {stock_symbol} since {start_date}:"))
        st.success(translate_word(f"You would have approximately {potential_returns:.2f}$ based on the percentage change of {percent_change:.2f}%."))
    else:
        st.warning(translate_word(f"Stock doesn't exist.\ntry again or check your input."))
        
from homepage import homepage
from welcome import welcome_page

page = st.sidebar.radio(translate_word("Select Page"), [translate_word("Welcome"), translate_word("Choose Language"), translate_word("User Entrance Field"), translate_word("Stock Analysis")])

if page == translate_word("Welcome"):
    welcome_page()
elif page == translate_word("User Entrance Field"):
    homepage()
elif page == translate_word("Stock Analysis"):
    stockanalyzer()
elif page == translate_word("Choose Language"):
    language_chooser()
