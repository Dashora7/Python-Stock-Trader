from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import VotingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

df_weekly = pd.read_csv('data//tech_df')

df_weekly.replace([np.inf, -np.inf], np.nan)

df_weekly.dropna(inplace=True)
df_weekly.drop(columns='Unnamed: 0', inplace=True)

print(df_weekly.columns)

features = df_weekly[['open', 'high', 'low', 'close', 'adx', 'aroon', 'macd', 'rsi', 'stoch', 'obv', 'ma_50', 'current_close_pct_change']].values
labels = df_weekly['future_close_pct_change'].values
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
reg1 = GradientBoostingRegressor(random_state=1, n_estimators=10)
reg2 = RandomForestRegressor(random_state=1, n_estimators=10)
reg3 = LinearRegression()
ereg = VotingRegressor(estimators=[('gb', reg1), ('rf', reg2), ('lr', reg3)])
ereg = ereg.fit(X_train, y_train)
print(ereg.score(X_test, y_test))