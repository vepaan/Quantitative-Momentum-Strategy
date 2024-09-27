import pandas as pd
import os

input_file = 'data/processed_data/portfolio_data.csv'
output_file = 'portfolios/MACD.csv'

stock_data = pd.read_csv(input_file)

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    data['EMA_short'] = calculate_ema(data['Close'], short_window)
    data['EMA_long'] = calculate_ema(data['Close'], long_window)
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal'] = calculate_ema(data['MACD'], signal_window)
    return data

def calculate_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

signals = []
for ticker in stock_data['Ticker'].unique():
    ticker_data = stock_data[stock_data['Ticker'] == ticker]
    count_ticker_data = len(ticker_data)

    if count_ticker_data >= 1:
        ticker_data = calculate_macd(ticker_data)

        latest_macd = ticker_data['MACD'].iloc[-1]
        latest_signal = ticker_data['Signal'].iloc[-1]
        latest_close = ticker_data['Close'].iloc[-1]

        if latest_macd > latest_signal:
            signal = 'Buy'
        elif latest_macd < latest_signal:
            signal = 'Sell'
        else:  # Hold signal
            signal = 'Hold'

        signals.append({
            'Ticker': ticker,
            'Date': ticker_data['Date'].iloc[-1],
            'Latest Close': latest_close,
            'MACD': latest_macd,
            'Signal': latest_signal,
            'MACD Signal': signal
        })

signals_df = pd.DataFrame(signals)

# Always write headers by overwriting the file
signals_df.to_csv(output_file, index=False)  # This will write the header every time

print(f"Data successfully written to {output_file}.")
