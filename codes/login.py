import json
import os
import streamlit as st
import pandas as pd
from chooseLangauge import translate_word
json_file_path = r"texts\users.json"
main_script_path = "test.py"
def load_company_dict():
    try:
        with open(r"texts\stocks.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

company_dict = load_company_dict()
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
                    st.error("Error decoding JSON. Please check the file format.")
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
                    st.error("Error decoding JSON. Please check the file format.")
                    return
            else:
                users = {}
    else:
        users = {}

    if username in users:
        st.warning(translate_word("Username is already taken. Please choose another one"))
    elif username=="":
        st.warning(translate_word("You have to enter a username"))
    elif password=="":
        st.warning(translate_word("You have to enter a password"))
    else:
        user_data = {"password": password}
        age =""
        city =""
        amount_invested = ""
        stock_investment=0
        users[username] = user_data
        users[f"{username}_info"] = {'Age':age,'City':city,'Stock_investment':stock_investment,'Amount_invested':amount_invested}
        with open(json_file_path, "w") as file:
            json.dump(users, file)
        st.success(translate_word("You have successfully signed up!"))



def sign_in(username, password):
    users ={}
    if user_exists(username):
        with open(json_file_path, "r") as file:
            users = json.load(file)
            user_data = users.get(username)    
            if user_data and user_data.get("password") == password:
                additional_info = users.get(f"{username}_info")
                
                st.caption(translate_word(f"welcome back, {username}"))
                st.write(translate_word("User info"))
                from israelcities import israeli_cities
                age= st.text_input(translate_word("Enter your age"))
                st.button(translate_word('Okay'), on_click=click_button)
                if st.session_state.clicked:
                    try:
                        if int(age) < 0 :
                            st.warning(translate_word("Invalid input"))
                            age=""
                        elif int(age) >99:
                            st.warning(translate_word("Invalid input"))
                            age = ""
                        else: 
                            additional_info['Age']=int(age)
                            st.balloons()
                    except:st.warning(translate_word("Invalid input"))
                city=  st.selectbox(translate_word("Enter your city"), israeli_cities)
                stock =st.selectbox(translate_word("Select or enter company name:"), list(company_dict.keys()), index=0).upper()
                additional_info['City'] = city
                additional_info['Stock_investment'] = stock
                amount_invested= st.text_input(translate_word("Enter the amount you want to invest"))
                st.button('Confirm', on_click=click_button)
                if st.session_state.clicked:
                    try:
                        if int(amount_invested) < 0:
                            st.warning(translate_word("Invalid input"))
                            amount_invested =""
                        else: 
                            additional_info['Amount_invested']=int(amount_invested)
                            st.balloons()
                    except:st.warning(translate_word("Invalid input"))
                users[username] = user_data
                users[f"{username}_info"] = {'Age':age,'City':city,'Stock_investment':stock,'Amount_invested':amount_invested}
                with open(json_file_path, "w") as file:
                    json.dump(users, file)
                d = {
                    'Username': username,
                    'Password': user_data['password'],
                    'Age': additional_info['Age'],
                    'Stock':additional_info['Stock_investment'],
                    'City':additional_info['City'],
                    'Amount invested':additional_info['Amount_invested']
                }
                df = pd.DataFrame([d])
                st.table(df)
                
                return True
            else:
                st.warning(translate_word("Incorrect password. Please check for spelling and try again."))
    else:
        st.warning(translate_word("User does not exist. Please sign up or check the username."))