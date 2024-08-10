# Stock Analyzer App

Welcome to the Stock Analyzer App! This web application is built using Streamlit and provides tools for analyzing stock prices, making predictions, and exploring investment opportunities.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Requirements](#Requirements)
- [Progrramers](#Pro-Grammers)
- [Notes](#Notes)
### Pro-Grammers

- Mark Kolesnik
- Itay Froomer
- Lior Mishaiev
## Features

- Analyze stock prices and trends.
- Make predictions using Linear Regression and LSTM models.
- Explore investment opportunities based on historical stock data.
- Give and get recommendations about stocks.
- Cross shares in order to determine which is best suited for you.


### Prerequisites

Make sure you have the following installed:

- Python 3.6 or later
- pip (Python package installer)
### Installation

1. Clone the repository:

   git clone [git@github.com:itayfroo/Stock_finnale_project.git](#)

   Can also fork from https://github.com/itayfroo/Stock_finnale_project.git
   *****************************************************************
2. Install packages - pip install -r requirements.txt
    - [Packages](#Requirements)
  
   *****************************************************************
3. Run the app in the PowerShell:

    - [streamlit run codes\main.py](#)
   *****************************************************************

### Requirements
- streamlit
- requests
- yfinance
- pandas
- plotly
- scikit-learn
- numpy
- tensorflow
- datetime
- googletrans==4.0.0-rc1
- google_trans_new


### Notes
- If you can't open venv(ExecutionPolicy is restricted) run
  [Set-ExecutionPolicy -Scope CurrentUser RemoteSigned](#) in the PowerShell.

- **Classes**:
   1. `Recommendations` (recommendations.py): Handles everything about user recommendations.
   2. `PrecentChange` (stockCompare.py): Calculates the percent change of the close price of stocks.
   3. `Scripts` (welcome.py): Displays the scripts of the project.
   4. `RemoveUser` (signIn.py): Allows the option to remove a registered user.


