#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 00:32:00 2023

@author: SebasRod
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests

url = "https://financialmodelingprep.com/api/v3/symbol/NASDAQ"
headers = {
    'apikey': '857bc36badd88e4c08842ca111368b69',
}

response = requests.get(url, params=headers) 
    
data = response.json()
data = pd.DataFrame(data)

symbol_nasdaq = data['symbol']
all_symbols = symbol_nasdaq.copy()

st.set_page_config(layout="wide")

st.title('Panel de Acciones de Bolsa de Latinos en Wall Street ')
st.write('Datos proporcionados por Financial Modeling Prep Dashboard')

with st.sidebar:
    # Text input for user search query in the first column
    user_input = st.text_input("Search for a Company Symbol:", "")

    # Filter the symbol list based on user input
    filtered_symbols = symbol_nasdaq[symbol_nasdaq.str.contains(user_input, case=False)].tolist()

    # Get the symbols that are not in the filtered list
    remaining_symbols = [symbol for symbol in symbol_nasdaq.tolist() if symbol not in filtered_symbols]

    # Concatenate the filtered symbols with the remaining symbols
    all_symbols = ['Select the company'] + filtered_symbols + remaining_symbols

    # Find the index of user_input in all_symbols. If not found, default to 0 ('Select the company')
    index_to_select = all_symbols.index(user_input) if user_input in all_symbols else 0

    # Display selectbox with all symbols in the second column
    selected_symbol = st.selectbox(label='Company Selection', options=all_symbols, index=index_to_select)

    if selected_symbol == 'Select the company':
        st.write('No data yet')
    else:
        req = f"https://financialmodelingprep.com/api/v3/quote/{selected_symbol}"

        response = requests.get(req, params=headers)

        stock_quote = response.json()
        stock_name = stock_quote[0]['name']
        stock_price = stock_quote[0]['price']
        stock_chg = stock_quote[0]['changesPercentage']
        stock_vol = stock_quote[0]['volume']

        st.write(f'Stock information for {selected_symbol} : {stock_name} ')
    
        st.metric("Price", f"$ {stock_price}", f"{stock_chg} %")
        st.metric("Volume", f"$ {stock_vol}")


if selected_symbol == 'Select the company':
    st.write('No data yet')
else:

    req = f"https://financialmodelingprep.com/api/v3/profile/{selected_symbol}"

    response = requests.get(req, params=headers)
    comp_info = response.json()


    comp_desc = comp_info[0]['description']
    comp_web = comp_info[0]['website']
    comp_name = comp_info[0]['companyName']

    req = f"https://financialmodelingprep.com/api/v3/income-statement/{selected_symbol}?period=annual"
    response = requests.get(req, params=headers)
    income_info = response.json()
    income_info = pd.DataFrame(income_info)

    req = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{selected_symbol}?period=annual"
    response = requests.get(req, params=headers)
    bss_info = response.json()
    bss_info = pd.DataFrame(bss_info)


    st.header(f'Company information for {selected_symbol} : {comp_name} ', divider = 'gray')

    st.text_area("Company Description",f"{comp_desc}")
    st.write(f"Visit [Company Website]({comp_web}) for more information.")

    col1_cha, col2_cha = st.columns(2)

    with col1_cha:
        st.subheader('Revenue Chart')
        st.line_chart(income_info, x="fillingDate", y="revenue")

    with col2_cha:
        st.subheader('Balance Sheet Chart')
        st.line_chart(bss_info, x="fillingDate", y=["totalAssets", "totalEquity", "totalDebt"])    
