import streamlit as st
import pickle
import pandas as pd
from datetime import datetime
import plotly.express as px 

# apple_df=pd.read_csv('AAPL_stock_data.csv',parse_dates=True,index_col='Date',usecols=['Date','Close'])

# apple_df=apple_df.asfreq('D').fillna(apple_df.bfill())
# apple_df=apple_df[1098:]

st.set_page_config(layout="wide")

st.title('Forecasting Apple Stock Price Using fbprophet')

# Load the data from the pickle file
future_close_df = pickle.load(open('future_close_data_prophet.pkl', 'rb'))

# Ensure the 'date' column is of datetime type
future_close_df['date'] = pd.to_datetime(future_close_df['date']).dt.date

# Streamlit date input
selected_date = st.date_input('Select a Day', 
                              min_value=datetime(2024, 7, 13).date(), 
                              max_value=datetime(2027, 7, 15).date())

# Find the forecast value for the selected date
forecast_value = future_close_df.loc[future_close_df['date'] == selected_date, 'close']

# Check if the selected date has a forecast value
if not forecast_value.empty:
    forecast_value = round(forecast_value.values[0], 2)
    st.write(f"Forecast Stock Price:  **{forecast_value}$**")
else:
    st.write(f"No forecast value available for {selected_date}")

# st.dataframe(future_close_df)


# Create a sample apple_df for demonstration purposes
apple_df=pd.read_csv('AAPL_stock_data.csv',parse_dates=True,usecols=['Date','Close'])
apple_df.columns=['date','close']
# Add a column to indicate whether the data is actual or forecasted
apple_df['source'] = 'Actual'
future_close_df['source'] = 'Forecasted'

# Combine the dataframes
combined_df = pd.concat([apple_df, future_close_df], ignore_index=True)

# Create the combined line plot
fig = px.line(combined_df, x='date', y='close', color='source', 
              labels={'close': 'Stock Price', 'date': 'Date', 'source': 'Data Source'},
              title='Actual vs Forecasted Stock Prices')

# Display the plot in Streamlit
st.plotly_chart(fig)
