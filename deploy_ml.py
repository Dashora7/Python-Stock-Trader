import technical_acquisition_methods as tam



features = df_weekly[['open', 'high', 'low', 'close', 'adx', 'aroon', 'macd', 'rsi', 'stoch', 'obv', 'ma_50', 'current_close_pct_change']].values
labels = df_weekly['future_close_pct_change'].values
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
reg1 = GradientBoostingRegressor(random_state=1, n_estimators=10)
reg2 = RandomForestRegressor(random_state=1, n_estimators=10)
reg3 = LinearRegression()
ereg = VotingRegressor(estimators=[('gb', reg1), ('rf', reg2), ('lr', reg3)])
ereg = ereg.fit(X_train, y_train)
print(ereg.score(X_test, y_test))