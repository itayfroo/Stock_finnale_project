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