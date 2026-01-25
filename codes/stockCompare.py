import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from chooseLangauge import translate_word
import datetime
import random
from recommendations import recommendations
from encryptionRecomm import EncriptRecoms
from server import *
import time

# --------------------------------------------------------
# CLASS: EncriptRecoms
# --------------------------------------------------------

# --------------------------------------------------------
# CLASS: Percent Change
# --------------------------------------------------------
class PrecentChange:


    def __init__(self, prices, start_date, end_date):
        self.price_dict = prices
        self.start = self._nearest_date(start_date)
        self.end = self._nearest_date(end_date)

        self.change = self.precentChange()


    def _nearest_date(self, date_str):
        # dictionary keys: "YYYY-MM-DD"
        available = list(self.price_dict.keys())
        if date_str in available:
            return date_str
        # sort and find closest
        dt = pd.to_datetime(date_str)
        candidates = sorted(available, key=lambda x: abs(pd.to_datetime(x) - dt))
        return candidates[0]


    def precentChange(self):
        start_price = float(self.price_dict[self.start])
        end_price = float(self.price_dict[self.end])
        percent_change = ((end_price - start_price) / start_price) * 100
        return percent_change


# --------------------------------------------------------
# STATE HANDLING
# --------------------------------------------------------
if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True


# --------------------------------------------------------
# USER RATING INPUT
# --------------------------------------------------------
def rating():
    st.subheader(translate_word("Rating"))
    st.markdown(translate_word("Please rate this stock (1-5 stars):"))
    rating = st.empty()
    stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
    user_rating = rating.radio(" ", stars, key='⭐⭐⭐⭐⭐')
    return user_rating


# --------------------------------------------------------
# BAR GRAPH FOR VALUE COMPARISON
# --------------------------------------------------------
def display_stock_values(stock_symbol1, stock_value1, stock_symbol2, stock_value2):
    fig = go.Figure(data=[
        go.Bar(name=translate_word("Stock Value"),
               x=[stock_symbol1, stock_symbol2],
               y=[stock_value1, stock_value2])
    ])

    fig.update_layout(
        title=translate_word("Stock Values Today"),
        xaxis_title=translate_word("Stock Symbol"),
        yaxis_title=translate_word("Stock Value (USD)")
    )

    st.plotly_chart(fig)


# --------------------------------------------------------
# DOWNLOAD STOCK DATA
# --------------------------------------------------------
@st.cache_data
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
        if stock_data is None or stock_data.empty:
            return None
        return stock_data
    except Exception:
        return None


# --------------------------------------------------------
# LINE COMPARISON GRAPH
# --------------------------------------------------------
def plot_stock_comparison(stock_data1, stock_data2, stock1="stock1", stock2="stock2"):
    # Extract dates and prices from dictionaries
    dates1 = list(stock_data1.keys())
    prices1 = list(stock_data1.values())

    dates2 = list(stock_data2.keys())
    prices2 = list(stock_data2.values())

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates1,
        y=prices1,
        mode='lines',
        name=stock1
    ))

    fig.add_trace(go.Scatter(
        x=dates2,
        y=prices2,
        mode='lines',
        name=stock2
    ))

    fig.update_layout(
        title=translate_word('Stock Price Comparison'),
        xaxis_title=translate_word('Date'),
        yaxis_title=translate_word('Stock Price (USD)')
    )

    st.plotly_chart(fig)


# --------------------------------------------------------
# INVESTMENT RETURN
# --------------------------------------------------------
def investment_return(prices, start_value=100):
    # prices is a list of numbers
    if not prices:
        return start_value

    start_price = prices[0]
    end_price = prices[-1]

    percent_change = (end_price - start_price) / start_price
    end_value = start_value * (1 + percent_change)

    return end_value


# --------------------------------------------------------
# PIE CHART FOR RETURNS
# --------------------------------------------------------
def plot_investment_return(stock_data1, stock_data2, stock_symbol1, stock_symbol2):
    # stock_data1 and stock_data2 are dicts: {"YYYY-MM-DD": price}

    # Convert dicts to price lists for investment_return()
    prices1 = list(stock_data1.values())
    prices2 = list(stock_data2.values())

    # Compute returns
    investment1 = investment_return(prices1)
    investment2 = investment_return(prices2)

    labels = [stock_symbol1, stock_symbol2]
    values = [investment1, investment2]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Color selection
    from israelcities import colors
    first_color = st.selectbox("Choose a color for " + stock_symbol1, colors, index=0)
    available_colors = [color for color in colors if color != first_color]
    second_color = st.selectbox("Choose a color for " + stock_symbol2, available_colors, index=0)

    fig.update_traces(marker=dict(colors=[first_color, second_color]))

    # Random colors button
    if st.button("Generate random colors"):
        random.shuffle(colors)
        first_color = colors[0]
        second_color = colors[1]
        fig.update_traces(marker=dict(colors=[first_color, second_color]))

    fig.update_layout(title=translate_word('Return on each stock: $100'))

    st.plotly_chart(fig)



# --------------------------------------------------------
# FETCH TICKER INFO
# --------------------------------------------------------
@st.cache_data
def get_stock_info(symbol, info_type):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get(info_type, translate_word("Unavailable"))
    except Exception:
        return translate_word("Unavailable")


# --------------------------------------------------------
# MAIN COMPARISON FUNCTION
# --------------------------------------------------------
def Compare():
    st.title(translate_word("Stock Comparison"))

    with open("texts/stocks.json", "r") as json_file:
        stocks_dict = json.load(json_file)

    stock_symbol1 = st.selectbox(translate_word("Select the first stock:"), list(stocks_dict.keys()))
    stock_symbol2 = st.selectbox(translate_word("Select the second stock:"), list(stocks_dict.keys()),
                                 index=list(stocks_dict.keys()).index("APPLE"))

    min_date = datetime.date(2020, 1, 1)
    max_date = datetime.datetime.now() - datetime.timedelta(days=16)

    start_date = st.date_input(translate_word("Select start date:"),
                               min_value=min_date,
                               max_value=max_date,
                               value=min_date)

    end_date = datetime.datetime.now().date()

    st.button(translate_word('Compare'), on_click=click_button)

    if not st.session_state.clicked:
        return

    symbol1 = stocks_dict.get(stock_symbol1)
    symbol2 = stocks_dict.get(stock_symbol2)

    if not symbol1 or not symbol2 or symbol1 == symbol2:
        st.warning(translate_word("Please select two different stocks."))
        return

    # DISPLAY IMAGES
    for sym in [symbol1, symbol2]:
        try:
            st.image(f"company_logos/{sym.lower()}.png", width=200)
        except:
            try:
                st.image(f"company_logos/{sym.lower()}.jpg", width=200)
            except:
                st.caption("No image available")
        st.caption(sym)

    # FETCH DATA
    stock_data1 = get_stock_data(symbol1, start_date, end_date)
    stock_data2 = get_stock_data(symbol2, start_date, end_date)

    #PRICED DATA DICTIONARY
    price_data_1 = stock_data1['Close'].to_dict()[f'{symbol1}']
    prices_stock_data1 = {
        k.strftime("%Y-%m-%d"): v
        for k, v in price_data_1.items()
    }
    price_data_2 = stock_data2['Close'].to_dict()[f'{symbol2}']
    prices_stock_data2 = {
        k.strftime("%Y-%m-%d"): v
        for k, v in price_data_2.items()
    }



    if stock_data1 is None:
        st.error(f"No data available for {stock_symbol1}.")
        return
    if stock_data2 is None:
        st.error(f"No data available for {stock_symbol2}.")
        return

    # PLOT LINE GRAPH
    plot_stock_comparison(prices_stock_data1, prices_stock_data2, stock_symbol1, stock_symbol2)

    # FIXED FLOAT VALUES
    price1 = float(stock_data1['Close'].iloc[-1])
    price2 = float(stock_data2['Close'].iloc[-1])

    # DISPLAY WHICH STOCK IS HIGHER
    if price1 >= price2:
        st.success(translate_word(f"{stock_symbol1}'s value today: {price1:.2f}$"))
        st.error(translate_word(f"{stock_symbol2}'s value today: {price2:.2f}$"))
    else:
        st.success(translate_word(f"{stock_symbol2}'s value today: {price2:.2f}$"))
        st.error(translate_word(f"{stock_symbol1}'s value today: {price1:.2f}$"))

    display_stock_values(stock_symbol1, price1, stock_symbol2, price2)


    # TABLE DATA
    change1 = PrecentChange(prices_stock_data1,str(start_date),str(end_date))
    change2 = PrecentChange(prices_stock_data2,start_date,end_date)

    comparison_data = {
        translate_word(str(start_date)): [
            "Current Close", "Max Close", "Min Close", "Average Close", "Percent Of Change",
            "Market Cap", "Dividend Yield", "EPS", "P/E Ratio", "Volume",
            "Previous Close", "Open Price", "Forward P/E", "PEG Ratio",
            "Book Value", "Price/Sales", "Price/Book", "Beta", "Short Ratio",
            "Forward EPS", "Dividend Rate", "Ex-Dividend Date",
            "Last Split Factor", "Last Split Date",
        ],

        stock_symbol1: [
            f"{float(prices_stock_data1[change1.end]):.2f}",
            f"{max(prices_stock_data1.values()):.2f}",
            f"{min(prices_stock_data1.values()):.2f}",
            f"{(sum(prices_stock_data1.values()) / len(prices_stock_data1)):.2f}",
            f"{change1.change:.2f}%",

            get_stock_info(symbol1, "marketCap"),
            get_stock_info(symbol1, "dividendYield"),
            get_stock_info(symbol1, "trailingEps"),
            get_stock_info(symbol1, "trailingPE"),
            get_stock_info(symbol1, "volume"),
            get_stock_info(symbol1, "previousClose"),
            get_stock_info(symbol1, "open"),
            get_stock_info(symbol1, "forwardPE"),
            get_stock_info(symbol1, "pegRatio"),
            get_stock_info(symbol1, "bookValue"),
            get_stock_info(symbol1, "priceToSalesTrailing12Months"),
            get_stock_info(symbol1, "priceToBook"),
            get_stock_info(symbol1, "beta"),
            get_stock_info(symbol1, "shortRatio"),
            get_stock_info(symbol1, "forwardEps"),
            get_stock_info(symbol1, "dividendRate"),
            get_stock_info(symbol1, "exDividendDate"),
            get_stock_info(symbol1, "lastSplitFactor"),
            get_stock_info(symbol1, "lastSplitDate"),
        ],

        stock_symbol2: [
            f"{float(prices_stock_data2[change2.end]):.2f}",
            f"{max(prices_stock_data2.values()):.2f}",
            f"{min(prices_stock_data2.values()):.2f}",
            f"{(sum(prices_stock_data2.values()) / len(prices_stock_data2)):.2f}",
            f"{change2.change:.2f}%",

            get_stock_info(symbol2, "marketCap"),
            get_stock_info(symbol2, "dividendYield"),
            get_stock_info(symbol2, "trailingEps"),
            get_stock_info(symbol2, "trailingPE"),
            get_stock_info(symbol2, "volume"),
            get_stock_info(symbol2, "previousClose"),
            get_stock_info(symbol2, "open"),
            get_stock_info(symbol2, "forwardPE"),
            get_stock_info(symbol2, "pegRatio"),
            get_stock_info(symbol2, "bookValue"),
            get_stock_info(symbol2, "priceToSalesTrailing12Months"),
            get_stock_info(symbol2, "priceToBook"),
            get_stock_info(symbol2, "beta"),
            get_stock_info(symbol2, "shortRatio"),
            get_stock_info(symbol2, "forwardEps"),
            get_stock_info(symbol2, "dividendRate"),
            get_stock_info(symbol2, "exDividendDate"),
            get_stock_info(symbol2, "lastSplitFactor"),
            get_stock_info(symbol2, "lastSplitDate"),
        ]
    }

    with open(r"texts\stocks.json", "r") as r:
        super = json.load(r)

    stocks = [symbol1, symbol2]
    stocks[0] = [key for key, value in stocks_dict.items() if value == symbol1][0]
    stocks[1] = [key for key, value in stocks_dict.items() if value == symbol2][0]
    df_comparison = pd.DataFrame(comparison_data)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text(f"""Real time updated



                                Table
                                """)
        st.table(df_comparison)

    with col2:
        st.text("")
        plot_investment_return(prices_stock_data1, prices_stock_data2, stock_symbol1, stock_symbol2)
    from longtexts import terms
    terms()
    with st.spinner("Loading"):
        recommendations()

    username = st.text_input(translate_word("Enter your recommender name"))
    stock_recommend = st.selectbox(translate_word("Which stock do you recommend?"), stocks)
    stock_recommend = super[stock_recommend]
    st.caption(stock_recommend)
    recommendation = st.text_area(translate_word("Leave a comment"))
    rate = rating()
    st.button(translate_word('Send'), on_click=click_button)
    if st.session_state.clicked:
        try:
            data = update_recom(username, stock_recommend, recommendation, rate)
            if data != False:
                st.caption(translate_word("Comment uploaded."))

            else:
                st.caption("")
        except:
            st.caption(translate_word("Please fill all comments fields."))
    else:
        st.warning(translate_word("Failed to fetch data for one or both of the stocks. Please try again."))




def update_recom(username, stock_symbol, comment,rating='⭐⭐⭐⭐⭐', date=str(datetime.datetime.now())):
    connection = EncriptRecoms()
    if username == "" or comment == "":
        return False

    try:
        # encrypt + send
        to_ciphe = {
            f"{username}_{stock_symbol}":
            [stock_symbol, comment, rating, date]
        }

        connection.start_client(to_ciphe)
        from server import push_recommendation

        with st.status("🔐 Preparing SSAP protocol transmission...", expanded=True) as main_status:
            st.write("📦 Packing recommendation payload...")
            time.sleep(1)

            # Inner status for RSA
            with st.status("🔑 Fetching RSA public key...", expanded=True) as rsa_status:
                key = connection.fetch_public_key()
                pem_text = key.export_key().decode()

                mid = len(pem_text) // 2
                display = st.empty()
                display.code(pem_text[:mid])
                time.sleep(1)

                display.code(pem_text)
                time.sleep(1.5)

                rsa_status.update(
                    label="✅ Fetched RSA public key",
                    state="complete",
                    expanded=False
                )

            time.sleep(1.5)

            with st.status("🧮 Generating AES session key...", expanded=True) as aesStatus:
                time.sleep(1)
                st.code(connection._aesKey)
                time.sleep(1.5)
            aesStatus.update(
                label="✅ Generating AES session key completed successfully",
                state="complete",
                expanded=False
            )
            time.sleep(1.5)

            st.write("⚙️ Encrypting header + body with AES-ECB...")
            time.sleep(1.5)



            st.write("🗝️ Encrypting AES key using RSA-2048...")
            time.sleep(0.7)

            st.write("📡 Sending encrypted packet to server...")
            time.sleep(0.7)

            main_status.update(
                label="✅ SSAP transmission completed successfully",
                state="complete",
                expanded=False
            )

        push_recommendation(
            f"{username}_{stock_symbol}",
            [stock_symbol, comment, rating, date]
        )

        return to_ciphe

    except Exception as e:
        st.warning(e)
        return False



def pages():
    page = translate_word("Comparison")
    if page == translate_word("Comparison"):
        Compare()


if __name__ == "__main__":
    pages()