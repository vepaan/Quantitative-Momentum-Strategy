import csv
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

months_range=12

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
    file_path = 'data/raw_data/hedge_funds.csv'
    sector_tickers = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        for header in headers:
            sector_tickers[header] = []
        for row in csv_reader:
            for idx, ticker in enumerate(row):
                if ticker:
                    sector_tickers[headers[idx]].append(ticker)

    stock_rsi = {}
    portfolio_data = []

    output_dir = 'data/processed_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'portfolio_data.csv')
    output_columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI']

    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(output_columns)

    for sector, tickers in sector_tickers.items():
        print(f"Processing sector: {sector}")
        
        for ticker in tickers:
            print(f"Fetching data for {ticker}...")
            try:
                data = get_stock_data(ticker, months_range)
                if data.empty:
                    print(f"No data fetched for {ticker}. Skipping...")
                    continue
            
                rsi = calculate_rsi(data)
                data['RSI'] = rsi
                data.dropna(subset=['RSI'], inplace=True) #this will remove rows where rsi is empty so sometimes you might have less data in portfolio than extracted
                data['Ticker'] = ticker
                data = data.reset_index()
                data = data[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI']]
                portfolio_data.append(data)
                
                stock_rsi[ticker] = data['RSI'].iloc[-1]  # Most recent RSI value
                
                print(f"RSI for {ticker}: {stock_rsi[ticker]}") #just prinintg the rsi value
            except Exception as e:
                print(f"Failed to process {ticker}: {e}")

    if portfolio_data:
        portfolio_df = pd.concat(portfolio_data, ignore_index=True)
        portfolio_df.to_csv(output_file, mode='a', index=False, header=False)
        print(f"\nAll data and RSI values have been saved to '{output_file}'.")
    else:
        print("No data to save.")

    print("\nRSI values for all stocks:")
    for ticker, rsi_value in stock_rsi.items():
        print(f"{ticker}: {rsi_value}")

if __name__ == "__main__":
    months = months_range  #doing this so i can use months in rsi.py
    process_portfolio(months)
