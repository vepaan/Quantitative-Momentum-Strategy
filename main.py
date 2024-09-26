import csv
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Function to get stock data from yfinance
def get_stock_data(ticker, months_range):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months_range * 30)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Download stock data using yfinance
    data = yf.download(ticker, start=start_date_str, end=end_date_str)
    return data

# Function to calculate RSI
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Read CSV file and store tickers by sector
file_path = 'data/raw_data/hedge_funds.csv'
sector_tickers = {}

# Read the CSV file
with open(file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Read the header (sector names)
    headers = next(csv_reader)
    
    # Initialize lists for each sector in the dictionary
    for header in headers:
        sector_tickers[header] = []
    
    # Read the stock tickers and store them in the respective sector list
    for row in csv_reader:
        for idx, ticker in enumerate(row):
            if ticker:  # Ensure that empty values are ignored
                sector_tickers[headers[idx]].append(ticker)

# Dictionary to store RSI values for each ticker
stock_rsi = {}

# Process each sector and its tickers
months_range = 2  # Adjust this for the date range (months)
for sector, tickers in sector_tickers.items():
    print(f"Processing sector: {sector}")
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        try:
            # Fetch stock data for the ticker
            data = get_stock_data(ticker, months_range)
            
            # Calculate RSI for the stock
            rsi = calculate_rsi(data)
            
            # Store the most recent RSI value
            stock_rsi[ticker] = rsi.iloc[-1]  # Most recent RSI value
            
            print(f"RSI for {ticker}: {stock_rsi[ticker]}")
        except Exception as e:
            print(f"Failed to process {ticker}: {e}")

# Print the collected RSIs for each stock
print("\nRSI values for all stocks:")
for ticker, rsi_value in stock_rsi.items():
    print(f"{ticker}: {rsi_value}")

# You can store the RSI values in a CSV or use them further in your code.
