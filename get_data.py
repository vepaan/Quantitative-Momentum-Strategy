import csv
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

months_range=1

def get_stock_data(ticker, months_range):
    end_date = datetime.now()
    start_date = end_date - timedelta((months_range*30+20)) # adjusting for the 14 day rsi and 20 day window for moving average (major error debugged)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    print(end_date_str,start_date_str)

    data = yf.download(ticker, start=start_date_str, end=end_date_str)
    return data

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def process_portfolio(months_range):
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

    # List to hold all data for the portfolio
    portfolio_data = []

    # Ensure the portfolios directory exists
    output_dir = 'data/processed_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'portfolio_data.csv')

    # Define the columns for the output CSV
    output_columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI']

    # Initialize the CSV file with headers
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output_columns)

    # Process each sector and its tickers
    for sector, tickers in sector_tickers.items():
        print(f"Processing sector: {sector}")
        
        for ticker in tickers:
            print(f"Fetching data for {ticker}...")
            try:
                # Fetch stock data for the ticker
                data = get_stock_data(ticker, months_range)
                
                #error start
                if data.empty:
                    print(f"No data fetched for {ticker}. Skipping...")
                    continue
                
                # Calculate RSI for the stock
                rsi = calculate_rsi(data)
                
                # Add RSI to the DataFrame
                data['RSI'] = rsi
                
                # Drop rows where RSI is NaN (first 'period' rows)
                data.dropna(subset=['RSI'], inplace=True)
                
                # Add a Ticker column
                data['Ticker'] = ticker
                
                # Reorder columns to match output_columns
                data = data.reset_index()
                data = data[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI']]

                #error end print(data)

                # Append to the portfolio_data list
                portfolio_data.append(data)
                
                # Store the most recent RSI value
                stock_rsi[ticker] = data['RSI'].iloc[-1]  # Most recent RSI value
                
                print(f"RSI for {ticker}: {stock_rsi[ticker]}")
            except Exception as e:
                print(f"Failed to process {ticker}: {e}")

    # Concatenate all data into a single DataFrame
    if portfolio_data:
        portfolio_df = pd.concat(portfolio_data, ignore_index=True)
        
        # Save the DataFrame to CSV
        portfolio_df.to_csv(output_file, mode='a', index=False, header=False)
        
        print(f"\nAll data and RSI values have been saved to '{output_file}'.")
    else:
        print("No portfolio data to save.")

    # Optionally, print the collected RSIs for each stock
    print("\nRSI values for all stocks:")
    for ticker, rsi_value in stock_rsi.items():
        print(f"{ticker}: {rsi_value}")

# Main execution block
if __name__ == "__main__":
    months = months_range  # Adjust this for the date range (months)
    process_portfolio(months)
