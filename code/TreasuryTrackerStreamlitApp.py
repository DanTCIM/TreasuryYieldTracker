#!/usr/bin/env python
# coding: utf-8
# # Treasury Yield Tracker
# ## Requirements and Import
import streamlit as st
import altair as alt
import yfinance as yf
import pandas as pd
import numpy as np

# Streamlit application starts here
st.title('Treasury Yield Tracker')
# Example of including a link in Streamlit
link = "https://github.com/DanTCIM/TreasuryYieldTracker.git"
st.write("Here is a simple way to monitor the market interest rate.")
st.markdown(f"You can find the code and the documentation of the project in [GitHub]({link}).")

# ## Download Treasury rate data
treasury_rate_data = yf.download("^IRX ^FVX ^TNX ^TYX", start="2022-12-29", end=None)#, interval="1mo")
df = treasury_rate_data["Adj Close"]

# Convert the data
# Add Close Date information
df = df.copy()
df['Close Date'] = df.index.strftime('%Y-%m-%d')

# Rename column names
new_column_names = {'^IRX': '13-week T-Bill',
                    '^FVX': '5-yr Treasury',
                    '^TNX': '10-yr Treasury',
                    '^TYX': '30-yr Treasury'}

df = df.rename(columns = new_column_names)

# Output columns
output_list = ['13-week T-Bill', '5-yr Treasury', '10-yr Treasury', '30-yr Treasury']

# ## Visualize the data

# Plotting the data with Streamlit
# Melt the DataFrame to convert it to long format
melted_df = df.melt(id_vars='Close Date', var_name='Ticker', value_name='Yield')

# Define range:
# Determine the minimum and maximum values of 'Yield'
min_y_value = melted_df['Yield'].min()
max_y_value = melted_df['Yield'].max()
# Calculate the starting and end points for the Y-axis range
y_start = np.floor(min_y_value*2)/2
y_end = np.ceil(max_y_value*2)/2

# Create a common chart object
chart = alt.Chart(melted_df).mark_line().encode(
    x='Close Date:T',
    y=alt.Y('Yield:Q', scale=alt.Scale(domain=[y_start, y_end])), 
    #y='Yield:Q',
    color=alt.Color('Ticker:N', sort=output_list),
    tooltip=['Close Date:T', 'Ticker:N', 'Yield:Q']
)

# Draw a chart
st.altair_chart(chart, 
                theme=None, 
                #theme="streamlit", 
                use_container_width=True)

# Filter for month ends
month_end_data = df.resample('ME').last()
month_end_data.set_index('Close Date', inplace=True)

# Show the filtered DataFrame
# Displaying a table
st.subheader('Month-End Data Table')
st.dataframe(month_end_data[output_list])  # Display the DataFrame as a table

# Source
todays_date = df['Close Date'].iloc[-1]

link1 = "https://finance.yahoo.com/quote/%5EIRX/history"
link2 = "https://finance.yahoo.com/quote/%5EFVX/history"
link3 = "https://finance.yahoo.com/quote/%5ETNX/history"
link4 = "https://finance.yahoo.com/quote/%5ETYX/history"

st.write(f"Data source: Yahoo Finance as of {todays_date}")
st.write(f"Adjusted Close from Tickers: [^IRX]({link1}) (13-week T-Bill), [^FVX]({link2}) (5-yr Treasury), [^TNX]({link3}) (10-yr Treasury), [^TYX]({link4}) (30-yr Treasury)")