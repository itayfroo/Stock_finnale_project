import streamlit as st
from chooseLangauge import translate_word
from datetime import time,datetime
import json
from test import get_stock_data,get_stock_symbol,plot_stock_data,predict_tomorrows_stock_value_linear_regression,predict_tomorrows_stock_value_lstm
import pandas as pd
import plotly.express as px
from longtexts import display_lstm_info,linear_Regression
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

def stockanalyzer():
    st.title(translate_word("Stock Analyzer"))


    company_name = st.selectbox(translate_word("Select or enter company name:"), list(company_dict.keys()), index=0).upper()




    min_date = datetime.date(2022, 1, 1)
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
                    plot_stock_data(stock_data)
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
                    investment(stock_symbol,stock_data)
            else:
                st.warning(translate_word(f"Stock doesn't exist.\ntry again or check your input.")) 
               
    
def investment(stock_symbol,stock_data):
    st.title(translate_word("Investment"))
    if stock_data is not None:
        value = st.slider(translate_word("If you were to invest:"), min_value=100, max_value=5000, value=100, step=50,key = "level1")
        start_price = stock_data['Close'].iloc[0]
        end_price = stock_data['Close'].iloc[-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        potential_returns = value * (1 + percent_change / 100)
        st.write(translate_word(f"If you invest {value:.2f}$ in {stock_symbol} from the start of 2022 until today:"))
        st.success(translate_word(f"You would have approximately {potential_returns:.2f}$ based on the percentage change of {percent_change:.2f}%."))

    else:
        st.warning(translate_word(f"Stock doesn't exist.\ntry again or check your input."))