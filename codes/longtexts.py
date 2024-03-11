import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from chooseLangauge import translate_word

def display_lstm_info():
    st.markdown(translate_word("""
        Long Short-Term Memory (LSTM) is a type of recurrent neural network (RNN) architecture that is designed to overcome the limitations of traditional RNNs in capturing long-term dependencies in sequential data. RNNs, in theory, can learn from past information to make predictions on future data points, but in practice, they often struggle to learn and remember information from distant past time steps due to the vanishing gradient problem.

LSTM was introduced to address the vanishing gradient problem by incorporating memory cells and gating mechanisms. The key components of an LSTM cell include:

1. **Cell State (Ct):** This is the memory of the cell. It can retain information over long sequences, allowing the model to capture long-term dependencies.

2. **Hidden State (ht):** This is the output of the cell and is used for making predictions. It can selectively expose parts of the cell state.

3. **Three Gates:**
   - **Forget Gate (ft):** Decides what information to throw away from the cell state.
   - **Input Gate (it):** Updates the cell state with new information.
   - **Output Gate (ot):** Controls what parts of the cell state should be output.

LSTM's ability to selectively learn, forget, and store information makes it particularly effective for tasks involving sequences, such as time series forecasting, natural language processing, and speech recognition.

In the context of time series prediction, like predicting stock prices, LSTM models are well-suited to capture patterns and dependencies in historical data and make predictions for future values based on that learned context.
    """))

def linear_Regression(stock_data):
    st.markdown(translate_word("""
Linear regression is a statistical method used for modeling the relationship between a dependent variable and one or more independent variables by fitting a linear equation to the observed data. The most common form is simple linear regression, which deals with the relationship between two variables, while multiple linear regression deals with two or more predictors.

The linear regression equation has the form:

Y =  β(0)+ β(1)X(1) + β(2)X(2) + ... + β(n)x(n) +  ε

Here:
- Y  is the dependent variable.
- X(1), X(2), ..., X(n) are independent variables.
- β(0) is the intercept.
- β(1), β(2)...,β(N) are the coefficients representing the relationship between the independent variables and the dependent variable.
- ε is the error term, representing the unobserved factors that affect the dependent variable.

The goal of linear regression is to find the values of the coefficients that minimize the sum of the squared differences between the observed and predicted values. Once the model is trained, it can be used to make predictions for new data.

Linear regression is widely used in various fields for tasks such as predicting stock prices, housing prices, sales forecasting, and many other applications where understanding the relationship between variables is crucial.  
                """))
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']
    data = y
    model = LinearRegression()
    model.fit(X, y)

    # Predictions for the entire range
    predictions = model.predict(X)

    # Plot the actual and predicted values
    fig_lr = px.line(X, x='Days', y=y, title=translate_word('Actual vs Predicted (Linear Regression)'))
    fig_lr.add_scatter(x=X['Days'], y=predictions, mode='lines', name='Predicted')
    fig_lr.update_xaxes(title_text=translate_word('Days'))
    fig_lr.update_yaxes(title_text=translate_word('Stock Price (USD)'))

    st.plotly_chart(fig_lr)
    m = (y.iloc[-1] - y.iloc[0]) / 707
    st.write(translate_word("The y(x) linear function:"))
    st.write(f"Y = {float(m)}x + {float(y.iloc[0])}")

def terms():
    with st.expander(translate_word('Terms 💡')):
        st.markdown("""
            - **Max Close**: 
              - Represents the highest closing price observed for the stock during the specified time period. 
              - Indicates the peak value reached by the stock's price, reflecting high investor optimism or demand.
              
            - **Min Close**: 
              - The lowest closing price recorded for the stock within the specified time frame. 
              - Signifies the lowest point reached by the stock's price, indicating low investor sentiment or demand.
              
            - **Average Close**: 
              - The mean value of all closing prices recorded for the stock during the specified time period. 
              - Provides a balanced view of the stock's performance over the period.
              
            - **Percent of Change**: 
              - Indicates the percentage change in the stock's price from the beginning to the end of the specified time period. 
              - Measures the extent of price movement, showing if the stock has appreciated or depreciated over the period.
              
            - **Market Cap**: 
              - The total value of a company's outstanding shares of stock, calculated by multiplying the current stock price by the total number of outstanding shares. 
              - Represents the market's valuation of the company, used to compare the sizes of different companies.
              
            - **Dividend Yield**: 
              - Shows how much a company pays out in dividends each year relative to its stock price, expressed as a percentage. 
              - Indicates the return on investment in the form of dividends.
              
            - **EPS (Earnings Per Share)**: 
              - A company's net profit divided by the number of outstanding shares, representing the portion of profit allocated to each outstanding share of common stock. 
              - Used by investors to assess the company's profitability.
              
            - **P/E Ratio (Price-to-Earnings Ratio)**: 
              - The ratio of a company's current stock price to its earnings per share (EPS). 
              - Indicates how much investors are willing to pay for each dollar of the company's earnings.
              
            - **Volume**: 
              - The total number of shares traded during a given period.
              - Provides insight into the liquidity and interest in a particular stock.
              
              
            - **Previous Close**: 
              - The closing price of the stock in the previous trading session.
              - Helps investors understand how the stock performed relative to the last trading day.
              
            - **Open Price**: 
              - The price at which a stock first trades upon the opening of the market.
              - Provides insight into market sentiment at the beginning of the trading day.
              
            - **Forward P/E**: 
              - The P/E ratio using estimated future earnings rather than trailing earnings.
              - Offers insight into the company's future earnings potential.
              
            - **PEG Ratio (Price/Earnings to Growth Ratio)**: 
              - The ratio of the P/E ratio to the annual EPS growth rate.
              - Helps investors assess the stock's valuation relative to its growth prospects.
              
            - **Book Value**: 
              - The total value of a company's assets that shareholders would theoretically receive if the company were liquidated.
              - Offers insight into the company's underlying value per share.
              
            - **Price/Sales**: 
              - The ratio of a company's market capitalization to its revenue.
              - Helps investors assess the company's valuation relative to its sales.
              
            - **Price/Book**: 
              - The ratio of a company's stock price to its book value per share.
              - Indicates whether a stock is undervalued or overvalued relative to its book value.
              
            - **Beta**: 
              - A measure of a stock's volatility in relation to the overall market.
              - Helps investors assess the risk associated with investing in a particular stock.
              
            - **Short Ratio**: 
              - The ratio of the number of shares sold short to the average daily trading volume.
              - Indicates market sentiment, with a higher ratio suggesting more bearish sentiment.
              
            - **Forward EPS (Earnings Per Share)**: 
              - The forecasted earnings per share for a company for the next fiscal period.
              - Provides insight into expected future profitability.
              
            - **Dividend Rate**: 
              - The annualized dividend payout per share.
              - Indicates the amount of income investors can expect to receive from dividends.
              
            - **Ex-Dividend Date**: 
              - The date on which a stock begins trading without the dividend included in its price.
              - Determines eligibility for receiving the upcoming dividend payment.
              
            - **Last Split Factor**: 
              - The ratio by which a stock was split in its most recent stock split.
              - Provides information about the magnitude of the stock split.
              
            - **Last Split Date**: 
              - The date on which a stock underwent its most recent stock split.
              - Indicates the timing of the split event.
        """)
