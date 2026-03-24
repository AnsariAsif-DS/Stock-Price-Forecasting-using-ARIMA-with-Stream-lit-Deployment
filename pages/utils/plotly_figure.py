import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime
import pandas as pd

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = "#5b81ba"
    rowOddColor = "#C5CFDA"
    fig = go.Figure(
        data=[go.Table(
            header = dict(
                values=['<b><b>']+["<b>"+str(i)[:10]+"</b>" for i in dataframe.columns],
                line_color = '#0078ff', fill_color = '#0078ff',
                align = 'center',font = dict(color = 'white',size = 15),height = 35 
                ),
            cells = dict(
                values=[
                    ["<b>"+str(i)+"</b>" for i in dataframe.index]]
                    + [dataframe[i] for i in dataframe.columns], fill_color = [[rowEvenColor,rowOddColor]],
                    align = 'left',line_color = ['white'],font = dict(color = ['black'],size = 15)
                )
        )]
    )
    fig.update_layout(height = 400,margin = dict(l = 0,r = 0,t = 0,b = 0))
    return fig

def filtered_data(dataframe,num_period):

    if dataframe.empty:
        return dataframe

    last_date = dataframe.index[-1]

    if num_period == '1M':
        date = last_date - dateutil.relativedelta.relativedelta(months=1)
    elif num_period == '5D':
        date = last_date - dateutil.relativedelta.relativedelta(days=5)
    elif num_period == '6M':
        date = last_date - dateutil.relativedelta.relativedelta(months=6)
    elif num_period == '1Y':
        date = last_date - dateutil.relativedelta.relativedelta(years=1)
    elif num_period == '5Y':
        date = last_date - dateutil.relativedelta.relativedelta(years=5)
    elif num_period == 'YTD':
        date = datetime.datetime(last_date.year, 1, 1)
    else:
        return dataframe

    return dataframe[dataframe.index >= date]

def close_chart(dataframe,num_period = False):
    if num_period:
        dataframe = filtered_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['Open'],
                             mode='lines',name='Open', line = dict(width = 2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['Close'],
                             mode='lines',name='Close', line = dict(width = 2,color = "#9fff5a")))    
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['High'],
                             mode='lines',name='High', line = dict(width = 2,color = "#68419a")))
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['Low'],
                             mode='lines',name='Low', line = dict(width = 2,color = "#904523")))  
    fig.update_xaxes(rangeslider_visible = True)
    fig.update_layout(height = 500,margin = dict(l = 0,r = 20,t = 20,b = 0),plot_bgcolor = 'white',paper_bgcolor = '#e1efff',
                      legend = dict(xanchor = 'right',yanchor = 'top'))      
    return fig

def candlestick(dataframe,num_period):
    dataframe = filtered_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x = dataframe.index,open = dataframe['Open'],low = dataframe['Low'],
                                 close = dataframe['Close'],high = dataframe['High']))      
    fig.update_layout(showlegend = False,height = 500,margin = dict(l = 0,r = 20,t = 20,b = 0),plot_bgcolor = 'white',paper_bgcolor = '#e1efff')
    return fig

def RSI(dataframe,num_period):

    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filtered_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe.index,
                             y = dataframe.RSI, name='RSI',marker_color = 'orange',line = dict(width = 2, color = 'orange')))
    fig.add_trace(go.Scatter(x = dataframe.index,
                             y = [70] * len(dataframe), name = 'Overbought',marker_color = 'red',
                             line = dict(width = 2,color = 'red',dash = 'dash')))
    fig.add_trace(go.Scatter(x = dataframe.index,
                             y = [30] * len(dataframe),
                             fill='tonexty',name = 'Oversold',marker_color = '#79da84',line=dict(width = 2,color = '#79da84',dash = 'dash')))
    fig.update_layout(yaxis_range = [0,100],
                      height = 200,plot_bgcolor = 'white',paper_bgcolor = '#e1efff',
                      margin = dict(l=0,r = 0,t = 0,b= 0),
                      legend = dict(orientation = 'h', yanchor = 'top',y = 1.02,xanchor = 'right',x = 1))
    return fig

def Moving_Average(dataframe,num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'],50)
    dataframe = filtered_data(dataframe,num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['Close'],
                             mode='lines',name='Close', line = dict(width = 2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['Open'],
                             mode='lines',name='Open', line = dict(width = 2,color = "#9fff5a")))    
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['High'],
                             mode='lines',name='High', line = dict(width = 2,color = "#68419a")))
    fig.add_trace(go.Scatter(x= dataframe.index,y = dataframe['Low'],
                             mode='lines',name='Low', line = dict(width = 2,color = "#904523"))) 
    fig.add_trace(go.Scatter(x = dataframe.index,y = dataframe['SMA_50'], 
                             mode = 'lines',name='SMA_50',line = dict(width = 2,color = 'black'))) 
    fig.update_xaxes(rangeslider_visible = True)
    fig.update_layout(height = 500,margin = dict(l = 0,r = 20,t = 20,b= 0),
                      plot_bgcolor = 'white',paper_bgcolor = '#e1efff',
                      legend = dict(
                          yanchor = 'top',
                          xanchor = 'right'
                      ))
    return fig

def MACD(dataframe,num_period):
    macd_df = pta.macd(dataframe['Close'])

    dataframe['macd'] = macd_df.iloc[:, 0]
    dataframe['macd_signal'] = macd_df.iloc[:, 1]
    dataframe['macd_hist'] = macd_df.iloc[:, 2]

    dataframe = filtered_data(dataframe,num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x= dataframe.index,
        y = dataframe['macd'], name='RSI',marker_color ='orange',line = dict(width = 2,color = 'orange')
    ))
    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['macd_signal'],
        name='Overbought',marker_color = 'red',line=dict(width = 2,color = 'red',dash = 'dash')
    ))
    colors = ['red' if val < 0 else 'green' for val in dataframe['macd_hist']]
    fig.add_trace(go.Bar(
        x=dataframe.index,
        y=dataframe['macd_hist'],
        marker_color=colors,
        name='Histogram'
    ))
    fig.update_layout(
        height = 200,margin = dict(l = 0,r = 0,t = 0,b= 0),
        plot_bgcolor = 'white',paper_bgcolor = '#e1efff',
        legend = dict(orientation = 'h',yanchor = 'top',
                          y = 1.02,
                          xanchor = 'right',
                          x = 1
                      ))
    return fig

def Moving_Average_Forecast(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = forecast.index[:-30],y = forecast['Close'].iloc[:-30],
                             mode='lines',
                             name='Close Price',
                             line= dict(width = 2,color = 'black')))
    fig.add_trace(go.Scatter(x= forecast.index[-31:],y = forecast['Close'].iloc[-31:],
                             name = 'Future Close Price',
                             mode='lines',
                             line = dict(width = 2,color = 'red')))
    
    fig.update_xaxes(rangeslider_visible = True)
    fig.update_layout(height = 500,margin = dict(l=0, r=20,t=20,b=0),plot_bgcolor = 'white',
                      paper_bgcolor = '#e1efff',legend =dict(yanchor= 'top',xanchor = 'right'
                                                             ) )
    return fig


