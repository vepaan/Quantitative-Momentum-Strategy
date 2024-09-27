import pandas as pd
from get_data import months_range

months_range=int(months_range*30)

# Load the RSI data
rsi_data = pd.read_csv('data/processed_data/portfolio_data.csv')

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(data, window=months_range, num_std_dev=2):
    """Calculates the Bollinger Bands."""
    rolling_mean = data['RSI'][:window].mean()
    rolling_std = data['RSI'][:window].std()

    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)

    return upper_band, lower_band

# Create a list to store the signals
signals = []

# Loop through each ticker
for ticker in rsi_data['Ticker'].unique():
    ticker_data = rsi_data[rsi_data['Ticker'] == ticker]
    
    # Ensure there are enough data points
    if len(ticker_data) >= 14:
        # Calculate Bollinger Bands using all data points except the last one
        upper_band, lower_band = calculate_bollinger_bands(ticker_data[:13])
        
        # Get the most recent RSI
        latest_rsi = ticker_data['RSI'].iloc[-1]

        # Determine buy/sell/hold signal based on RSI and Bollinger Bands
        if latest_rsi < lower_band:
            signal = 'Buy'
        elif latest_rsi > upper_band:
            signal = 'Sell'
        else:
            signal = 'Hold'

        signals.append({
            'Ticker': ticker,
            'Date': ticker_data['Date'].iloc[-1],  # You may want to adjust this based on your actual data
            'RSI': latest_rsi,
            'Upper Band': upper_band,
            'Lower Band': lower_band,
            'Signal': signal
        })

# Convert the signals to a DataFrame
signals_df = pd.DataFrame(signals)

# Save to portfolio.csv
signals_df.to_csv('portfolios/portfolio.csv', index=False)
