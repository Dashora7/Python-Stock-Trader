import pandas as pd
import numpy as np
import quandl
import FundamentalAnalysis as fa
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import ta
'''
quandl.ApiConfig.api_key = 'exUkGQLmC9_T8J1TU3Xz'
fm = '07a2e7ec7eaf928f2a35b6e904281ba5'
'''

'''

#CONSUMER SENTIMENT INDEX
df_monthly_sentiment = quandl.get('UMICH/SOC1')
#df_monthly_sentiment.tail()

#NATIONAL GDP DATA
df_gdp = quandl.get('FRED/GDP')
df_gdp.tail()

'''

def get_price_data(ticker):
    start = dt.datetime(2010, 4, 5)
    end = dt.datetime.now()
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    return df

def get_weekly_returns(price_data):
    df_ohlc = price_data['Adj Close'].resample('7D').ohlc()
    df_ohlc = df_ohlc.reset_index()
    df_ohlc['future_close_pct_change'] = df_ohlc['close'].pct_change()
    df_ohlc['current_close_pct_change'] = df_ohlc['close'].pct_change()
    df_ohlc['future_close_pct_change'] = df_ohlc['future_close_pct_change'].shift(periods=-1)
    num_rows = df_ohlc.shape[0]
    df_ohlc = df_ohlc.drop(num_rows-1)
    df_ohlc = df_ohlc.drop(0)
    return df_ohlc
    
def get_50_day_ma(price_data):
    series = price_data['Adj Close'].rolling(window=50,min_periods=0).mean()
    return series

'''
# Show the available companies
companies = fa.available_companies()

# Collect general company information
profile = fa.profile(ticker)

# Collect recent company quotes
quotes = fa.quote(ticker)

# Collect market cap and enterprise value
enterprise_value = fa.enterprise(ticker)

# Show recommendations of Analysts
ratings = fa.rating(ticker)

# Obtain DCFs over time
dcf_quarterly = fa.discounted_cash_flow(ticker, period="quarter")

# Collect the Balance Sheet statements
balance_sheet_quarterly = fa.balance_sheet_statement(ticker, period="quarter")

# Collect the Income Statements
income_statement_quarterly = fa.income_statement(ticker, period="quarter")

# Collect the Cash Flow Statements
cash_flow_statement_quarterly = fa.cash_flow_statement(ticker, period="quarter")

# Show Key Metrics
key_metrics_quarterly = fa.key_metrics(ticker, period="quarter")

# Show a large set of in-depth ratios
financial_ratios = fa.financial_ratios(ticker)

# Show the growth of the company
growth_quarterly = fa.financial_statement_growth(ticker, period="quarter")

'''

def get_tech_factors(ticker):
    df_tick = get_price_data(ticker)
    weekly_ma50 = get_50_day_ma(df_tick).resample('7D').mean().to_frame()
    df_weekly = get_weekly_returns(df_tick)
    adx = ta.trend.ADXIndicator(high = df_tick['High'], low = df_tick['Low'], close = df_tick['Close']).adx()
    aroon = ta.trend.AroonIndicator(close = df_tick['Close']).aroon_indicator()
    macd = ta.trend.MACD(close = df_tick['Close']).macd()

    # THESE ARE MOMENTUM INDICATORS

    rsi = ta.momentum.RSIIndicator(close = df_tick['Close']).rsi()
    stoch = ta.momentum.StochasticOscillator(high = df_tick['High'], low = df_tick['Low'],
                                             close = df_tick['Close']).stoch()

    # THESE ARE VOLUME INDICATORS

    adl = ta.volume.AccDistIndexIndicator(high = df_tick['High'], low = df_tick['Low'],
                                            close = df_tick['Close'], volume=df_tick['Volume']).acc_dist_index()
    obv = ta.volume.OnBalanceVolumeIndicator(close = df_tick['Close'], volume = df_tick['Volume']).on_balance_volume()

    # THESE ARE VOLATILITY INDICATORS

    mbol = ta.volatility.BollingerBands(close = df_tick['Close']).bollinger_mavg()

    adx_weekly = adx.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    aroon_weekly = aroon.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    macd_weekly = macd.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    rsi_weekly = rsi.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    stoch_weekly = stoch.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    obv_weekly = obv.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    adl_weekly = adl.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()
    mbol_weekly = mbol.rolling(window=5,min_periods=0).mean().resample('7D').mean().to_frame()

    df_weekly['adx'] = adx_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['aroon'] = aroon_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['macd'] = macd_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['rsi'] = rsi_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['stoch'] = stoch_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['obv'] = obv_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['adl'] = adl_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['mbol'] = mbol_weekly[1:-1].set_index(df_weekly.index)
    df_weekly['ma_50'] = weekly_ma50[1:-1].set_index(df_weekly.index)

    df_weekly = df_weekly.drop(columns=['Date'])[5:]

    return df_weekly


'''

#WE NEED TO GENERATE TEHSE DATAFRAMES FOR ALL STOCKS, APPEND THEM ALL, THEN RUN THIS CODE

features = df_weekly[['open', 'high', 'low', 'close', 'adx', 'aroon', 'macd', 'rsi', 'stoch', 'obv', 'ma_50', 'current_close_pct_change']].values
labels = df_weekly['future_close_pct_change'].values
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
reg1 = GradientBoostingRegressor(random_state=1, n_estimators=10)
reg2 = RandomForestRegressor(random_state=1, n_estimators=10)
reg3 = LinearRegression()
ereg = VotingRegressor(estimators=[('gb', reg1), ('rf', reg2), ('lr', reg3)])
ereg = ereg.fit(X_train, y_train)
print(ereg.score(X_test, y_test))


'''