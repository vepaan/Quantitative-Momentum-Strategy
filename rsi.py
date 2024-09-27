import pandas as pd
from get_data import months_range

# Convert months_range to days
months_range = int(months_range * 30)

# Load the stock data (assumed to include the 'Close' price)
stock_data = pd.read_csv('data/processed_data/portfolio_data.csv')

# Function to calculate Bollinger Bands using closing prices
def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    """Calculates the Bollinger Bands based on closing prices."""
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()

    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)

    return upper_band, lower_band

# Create a list to store the signals
signals = []

# Loop through each ticker
for ticker in stock_data['Ticker'].unique():
    ticker_data = stock_data[stock_data['Ticker'] == ticker]

    # Ensure there are enough data points
    if len(ticker_data) >= 20:  # Use 20 for the moving average window
        # Calculate Bollinger Bands using the closing prices
        upper_band, lower_band = calculate_bollinger_bands(ticker_data)

        # Get the most recent RSI and closing price
        latest_rsi = ticker_data['RSI'].iloc[-1]
        latest_close = ticker_data['Close'].iloc[-1]

        # Determine buy/sell/hold signal based on RSI and Bollinger Bands
        if latest_rsi < 35 and latest_close < lower_band.iloc[-1]:  # Buy signal
            risk_averse_signal = 'Buy'
        elif latest_rsi > 65 and latest_close > upper_band.iloc[-1]:  # Sell signal
            risk_averse_signal = 'Sell'
        else:  # Hold signal
            risk_averse_signal = 'Hold'

        if latest_rsi < 35 or latest_close < lower_band.iloc[-1]:  # Buy signal
            aggresive_signal = 'Long'
        elif latest_rsi > 65 or latest_close > upper_band.iloc[-1]:  # Sell signal
            aggresive_signal = 'Short'
        else:  # Hold signal
            aggresive_signal = 'Hold'

        signals.append({
            'Ticker': ticker,
            'Date': ticker_data['Date'].iloc[-1],  # Most recent date
            'RSI': latest_rsi,
            'Upper Band': upper_band.iloc[-1],
            'Lower Band': lower_band.iloc[-1],
            'Latest Close': latest_close,
            'SafeSignal': risk_averse_signal,
            'AggresiveSignal': aggresive_signal
        })

# Convert the signals to a DataFrame
signals_df = pd.DataFrame(signals)

# Save to portfolio.csv
signals_df.to_csv('portfolios/portfolio.csv', index=False)
