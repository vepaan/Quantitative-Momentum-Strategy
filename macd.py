import pandas as pd

# File paths
input_file = 'data/processed_data/portfolio_data.csv'
output_file = 'portfolios/macd.csv'

# Load the stock data
stock_data = pd.read_csv(input_file)

# Function to calculate the Exponential Moving Averages (EMA)
def calculate_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

# Function to calculate MACD line, Signal line, and Histogram
def calculate_macd(data):
    ema_12 = calculate_ema(data['Close'], 12)
    ema_26 = calculate_ema(data['Close'], 26)

    macd_line = ema_12 - ema_26
    signal_line = calculate_ema(macd_line, 9)
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram

# Create a list to store the MACD data
macd_signals = []

# Loop through each ticker
for ticker in stock_data['Ticker'].unique():
    ticker_data = stock_data[stock_data['Ticker'] == ticker]
    # Ensure there are enough data points for EMA calculation
    if len(ticker_data) >= 26:
        # Calculate MACD, Signal line, and Histogram
        macd_line, signal_line, histogram = calculate_macd(ticker_data)

        # Get the most recent data
        latest_date = ticker_data['Date'].iloc[-1]
        latest_close = ticker_data['Close'].iloc[-1]
        latest_macd = macd_line.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        latest_histogram = histogram.iloc[-1]

        # Determine the MACD signal (Buy/Sell/Hold)
        if latest_macd > latest_signal:
            macd_signal = 'Buy'
        elif latest_macd < latest_signal:
            macd_signal = 'Sell'
        else:
            macd_signal = 'Hold'

        macd_signals.append({
            'Ticker': ticker,
            'Date': latest_date,
            'Close': latest_close,
            'MACD Line': latest_macd,
            'Signal Line': latest_signal,
            'Histogram': latest_histogram,
            'MACD Signal': macd_signal
        })

# Convert the MACD signals to a DataFrame
macd_df = pd.DataFrame(macd_signals)

# Save to macd.csv (append mode)
macd_df.to_csv(output_file, mode='a', header=not pd.read_csv(output_file, nrows=1).shape[0], index=False)

print("MACD data appended successfully!")
