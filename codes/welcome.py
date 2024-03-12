import streamlit as st
from chooseLangauge import translate_word
import os


#class number 3 - Displays each script in the code
class Scripts():
    
    
    def __init__(self,file):
        self.file = file
        self.name = os.path.basename(self.file)
        self.MarkDownCode()
    
    
    def MarkDownCode(self):
        try:
            with open(self.file, "r", encoding="utf-8") as file:
                text = file.read()

            with st.expander(self.name):
                st.text(text)
        except UnicodeDecodeError:
            st.error(f"Unable to decode the content of the file: {self.file}")


def welcome_page():
    st.title(translate_word("🚀 Welcome to Stock Analyzer App!"))

    st.image("icons8-stock-48.png", width=200)  
    st.write(translate_word("Explore the world of stocks with our powerful Stock Analyzer App! "))
    st.write(translate_word(
        "This app provides you with tools to analyze stock prices, make predictions, and discover investment opportunities. "
        "Navigate through the sidebar options to get started."
    ))

    st.subheader(translate_word("📚 Available Pages:"))

    st.markdown(f"- **{translate_word('User Entrance Field')}**: {translate_word('Navigate to the user entrance field to sign up, sign in, or change user information.')}")
    st.markdown(f"- **{translate_word('Stock Analysis')}**:  {translate_word('Explore the Stock Analysis page to analyze stock prices, make predictions, and check investment opportunities.')}")
    st.markdown(f"- **{translate_word('Choose Language')}**:  {translate_word('If you prefer a different language, use this page to choose your preferred language.')}")

    st.write(translate_word(
        "Feel free to explore the different functionalities and make the most out of the Stock Analyzer App! 📊📈"
    ))

    st.sidebar.subheader(translate_word("Should Read"))
    st.sidebar.markdown("- [Repo](https://github.com/itayfroo/Stock_finnale_project.git)")
    st.sidebar.markdown("- [Trello](https://trello.com/invite/b/IyuMvsIu/ATTI2efaf2747c29302d9c6d9b2e34de2adbD83CB449/stock-fetching-itayf-markk)")
    st.sidebar.markdown("- [Tk app repo](https://github.com/itayfroo/stock-analyzer.git)")
    st.sidebar.markdown("- [Read me!](https://github.com/itayfroo/Stock_finnale_project/blob/main/README.md)")
    st.markdown("---")    
    codes = [r"codes\main.py",r"codes\signIn.py",r'codes\longtexts.py',r'codes\login.py',r'codes\israelcities.py',r'codes\homepage.py',r'codes\chooseLangauge.py',r'codes\stockCompare.py',r'codes\recommendations.py',r'codes\welcome.py']
    st.subheader(translate_word("Scripts"))
    for i in codes:
        Scripts(i)
