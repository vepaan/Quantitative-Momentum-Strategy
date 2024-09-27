import pandas as pd
from get_data import months_range

days = int(months_range * 30)
stock_data = pd.read_csv('data/processed_data/portfolio_data.csv')

def calculate_bollinger_bands(data, windoww, num_std_dev=2):
    rolling_mean = data['Close'].rolling(window=windoww).mean()
    rolling_std = data['Close'].rolling(window=windoww).std()

    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)

    return upper_band, lower_band

signals = []

for ticker in stock_data['Ticker'].unique():
    ticker_data = stock_data[stock_data['Ticker'] == ticker]
    count_ticker_data = len(ticker_data) #ideally len(ticker_data) should be above 20 for a more accurate momentum

    if count_ticker_data>=1:  # set the 0 to any number that you want the moving average window to be, im using 0 for a higher flexibility.
        upper_band, lower_band = calculate_bollinger_bands(ticker_data, (count_ticker_data-1))
        latest_rsi = ticker_data['RSI'].iloc[-1]
        latest_close = ticker_data['Close'].iloc[-1]

        if latest_rsi < 30:  # Buy signal
            rsi_signal = 'Buy'
        elif latest_rsi > 70:  # Sell signal
            rsi_signal = 'Sell'
        else:  # Hold signal
            rsi_signal = 'Hold'

        if latest_close < lower_band.iloc[-1]:  # Buy signal
            MA_signal = 'Buy'
        elif latest_close > upper_band.iloc[-1]:  # Sell signal
            MA_signal = 'Sell'
        else:  # Hold signal
            MA_signal = 'Hold'

        signals.append({
            'Ticker': ticker,
            'Date': ticker_data['Date'].iloc[-1],  # Most recent date
            'RSI': latest_rsi,
            'Upper Band': upper_band.iloc[-1],
            'Lower Band': lower_band.iloc[-1],
            'Latest Close': latest_close,
            'RSI signal': rsi_signal,
            'MA signal': MA_signal
        })

signals_df = pd.DataFrame(signals)
signals_df.to_csv('portfolios/RSI_Bollinger.csv', index=False)
