import streamlit as st
import pandas as pd
from pages.utils.model_train import get_data,stationary_check,get_rolling_mean,get_differencing_order,fit_model,evaluate_model,get_forecast,inverse_scaling,scaling
from pages.utils.plotly_figure import plotly_table,Moving_Average_Forecast

st.set_page_config(
    page_title='Stock Prediction',
    page_icon='chart_with_downwards_trend',
    layout= 'wide'
)

st.title('Stock Prediction')

col1,col2,col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'TSLA')
rmse = 0

st.subheader('Prediction next 30 days Close Price for' +ticker)
close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)
differencing_order = get_differencing_order(rolling_price)
scaled_data,scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data,differencing_order)

st.write('**Model RMSE Score:**',rmse)

forecast = get_forecast(scaled_data,differencing_order)
forecast['Close'] = inverse_scaling(scaler , forecast['Close'])
st.write('#### Forecast Data (Next 30 Days)')

fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail,use_container_width=True)

forecast = pd.concat([rolling_price,forecast])

st.plotly_chart(Moving_Average_Forecast(forecast.iloc[150:]),use_container_width=True)

    # last_date = rolling_price.index[-1]

    # future_dates = pd.date_range(
    #     start=last_date,
    #     periods=len(forecast) + 1,
    #     freq='B'
    # )[1:]

    # forecast.index = future_dates

    # fig_tail = plotly_table(forecast.sort_index(ascending= True).round(3))
    # fig_tail.update_layout(height = 220)

    # st.plotly_chart(fig_tail,use_container_width= True)
    # forecast = pd.concat([rolling_price, forecast])
    # st.plotly_chart(Moving_Average_Forecast(forecast.iloc[-120:]),use_container_width= True)

#     historical_tail = rolling_price.iloc[150:]  # last 120 days
#     combined = pd.concat([historical_tail, forecast])
#     st.plotly_chart(
#     Moving_Average_Forecast(combined),
#     use_container_width=True
# )



    