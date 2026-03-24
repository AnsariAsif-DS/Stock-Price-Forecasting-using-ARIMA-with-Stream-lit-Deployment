import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta #technincal analysis or time series analysis
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import candlestick,MACD,RSI,Moving_Average,close_chart,filtered_data

st.set_page_config(
    page_title='Stock Analysis',
    page_icon='📃',
    layout='wide'
)
st.title('Stock Analysis')

col1 , col2 , col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock Ticker','TSLA')
with col2:
    start_date = st.date_input('Choose start date', datetime.date(today.year-1,today.month,today.day))
with col3:
    end_date = st.date_input('Choose end date',datetime.date(today.year,today.month,today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write('**Sector:**',stock.info['sector'])
st.write('**Full Time Employees:**',stock.info['fullTimeEmployees'])
st.write('**Website:**',stock.info['website'])
st.write('**Market Cap:**',stock.info['marketCap'])
st.write('**Country:**',stock.info['country'])
st.write('**Address:**',stock.info['address1'])
st.write('**Phone:**',stock.info['phone'])

col1 , col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index = ['marketCap','Beta','EPS','PE Ratio','Total Debt'])
    df[''] = [stock.info['marketCap'],stock.info['beta'],stock.info['trailingEps'],stock.info['trailingPE'],stock.info['totalDebt']]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)

with col2:
    df = pd.DataFrame(index = ['Quick Ratio','Revenue per share','Profit Margin','Debt to Equity','Return on Equity'])
    df[''] = [stock.info['quickRatio'],stock.info['revenuePerShare'],stock.info['profitMargins'],stock.info['debtToEquity'],stock.info['returnOnEquity']]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)

data = yf.download(ticker , start= start_date, end = end_date)

def clean_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

data = clean_columns(data)

col1,col2,col3 = st.columns(3)

last_price = float(data['Close'].iloc[-1])
prev_price = float(data['Close'].iloc[-2])

daily_change = last_price - prev_price

col1.metric(
    "Daily Change",
    round(last_price,2),
    round(daily_change,2)
)

last_10_df = data.tail(10).sort_index(ascending=False).round(3)
#last_10_df = last_10_df.reset_index(drop=True)
fig_df = plotly_table(last_10_df)

st.write('### Historical data (for last 10 days)')
st.plotly_chart(fig_df,use_container_width=True)


col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])
num_period = ''

with col1:
    if st.button('5D'):
        num_period = '5D'
with col2:
    if st.button('1M'):
        num_period = '1M'
with col3:
    if st.button('6M'):
        num_period = '6M'
with col4:
    if st.button('YTD'):
        num_period = 'YTD'
with col5:
    if st.button('1Y'):
        num_period = '1Y'
with col6:
    if st.button('5Y'):
        num_period = '5Y'
with col7:
    if st.button('MAX'):
        num_period = 'MAX'
        
period = num_period if num_period != '' else 'MAX'

col1,col2,col3 = st.columns([1,1,4])

with col1:
    chart_type = st.selectbox('',('Candle Stick','Line Chart'))

with col2:
    if chart_type =='Candle Stick':
        indicators = st.selectbox('',('RSI','MACD'))
    else:
        indicators = st.selectbox('',('RSI','Moving Average','MACD'))

ticker_ = yf.Ticker(ticker)

new_df1 = data.copy()
data1 = data.copy()


if num_period  == '':

    if chart_type == 'Candle Stick' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1,'1Y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1Y'),use_container_width=True)

    if chart_type == 'Candle Stick' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1,'1Y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1Y'),use_container_width=True)

    if chart_type == 'Line Chart' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1,'1Y'),use_container_width=True)
        st.plotly_chart(RSI(data1,'1Y'),use_container_width=True)

    if chart_type == 'Line Chart' and indicators == 'Moving Average':
        st.plotly_chart(Moving_Average(data1,'1Y'),use_container_width=True)

    if chart_type == 'Line Chart' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1,'1Y'),use_container_width=True)
        st.plotly_chart(MACD(data1,'1Y'),use_container_width=True)

else:

    if chart_type == 'Candle Stick' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1,num_period),use_container_width=True)
        st.plotly_chart(RSI(new_df1,num_period),use_container_width=True)

    if chart_type == 'Candle Stick' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1,num_period),use_container_width=True)
        st.plotly_chart(MACD(new_df1,num_period),use_container_width=True)

    if chart_type == 'Line Chart' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1,num_period),use_container_width=True)
        st.plotly_chart(RSI(new_df1,num_period),use_container_width=True)

    if chart_type == 'Line Chart' and indicators == 'Moving Average':
        st.plotly_chart(Moving_Average(new_df1,num_period),use_container_width=True)

    if chart_type == 'Line Chart' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1,num_period),use_container_width=True)
        st.plotly_chart(MACD(new_df1,num_period),use_container_width=True)

