#!/usr/bin/env python
# coding: utf-8

# # Treasury Yield Tracker

# ## Requirements and Import

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ## Download Treasury rate data

treasury_rate_data = yf.download("^IRX ^FVX ^TNX ^TYX", start="2022-12-29", end=None)#, interval="1mo")
todays_date = datetime.now().strftime('%Y-%m-%d')
df = treasury_rate_data["Adj Close"]

# ## Visualize the data

# Streamlit application starts here
st.title('Treasury Yield Tracker')
# Example of including a link in Streamlit
link = "https://github.com/DanTCIM/TreasuryYieldTracker.git"
st.write("Here is a simple way to monitor the market interest rate.")
st.markdown(f"You can find the code in [GitHub]({link}).")                    
                    
# Plotting the data with Streamlit
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df['^IRX'], label='13-week T-Bill', color='darkblue')
ax.plot(df.index, df['^FVX'], label='5-yr Treasury', color='orange')
ax.plot(df.index, df['^TNX'], label='10-yr Treasury', color='tomato')
ax.plot(df.index, df['^TYX'], label='30-yr Treasury', color='darkred')
ax.set_xlabel('Date')
ax.set_ylabel('Yield')
ax.legend()
ax.grid(True)

# Use Streamlit's method to display the figure
st.pyplot(fig)

st.write(f"Data source: Yahoo Finance as of {todays_date}")
st.write("Tickers: ^IRX: 13-week T-Bill, ^FVX: '5-yr Treasury, ^TNX: '10-yr Treasury, ^TYX: 30-yr Treasury")

# Filter for quarter ends
month_end_data = df.resample('M').last()

# Rename column names
new_column_names = {'^IRX': '13-week T-Bill',
                    '^FVX': '5-yr Treasury',
                    '^TNX': '10-yr Treasury',
                    '^TYX': '30-yr Treasury'}

month_end_data = month_end_data.rename(columns = new_column_names)

# Rerder columns
desired_order = ['13-week T-Bill', '5-yr Treasury', '10-yr Treasury', '30-yr Treasury']

# Show the filtered DataFrame
# Displaying a table
st.subheader('Month-End Data Table')
st.dataframe(month_end_data[desired_order])  # Display the DataFrame as a table








