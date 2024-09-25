from datetime import datetime, timedelta
import yfinance as yf

def get_stock_data(ticker, months_range):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months_range * 30)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start_date_str, end=end_date_str)
    return data

ticker = 'AAPL'
months_range = 2  # input your months range here
data = get_stock_data(ticker, months_range)
print(data)
