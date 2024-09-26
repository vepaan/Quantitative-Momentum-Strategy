import csv

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

# Print the sector-wise ticker lists
for sector, tickers in sector_tickers.items():
    print(f"{sector}: {tickers}")
