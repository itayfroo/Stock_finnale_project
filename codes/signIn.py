import json
import os
import streamlit as st
import pandas as pd
from chooseLangauge import translate_word


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
        st.warning(translate_word("Username is already taken. Please choose another one"))
    elif username=="":
        st.warning(translate_word("You have to enter a username"))
    elif password=="":
        st.warning(translate_word("You have to enter a password"))
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
        st.success(translate_word("You have successfully signed up!"))



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
                st.markdown("---")
                
                return True
            else:
                st.error("❌ " + translate_word("Incorrect password. Please try again."))
    else:
        st.error("❌ " + translate_word("User does not exist. Please sign up or check the username."))

