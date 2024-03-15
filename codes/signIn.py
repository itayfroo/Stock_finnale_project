import json
import os
import streamlit as st
import pandas as pd
from chooseLangauge import translate_word
import yfinance as yf
import requests
import random
from datetime import datetime


api_keys = ['MNI5T6CU7KLSFJA8', 'QJFF49AEUN6NX884', '9ZZWS60Q2CZ6JYUK', 'ZX5XTAKCAXGAYNBG', "XUKT2LY2NIC35B83","9XZBYP0RSJFMOT4L"
            ,"L485NGI7NK2M6VFT","PS74H4D0OXVW2M22","X7RFFB0EHKNTH25O","EEINBBF6PX2GAO02","FLTAY1Z6W73ZVRQB","JDZLDTK95XWAYVEP"
            ,"QOHMIEDH92482YHC","ZL7O0XZCYX1QQAIB"]
api_key = api_keys[random.randint(0,len(api_keys)-1)]  
json_file_path = r"texts\users.json"
main_script_path = "codes/main.py"


if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True
    
    
def user_exists(username):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            file_contents = file.read()
            if file_contents:
                try:
                    users = json.loads(file_contents)
                except json.JSONDecodeError:
                    st.error(translate_word("Error decoding JSON. Please check the file format."))
                    return False
            else:
                users = {}
                with open(json_file_path, "w") as empty_file:
                    json.dump(users, empty_file)
    else:
        users = {}
    return username in users


def sign_up(username, password, additional_info="default_value"):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            file_contents = file.read()
            if file_contents:
                try:
                    users = json.loads(file_contents)
                except json.JSONDecodeError:
                    st.error(translate_word("Error decoding JSON. Please check the file format."))
                    return
            else:
                users = {}
    else:
        users = {}

    if username in users:
        st.caption(translate_word("Username is already taken. Please choose another one"))
    elif username=="":
        st.caption(translate_word("You have to enter a username"))
    elif password=="":
        st.caption(translate_word("You have to enter a password"))
    else:
        user_data = {"password": password}
        age =""
        city =""
        amount_invested = 0
        stock_investment =""
        users[username] = user_data
        users[f"{username}_info"] = {'Age':age,'City':city,'Stock_investment':stock_investment,'Amount_invested':amount_invested}
        with open(json_file_path, "w") as file:
            json.dump(users, file)
        st.info(translate_word("You have successfully signed up!"))


def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
    
        if stock_data.empty:
            st.caption(translate_word("Check again tomrrow(:"))
            return None
        
       
        if stock_data.isnull().values.any():
            st.caption(translate_word("Data contains missing values. Please check the data for completeness."))
            return None

        return stock_data
    except: 
        return None


def get_stock_symbol_from_json(company_name):
    try:
        with open(r"texts\stocks.json", "r") as json_file:
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
        with open(r"texts\stocks.json", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[company_name] = stock_symbol

    with open(r"texts\stocks.json", "w") as json_file:
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
        st.caption(translate_word(f"Error: {e}"))

    return None


#Class number 4 - Deletes users
class RemoveUser():
    
    
    def __init__(self,username) -> None:
        self.name = username
        self.delete_user(self.name)
        self.delete_user(f"{self.name}_info")
        
        
    def delete_user(self,content):
        file_path = r"texts\users.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                if content in data:
                    del data[content]  
            with open(file_path, "w") as json_file:
                json.dump(data, json_file)
        else:
            print("JSON file does not exist.")


def end(username, password):
    users = {}
    if user_exists(username):
        with open(json_file_path, "r") as file:
            users = json.load(file)
            user_data = users.get(username)    
            if user_data and user_data.get("password") == password:
                additional_info = users.get(f"{username}_info")
                

                st.markdown("---")
                st.subheader("👤 " + translate_word("User Information"))
                
                st.write(f"**{translate_word('Username')}:** {username} 👩‍💻")
                st.write(f"**{translate_word('Password')}:** {user_data['password']} 🔒")
                if additional_info['Age']!="":
                    st.write(f"**{translate_word('Age')}:** {additional_info.get('Age', 'N/A')} 🎂")
                else:
                    st.write(f"**{translate_word('Age')}:** {additional_info.get('Age', 'N/A')}")
                st.write(f"**{translate_word('City')}:** {additional_info.get('City', 'N/A')} 🌆")
                st.write(f"**{translate_word('Stock Investment')}:** {additional_info.get('Stock_investment', 'N/A')} 💹")
                if additional_info['Amount_invested']!="" and additional_info['Amount_invested']!=0:
                    st.write(f"**{translate_word('Amount Invested')}:** {additional_info.get('Amount_invested', 'N/A')} 💰")
                else: 
                    st.write(f"**{translate_word('Amount Invested')}:** {additional_info.get('Amount_invested', 'N/A')} ")
                st.write(f"**{translate_word('Time of registration')}:** {additional_info.get('date', 'N/A')[0:19]}  📅")
                
                if st.button(translate_word('Delete account')):
                    RemoveUser(username)
                st.markdown("---")
                if (additional_info['Amount_invested']!=0):
                    stock_symbol = get_stock_symbol(additional_info['Stock_investment'])
                    end_date = datetime.now()
                    start_date = additional_info['date']
                    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f")
                        
                    stock_data = get_stock_data(stock_symbol, start_date, end_date)
                    try:
                        if stock_data is not None:
                            start_price = stock_data['Close'].iloc[0]
                            end_price = stock_data['Close'].iloc[-1]
                            
                            percent_change = ((end_price - start_price) / start_price) * 100
                            potential_returns = float(additional_info['Amount_invested']) * (1 + percent_change / 100)
                            
                            
                            gain_loss = potential_returns
                            
                            st.text(translate_word(f"Based on current stock prices, you would now have: {gain_loss:.2f}$"))
                            st.text(translate_word(f"with the precentage of change: {percent_change:.2f}%"))
                            if int(additional_info['Amount_invested'])<gain_loss:
                                st.text(translate_word(f"Your total gain: {int(additional_info['Amount_invested'])-gain_loss:.2f}$"))
                                st.info(translate_word("Would recommend investing in this stock(;"))
                            else:
                                st.text(translate_word(f"Your total loss: {(gain_loss - int(additional_info['Amount_invested'])):.2f}$"))
                                st.info(translate_word("Would't recommend investing in this stock(;"))
                            
                        else:
                            pass
                    except Exception as e:
                        st.warning(e)
                
                return True
            else:
                st.caption("❌ " + translate_word("Incorrect password. Please try again."))
    else:
        st.caption("❌ " + translate_word("User does not exist. Please sign up or check the username."))

