import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, features="lxml")
    # table that contains s&p 500 companies
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []

    print(table)

    # ignore the first row because it's the header row of the table
    for row in table.findAll('tr')[1:]:
        # ticker of the company for that row, 
        # which is what we're interested in
        ticker = row.findAll('td')[0].text.replace('\n','')
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers

# save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2003, 1, 1)
    end = dt.datetime(2019, 12, 31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists(f'stock_dfs/{ticker}.csv'):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv(f'stock_dfs/{ticker}.csv')
        else:
            print(f'Already Have {ticker}')

get_data_from_yahoo()