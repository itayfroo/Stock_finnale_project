import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf

import random
import json
import os
from chooseLangauge import translate_word,language_chooser
check = False

data=[]

api_keys = ['MNI5T6CU7KLSFJA8', 'QJFF49AEUN6NX884', '9ZZWS60Q2CZ6JYUK', 'ZX5XTAKCAXGAYNBG', "XUKT2LY2NIC35B83","9XZBYP0RSJFMOT4L"
            ,"L485NGI7NK2M6VFT","PS74H4D0OXVW2M22","X7RFFB0EHKNTH25O","EEINBBF6PX2GAO02","FLTAY1Z6W73ZVRQB","JDZLDTK95XWAYVEP"
            ,"QOHMIEDH92482YHC","ZL7O0XZCYX1QQAIB"]
api_key = api_keys[random.randint(0,len(api_keys)-1)]  

def get_stock_symbol_from_json(company_name):
    try:
        with open("stocks.json", "r") as json_file:
            data = json.load(json_file)
            if company_name in data:
                return data[company_name]
    except FileNotFoundError:
        pass  # File not found, proceed to API call
    except json.JSONDecodeError:
        pass  # JSON decoding error, proceed to API call

    return None
        
def update_stock_symbol_in_json(company_name, stock_symbol):
    try:
        with open("stocks.json", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[company_name] = stock_symbol

    with open("stocks.json", "w") as json_file:
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

            # Update JSON file with the new entry
            update_stock_symbol_in_json(company_name, stock_symbol)

            return stock_symbol
    except Exception as e:
        st.error(f"Error: {e}")

    return None



def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
        # Check if the retrieved data is empty
        if stock_data.empty:
            st.warning("No data available for the specified date range.")
            return None
        
        # Check if there are missing values in the data
        if stock_data.isnull().values.any():
            st.warning("Data contains missing values. Please check the data for completeness.")
            return None

        return stock_data
    except yf.YFinanceError as yf_error:
        # Handle the specific exception related to the failed download
        if "No timezone found, symbol may be delisted" in str(yf_error):
            st.warning(f"Error retrieving data: {yf_error}. The symbol may be delisted.")
        else:
            st.error(f"Error retrieving data: {yf_error}")
        
        return None


def plot_stock_data(stock_data):
    fig = px.line(stock_data, x=stock_data.index, y='Close', title='Stock Prices Over the Last Year')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Stock Price (USD)')
    st.plotly_chart(fig)

def predict_tomorrows_stock_value_linear_regression(stock_data):
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']

    model = LinearRegression()
    model.fit(X, y)

    tomorrow = X.iloc[[-1]]['Days'].values[0] + 1
    predicted_value = model.predict([[tomorrow]])[0]
    check1 = True
    return predicted_value

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

# Function to display information about LSTM



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
        with open("stocks.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

company_dict = load_company_dict()

from homepage import homepage
from main import stockanalyzer


page = st.sidebar.radio(translate_word("Select Page"), [translate_word("Home"), translate_word("Stock Analysis"),translate_word("Choose langauge")])
if page == translate_word("Home"):
    homepage()
elif page == translate_word("Stock Analysis"):
    stockanalyzer()
elif page == translate_word("Choose langauge"):
    language_chooser()