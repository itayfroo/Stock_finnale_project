import json
import streamlit as st
from chooseLangauge import translate_word
from handleReport import Reports


class Recommendations(Reports):
    def __init__(self, stock):
        self.company_dict = load_company_dict()
        super().__init__(stock)

    def on_average(self, stars_text):
        st.write(translate_word(f"Average is: {stars_text}"))

    def on_recommendation(self, name, comment, rate, date):
        try:
            with st.expander(name):
                st.subheader("Comment")
                st.text(translate_word(comment))
                st.subheader(f"Rating: {rate}")
                st.subheader(f"Date: {date}")
        except UnicodeDecodeError as e:
            st.error(f"An error loading the comment: {e}")

    def on_no_recommendations(self):
        st.info(translate_word("No recommendations about this stock yet"))

    def on_count(self, count):
        st.caption(translate_word(f"{count} recommendations found."))

    def on_warning(self, e):
        st.warning(e)


def load_company_dict():
    try:
        with open(r"texts\stocks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
