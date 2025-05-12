# # Treasury Yield Tracker
# ## Requirements and Import
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from fredapi import Fred
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
import os

# Load FRED API key
fred = Fred(api_key=st.secrets["FRED_API_KEY"])

# Streamlit application starts here
st.set_page_config(page_title="Treasury Yield Tracker", page_icon="📈")
st.title("Treasury Yield Tracker")
st.write("Here is a simple way to monitor the market interest rate.")


# Define series
series_ids = {
    "3 Month": "DGS3MO",
    "5 Year": "DGS5",
    "10 Year": "DGS10",
    "30 Year": "DGS30",
}

# Download from FRED
df_list = []
for label, code in series_ids.items():
    series = fred.get_series(code)
    df_list.append(series.rename(label).to_frame())

combined_df = pd.concat(df_list, axis=1)
combined_df.index.name = "Date"
combined_df = combined_df.dropna(how="all").reset_index()

# Output columns
output_list = list(series_ids.keys())

# ## Visualize the data

# Plotting the data with Streamlit
# Melt for plotting
melted_df = combined_df.melt(id_vars="Date", var_name="Ticker", value_name="Yield")
melted_df.dropna(subset=["Yield"], inplace=True)

# Filter data to only keep records from September 2022 onwards
melted_df = melted_df[melted_df["Date"] >= "2022-09-01"]

# Y-axis bounds
y_start = np.floor(melted_df["Yield"].min() * 2) / 2
y_end = np.ceil(melted_df["Yield"].max() * 2) / 2

# Make radio button less cramped by adding a space after each label
labels = [option + " " for option in output_list]

input_dropdown = alt.binding_radio(
    # Add the empty selection which shows all when clicked
    options=output_list + [None],
    labels=labels + ["All"],
    name="Ticker: ",
)
selection = alt.selection_point(
    fields=["Ticker"],
    bind=input_dropdown,
)

# Basic line chart
base_chart = (
    alt.Chart(melted_df)
    .mark_line()
    .encode(
        x="Date:T",
        y=alt.Y("Yield:Q", scale=alt.Scale(domain=[y_start, y_end])),
        color=alt.Color("Ticker:N", sort=output_list),
        # tooltip=['Ticker:N', 'Yield:Q']
    )
    .add_params(selection)
    .transform_filter(selection)
)

# Add interactive vertical line
selector = alt.selection_single(
    encodings=["x"],  # Selection based on x-axis (Close Date)
    on="mouseover",  # Trigger on mouseover
    nearest=True,  # Select the value nearest to the mouse cursor
    empty="none",  # Don't show anything when not mousing over the chart
)

rule = (
    alt.Chart(melted_df)
    .mark_rule()
    .encode(
        x="Date:T",
        opacity=alt.condition(selector, alt.value(1), alt.value(0)),
        color=alt.value("gray"),
    )
    .add_selection(selector)
)

# Add text annotations for Ticker and Yield at intersection
# This step might require adjusting depending on your DataFrame's structure
text = (
    base_chart.mark_text(align="left", dx=5, dy=-10, fontWeight="bold", fontSize=15)
    .encode(text=alt.condition(selector, "Yield:Q", alt.value(" "), format=".2f"))
    .transform_filter(selector)
)

# Assuming 'melted_df' has a 'Close Date' column in datetime format
start_date = melted_df["Date"].min()  # error code
end_date = melted_df["Date"].max()  # error code

# Generate quarter start dates within the range of your data
quarter_starts = pd.date_range(start=start_date, end=end_date, freq="QS").to_series()
quarter_starts_df = pd.DataFrame({"Date": quarter_starts})

# Chart for bold vertical lines at each quarter start
quarter_lines = (
    alt.Chart(quarter_starts_df)
    .mark_rule(
        color="gray", strokeWidth=1
    )  # Bold vertical lines, adjust color/strokeWidth as needed
    .encode(x="Date:T")
)

# Combine the charts
final_chart = alt.layer(base_chart, rule, text, quarter_lines)

# Draw a chart
st.altair_chart(
    final_chart,
    theme=None,
    # theme="streamlit",
    use_container_width=True,
)

# Filter for month ends
# month_end_data = df.resample("ME").last()
# month_end_data.set_index("Close Date", inplace=True)
combined_df["Date"] = pd.to_datetime(combined_df["Date"])

# Sort just in case
combined_df = combined_df.sort_values("Date")

# Group by year and month, then get last available row per group
combined_df["YearMonth"] = combined_df["Date"].dt.to_period("M")
month_end_data = combined_df.groupby("YearMonth").last().reset_index(drop=True)

# Filter from 2022 onwards
month_end_data = month_end_data[month_end_data["Date"] >= "2022-01-01"]
month_end_data = month_end_data.set_index("Date")
month_end_data.index = month_end_data.index.strftime("%Y-%m-%d")

# month_end_data = combined_df.set_index("Date").resample("M").last()
# month_end_data = month_end_data[month_end_data.index >= pd.to_datetime("2022-01-01")]
# month_end_data = month_end_data.set_index("Close Date")


with st.sidebar:
    st.subheader("Month-End Data Table")
    st.dataframe(month_end_data[output_list])

    todays_date = combined_df["Date"].max().strftime("%Y-%m-%d")
    st.write(f"Data source: FRED as of {todays_date}")
    st.markdown("[FRED Treasury Rates](https://fred.stlouisfed.org/categories/115)")

    st.markdown(
        """
        You can find the code and the documentation of the project in 
        [GitHub](https://github.com/DanTCIM/TreasuryYieldTracker.git).
    """
    )

# LLM section
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state or st.sidebar.button(
    "Clear conversation history"
):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome to Treasury Yield Tracker!"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Ask questions on the interest rate data."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = ChatOpenAI(temperature=0, model="gpt-4o", streaming=True)
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        combined_df,
        verbose=True,
        agent_type="openai-tools",
        allow_dangerous_code=True,
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
