# Treasury Yield Tracker
## 1. Description of the Project
Track 5-, 10-, 30-yr Treasury Yields and 13-week T-Bill using Yahoo Finance Data

The project automates the process of downloading Treasury rate data and displays the past interest rate since year-end 2022.  
It consists of sections for installing necessary libraries such as pandas, matplotlib, and yfinance, downloading the Treasury rate data using yfinance, preprocessing the data for visualization, and creating a line plot to visualize the data.

A user can adjust and edit the source tickers to monitor any market data from Yahoo Finance.
Source: [Yahoo Finance](https://finance.yahoo.com/)
- [^IRX](https://finance.yahoo.com/quote/%5EIRX/history): 13 week T-Bill
- [^FVX](https://finance.yahoo.com/quote/%5EFVX/history): 5 year Treasury
- [^TNX](https://finance.yahoo.com/quote/%5ETNX/history): 10 year Treasury
- [^TYX](https://finance.yahoo.com/quote/%5ETYX/history): 30 year Treasury

## 2. Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://treasurytracker.streamlit.app/)  
Please visit the Streamlit web app (https://treasurytracker.streamlit.app/) to see the implementation.

## 3. Codes

Here is the [Python code](code/TreasuryTrackerStreamlitApp.py) used for the Streamlit web app.  
Here is the [Jupyter Notebook](code/TreasuryYieldTracker.ipynb) that can run the code. 

## 4. Author
Dan Kim 

- [@LinkedIn](https://www.linkedin.com/in/dan-kim-4aaa4b36/)
- dan.kim.actuary@gmail.com (feel free to reach out with questions or comments)

## 5. Date
- Initially published on 2/17/2024
- The contents may be updated from time to time
  
## 6. License
This project is licensed under the Apache License 2.0- see the LICENSE.md file for details.

## 7. References
- https://finance.yahoo.com/
- https://treasurytracker.streamlit.app/
