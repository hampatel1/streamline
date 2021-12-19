import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt

st.sidebar.title("Options")
option = st.sidebar.selectbox('Which Dashboard?', ('Equity', 'Crypto', 'Stockwits', 'Pattern'), 0)
st.title(option)


if option == 'Equity':
    symbol = st.sidebar.text_input("Ticker", value='MSFT', max_chars=None, key=None, type='default')
    st.subheader('**Company Overview**')

    # date selection
    start_date = st.sidebar.text_input("Start Date", value='2021-01-01', type='default')
    end_date = st.sidebar.text_input("End Date", value=dt.datetime.date(dt.datetime.now()), type='default')

    # get data
    data = yf.download(symbol, start_date, end_date)

    # line chart
    st.subheader('Stock Closing Price')
    st.set_option('deprecation.showPyplotGlobalUse', False)

    plt.plot(data.index, data['Adj Close'], color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    st.pyplot()

    # candle chart
    st.subheader('Candlestick Closing Price')
    chart = st.checkbox("Press if you want to show candlestick chart")
    if chart:
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Adj Close'],
                        name=symbol)])

        fig.update_layout(width=700, height=700)
        st.plotly_chart(fig, use_container_width=True)

    # get daily volume for searched ticker
    st.subheader("Daily Volume")
    st.bar_chart(data['Volume'])

    # inset dataframe
    st.subheader('Dataframe')
    st.write(data)


if option == 'Stockwits':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])


