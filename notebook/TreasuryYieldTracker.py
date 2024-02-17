#!/usr/bin/env python
# coding: utf-8

# # Treasury Rate Time-Series Visualization

# ## Introduction

# The Jupyter notebook automates the process of downloading Treasury rate data and displaying the past 10-year rate time-series data with a monthly timestep over the past 12 months. It consists of sections for installing necessary libraries such as pandas, matplotlib, and yfinance, downloading the Treasury rate data using yfinance, preprocessing the data for visualization, and creating a line plot to visualize the data. The notebook fulfills the prompt "/generate I want to automatically download Treasury rate and show the past 10-yr rate time-series data using monthly timestep for the past 12-month period."

# ## Requirements
# yfinance

# In[2]:

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# ## Download Treasury rate data

# In[3]:


# Download Treasury rate data from Yahoo Finance for the past 12 months with monthly timestep
#^IRX: 1-Year Eris SOFR Swap Futures,M (YIAH24.CBT)
#^FVX five year Treasury
#^TNX 10 year Treasury
#^TYX 30 year Treasury

treasury_rate_data = yf.download("^IRX ^FVX ^TNX ^TYX", start="2022-12-29", end=None)#, interval="1mo")


# In[4]:


# Display the downloaded Treasury rate data
df = treasury_rate_data["Adj Close"]
#df.info()
#print(df)


# ## Visualize the data

# In[6]:
# Streamlit application starts here
st.title('Treasury Yield Tracker')

# Plotting the data with Streamlit
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df['^IRX'], label='1-yr SOFR', color='darkblue')
ax.plot(df.index, df['^FVX'], label='5-yr Treasury', color='orange')
ax.plot(df.index, df['^TNX'], label='10-yr Treasury', color='tomato')
ax.plot(df.index, df['^TYX'], label='30-yr Treasury', color='darkred')
ax.set.xlabel('Date')
ax.set.ylabel('Yield')
ax.legend()
ax.grid(True)

# Use Streamlit's method to display the figure
st.pyplot(fig)

# In[7]:


# Filter for quarter ends
quarter_end_data = df.resample('M').last()

# Rename column names
new_column_names = {'^IRX': '1-yr SOFR',
                    '^FVX': '5-yr Treasury',
                    '^TNX': '10-yr Treasury',
                    '^TYX': '30-yr Treasury'}

quarter_end_data = quarter_end_data.rename(columns = new_column_names)

# Rerder columns
desired_order = ['1-yr SOFR', '5-yr Treasury', '10-yr Treasury', '30-yr Treasury']

# Show the filtered DataFrame
#print(quarter_end_data[desired_order])
# Displaying a table
st.subheader('Monthly Table')
st.dataframe(quarter_end_data[desired_order])  # Display the DataFrame as a table






