import streamlit as st
from chooseLangauge import translate_word

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
    def MarkDownCode(file_path,file_name):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            with st.expander(file_name):
                st.text(text)
        except UnicodeDecodeError:
            st.error(f"Unable to decode the content of the file: {file_path}")

    st.sidebar.subheader("Matirials")
    st.sidebar.markdown("- [Repo](https://github.com/itayfroo/Stock_finnale_project.git)")
    st.sidebar.markdown("- [Trello](https://trello.com/invite/b/IyuMvsIu/ATTI2efaf2747c29302d9c6d9b2e34de2adbD83CB449/stock-fetching-itayf-markk)")
    st.sidebar.markdown("- [Tk app repo](https://github.com/itayfroo/stock-analyzer.git)")
    st.markdown("---")    
    MarkDownCode(r"codes\test.py",'test.py')
    MarkDownCode(r"codes\signIn.py",'signIn')
    MarkDownCode(r'codes\longtexts.py','longtexts.py')
    MarkDownCode(r'codes\login.py','login.py')
    MarkDownCode(r'codes\israelcities.py','israelcities.py')
    MarkDownCode(r'codes\homepage.py','homepage.py')
    MarkDownCode(r'codes\chooseLangauge.py','chooseLangauge.py')
    MarkDownCode(r'codes\welcome.py','welcome.py')
    
    
    

