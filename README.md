# Treasury Yield Tracker
## 1. Description of the Project

The **Treasury Yield Tracker** is a Streamlit web application that allows users to visualize historical Treasury yield data using the [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/) API.

The project automates:
- Downloading and aggregating market interest rates (3M, 5Y, 10Y, 30Y)
- Displaying clean, interactive charts using Altair
- Providing a business-friendly view with monthly data sampled at the **last available business day** of each month since 2022
- Optional integration with an LLM agent to ask natural language questions about the data

### Key Features
- Clean and responsive Streamlit UI
- Interactive radio filter for yield term selection
- Sidebar table with latest month-end yield values
- Automatic detection of most recent FRED update
- LangChain + OpenAI-powered chat for data exploration

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
- [FRED: Federal Reserve Economic Data](https://fred.stlouisfed.org/)
- [Altair: Declarative Visualization in Python](https://altair-viz.github.io/)
