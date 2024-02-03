import json
import os
import streamlit as st
import pandas as pd
from chooseLangauge import translate_word


json_file_path = "users.json"
main_script_path = "test.py"

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
        
        users[username] = user_data
        users[f"{username}_info"] = {'Age':age,'City':city,'Amount_invested':amount_invested}
        with open(json_file_path, "w") as file:
            json.dump(users, file)
        st.success(translate_word("You have successfully signed up!"))



def end(username, password):
    users ={}
    if user_exists(username):
        with open(json_file_path, "r") as file:
            users = json.load(file)
            user_data = users.get(username)    
            if user_data and user_data.get("password") == password:
                additional_info = users.get(f"{username}_info")
                
                st.caption(translate_word(f"welcome back, {username}"))
                st.write(translate_word("User info"))
                d = {
                    'Username': username,
                    'Password': user_data['password'],
                    'Age': additional_info['Age'],
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