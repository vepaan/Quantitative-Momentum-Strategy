import pandas as pd

input_file = 'data/processed_data/portfolio_data.csv'
output_file = 'portfolios/macd.csv'

# Load stock data
stock_data = pd.read_csv(input_file)

# Check if output file exists, if not, write headers
try:
    macd_df = pd.read_csv(output_file)
except FileNotFoundError:
    macd_df = pd.DataFrame(columns=['Ticker', 'Date', 'Close', 'MACD_Line', 'Signal_Line', 'Histogram', 'MACD_Signal'])

# Function to calculate EMA
def calculate_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

signals = []

# Loop through each ticker
for ticker in stock_data['Ticker'].unique():
    ticker_data = stock_data[stock_data['Ticker'] == ticker]
    
    # If not enough data, skip the ticker
    if len(ticker_data) < 26:
        print(f"Not enough data for {ticker}")
        continue
    
    ticker_data = ticker_data.sort_values('Date')  # Sort data by date
    
    # Calculate 12-day and 26-day EMAs
    ema_12 = calculate_ema(ticker_data['Close'], 12)
    ema_26 = calculate_ema(ticker_data['Close'], 26)
    
    # Calculate MACD line and signal line
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    
    # Take the latest data
    latest_row = ticker_data.iloc[-1]
    
    # Determine MACD signal (Buy, Sell, Hold)
    if histogram.iloc[-1] > 0 and macd_line.iloc[-1] > signal_line.iloc[-1]:
        macd_signal = 'Buy'
    elif histogram.iloc[-1] < 0 and macd_line.iloc[-1] < signal_line.iloc[-1]:
        macd_signal = 'Sell'
    else:
        macd_signal = 'Hold'
    
    signals.append({
        'Ticker': ticker,
        'Date': latest_row['Date'],
        'Close': latest_row['Close'],
        'MACD_Line': macd_line.iloc[-1],
        'Signal_Line': signal_line.iloc[-1],
        'Histogram': histogram.iloc[-1],
        'MACD_Signal': macd_signal
    })

# Create a DataFrame for signals
signals_df = pd.DataFrame(signals)

# Append to the existing file
if macd_df.empty:
    signals_df.to_csv(output_file, index=False)
else:
    signals_df.to_csv(output_file, mode='a', header=False, index=False)
