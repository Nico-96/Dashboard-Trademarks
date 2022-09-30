from datetime import datetime, date, timedelta
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# 10 Criptos
BTC = "BTC/USD"
ETH = "ETH/USD"
SOL = "SOL/USD"
ADA = "ADA-PERP"
DOT = "DOT/USD"
MATIC = "MATIC/USD"
EGLD = "EGLD-PERP"
DOGE = "DOGE/USD"
XRP = "XRP/USD"
UNI = "UNI/USD"

URL_BASE = "https://ftx.com/api"

def get_historical(coin, start_date, end_date, resolution = 86400):

    if coin == "EGLD" or coin == 'DOT' or coin == 'ADA':
        coin = coin + '-PERP'
    else:
        coin = coin + '/USD'

    start_time = pd.to_datetime(start_date.strftime("%Y-%m-%d")).timestamp()
    end_time = pd.to_datetime(end_date.strftime("%Y-%m-%d")).timestamp()

    url =  f'{URL_BASE}/markets/{coin}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
    res = requests.get(url).json()
    result = pd.DataFrame(res['result'])
    
    result['date'] = pd.to_datetime(result['time']/1000, unit = 's', origin = 'unix')
    result.drop(['startTime', 'time'], axis = 1, inplace = True)
    return result

def get_market(coin: str):

    if coin == "EGLD" or coin == 'DOT' or coin == 'ADA':
        coin = coin + '-PERP'
    else:
        coin = coin + '/USD'

    url =  f'{URL_BASE}/markets/{coin}'
    res = requests.get(url).json()
    result = pd.DataFrame(res['result'], index = [0])
    priceHigh24h = float(result['priceHigh24h'])
    priceLow24h = float(result['priceLow24h'])
    volumeUsd24h = float(result['volumeUsd24h'])
    change24h = float(result['change24h'])
    return priceHigh24h, priceLow24h, volumeUsd24h, change24h

def get_market_price(coin: str):

    if coin == "EGLD" or coin == 'DOT' or coin == 'ADA':
        coin = coin + '-PERP'
    else:
        coin = coin + '/USD'

    url =  f'{URL_BASE}/markets/{coin}'
    res = requests.get(url).json()
    result = pd.DataFrame(res['result'], index = [0])
    price = result['price']
    return price

# Streamlit pages
st.set_page_config(layout = 'wide')
st.sidebar.image(
"https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/z3ahdkytzwi1jxlpazje",
width=50)
# Main Page
def main_page():
    st.image('https://th.bing.com/th/id/R.6bb7aa14d8159440219819b685418522?rik=k44laQRIZUiT8g&pid=ImgRaw&r=0')
    st.title('¡¡Bienvenido!!')
    st.markdown('''
    ## Crypto Dashboard - FTX API 
    ### En este Dashboard veremos informacion en tiempo real, estas son precios historicos, diarios y además podes realizar conversiones de Criptos. Se utilizó [FTX API](https://docs.ftx.com/#overview) para la realización del mismo.
    ### Se pueden observar por el momento las siguientes:
    ###  Bitcoin: BTC &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; &nbsp;  Ethereum: ETH  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;  Solana: SOL 
    ###  Cardano: ADA &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;  Polkadot: DOT  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp;  Matic: MATIC
    ###  ElRond: EGLD &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;  Doge: DOGE  &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; &nbsp; &nbsp; &nbsp;  Ripple: XRP
    ###  Uniswap: UNI
    # ''')
       
# Dashboard
def pageII():
    st.title('Cryptos', anchor = "title")

    # Sidebar

    tickers = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'UNI')
    dropdown = st.sidebar.selectbox('Elige tu Cripto', tickers)
    start_date = st.sidebar.date_input('Comienzo', value = pd.to_datetime('2022-08-01'), key = 'dstart_date')
    end_date = st.sidebar.date_input('Final', value = pd.to_datetime('now'), key = 'dend_date')
    dresolution = st.sidebar.slider('Tamaño', min_value = 86400, max_value = 86400*30, step = 86400, key = 'dresolution')
    

    # Page
    st.subheader(f'{dropdown}/USD', anchor = 'coin')
    coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = dresolution)

    check = st.radio('Filtros', ['1D', '7D', '1M', '3M', '1Y', 'All', 'None'], horizontal = True, index = 6)

    if check == '1D':
        back_days = date.today() - timedelta(days = 1)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [15, 60, 300, 900, 3600, 14400, 86400], key = '1dresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '7D':
        back_days = date.today() - timedelta(days = 7)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = 900)
        resolution = st.select_slider('Resolution', options = [300, 900, 3600, 14400, 86400, 86400*2, 86400*3], key = '7dresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '1M':
        back_days = date.today() - timedelta(days = 30)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [900, 3600, 14400, 86400, 86400*2, 86400*3, 86400*4], key = '1mresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '3M':
        back_days = date.today() - timedelta(days = 90)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [3600, 14400, 86400, 86400*2, 86400*3, 86400*4, 86400*7], key = '3mresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == '1Y':
        back_days = date.today() - timedelta(days = 365)
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)

    if check == 'All':
        back_days = date.today() - timedelta(days = 1095) # 3 years
        start_date = pd.to_datetime(back_days)
        end_date = pd.to_datetime('now')
        resolution = st.select_slider('Resolution', options = [86400, 86400*5, 86400*10, 86400*15, 86400*20, 86400*25, 86400*30], key = '1yresolution')
        coin_df = get_historical(dropdown, start_date = start_date, end_date = end_date, resolution = resolution)
    
    if check == 'None':
        pass

    # Moving average - 30weeks
    coin_df['30wma'] = coin_df['close'].rolling(30).mean()

    variance = round(np.var(coin_df['close']),3)
    priceHigh24h, priceLow24h, volumeUsd24h, change24h = get_market(dropdown)
    price = get_market_price(dropdown)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col4: st.metric('Variance', variance)
    with col2: st.metric('24h High', priceHigh24h)
    with col3: st.metric('24h Low', priceLow24h)
    with col5: st.metric('24h Volume', volumeUsd24h)
    with col1: st.metric('Price', price, round(change24h,5))


    # Candle and volume chart
    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, vertical_spacing = 0.1, row_heights = [100,30])
    fig.add_trace(
        go.Candlestick(x = coin_df['date'],
                       open = coin_df['open'], high = coin_df['high'],
                       low = coin_df['low'], close = coin_df['close'],
                       name = 'Variaciones del Día',
                       ), row = 1, col = 1
    )

    fig.update_layout(xaxis_rangeslider_visible = False)

    fig.add_trace(
        go.Scatter(
            x = coin_df['date'],
            y = coin_df['30wma'],
            line = dict(color = '#e0e0e0', width = 2, dash = 'dot'),
            name = "Ultimo Mes"
        ), row = 1, col = 1
    )

    # Bar chart 
    fig.add_trace(
        go.Bar(
            x = coin_df['date'],
            y = coin_df['volume'],
            marker = dict(color = coin_df['volume'], colorscale = 'aggrnyl_r')
        ), row = 2, col = 1
    )
    fig['layout']['xaxis2']['title'] = 'Fecha'
    fig['layout']['yaxis']['title'] = 'Precio'
    fig['layout']['yaxis2']['title'] = 'Volumen'
    st.plotly_chart(fig, use_container_width = True)

    # Show data
    if st.checkbox('Mostrar Datos'):
        st.dataframe(coin_df)

    # Crypto/USD Calculator
    st.header('Conversor de Criptos')
    #st.subheader('Please select two currencies from the following boxes')
    col1, col2 = st.columns(2)

    tickers2 = ('USD', 'BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC', 'EGLD', 'DOGE', 'XRP', 'UNI')
    with col1: box01 = st.selectbox('Cripto a Elegir',tickers2, key = 'coin1')
    with col2: box02 = st.selectbox('Cripto a Convertir', tickers2, key = 'coin2')
    
    columns = st.columns((2, 1, 2))
    quantity = columns[1].number_input('Cantidad')


    if box01 != 'USD' and box02 != 'USD':
        price1 = get_market_price(box01)
        price2 = get_market_price(box02)
        convert = float(quantity*price1/price2)
    elif box01 == 'USD' and box02 != 'USD':
        price2 = get_market_price(box02)
        convert = float(quantity/price2)
    elif box01 != 'USD' and box02 == 'USD':
        price1 = get_market_price(box01)
        convert = float(quantity*price1)
    else:
        convert = quantity

    columns = st.columns((2, 1, 2))
    #quantity = columns[1].text(f'{quantity} {box01} = {convert} {box02}')
    quantity = columns[1].metric('',convert)

pages = {
    'I. Página Principal': main_page,
    'II. Crypto Dashboard': pageII
}

selected_page = st.sidebar.radio("Navegacion", pages.keys())
pages[selected_page]()