# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:26:32 2020

@author: nrdas
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

def get_sentdex_main_data(ticker):
    response = requests.get('http://sentdex.com/financial-analysis/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        soup.prettify()
    tags = soup.find_all('span')[3:]
    hislist = ['increasing' if tag['class'][1] == 'glyphicon-chevron-up' else 'decreasing' for tag in tags]
    response = requests.get('http://sentdex.com/financial-analysis/')
    df = pd.read_html(response.text)[0]
    hdf = pd.DataFrame(hislist)
    hdf.columns = ['history']
    df = pd.concat([df, hdf], axis=1)
    ser = df.loc[df['Symbol'] == ticker]
    return {'volume': ser['all Volume of Mentions'].tolist()[0], 'sentiment': ser['all Overall Sentiment'].tolist()[0],
            'history': ser['history'].tolist()[0]}

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.strip()
        if '.' in ticker:
            a, b = ticker.split('.')
            ticker = a+'-'+b
        tickers.append(ticker)

    with open("data//sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers

save_sp500_tickers()