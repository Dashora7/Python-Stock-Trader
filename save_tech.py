import pickle
import technical_acquisition_methods as tam
import pandas as pd

df_list = []
with open('data//sp500tickers.pickle', 'rb') as f:
    tickers = pickle.load(f)

for ticker in tickers:
    df_list.append(tam.get_tech_factors(ticker))
    print('added' + ticker)

df_weekly = pd.concat(df_list)
df_weekly.to_csv('data//tech_df')