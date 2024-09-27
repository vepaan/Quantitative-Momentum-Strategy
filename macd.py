import pandas as pd

input_file = 'data/processed_data/portfolio_data.csv'
output_file = 'portfolios/macd.csv'

stock_data = pd.read_csv(input_file)

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

# Function to calculate MACD, Signal Line, and Histogram
def calculate_macd(data):
    ema_12 = calculate_ema(data['Close'], 12)
    ema_26 = calculate_ema(data['Close'], 26)
    macd_line = ema_12 - ema_26
    signal_line = calculate_ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# Create a list to store MACD data
macd_data = []

# Loop through each ticker
for ticker in stock_data['Ticker'].unique():
    ticker_data = stock_data[stock_data['Ticker'] == ticker]

    # Ensure there are enough data points for both EMA 12 and EMA 26
    if len(ticker_data) < 26:
        print(f"Not enough data for {ticker}. Skipping...")
        continue

    # Calculate MACD, Signal Line, and Histogram
    macd_line, signal_line, histogram = calculate_macd(ticker_data)

    # Get the most recent MACD data and append it to the list
    for i in range(len(ticker_data)):
        macd_data.append({
            'Ticker': ticker,
            'Date': ticker_data['Date'].iloc[-1],
            'Close': ticker_data['Close'].iloc[-1],
            'MACD Line': macd_line.iloc[-1],
            'Signal Line': signal_line.iloc[-1],
            'Histogram': histogram.iloc[-1],
            'MACD Signal': 'Buy' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'Sell'
        })

# Convert to DataFrame
macd_df = pd.DataFrame(macd_data)

# Append to macd.csv or create it if it doesn't exist
macd_df.to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))
