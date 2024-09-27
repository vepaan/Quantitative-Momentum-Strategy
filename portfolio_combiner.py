import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill

rsi_bollinger_file = 'portfolios/RSI_Bollinger.csv'
macd_file = 'portfolios/MACD.csv'
output_file = 'portfolios/portfolio.xlsx'

rsi_bollinger_df = pd.read_csv(rsi_bollinger_file)
macd_df = pd.read_csv(macd_file)

if 'Ticker' in rsi_bollinger_df.columns and 'Ticker' in macd_df.columns:
    rsi_bollinger_selected = rsi_bollinger_df[['Ticker', 'Date', 'Latest Close', 'Upper Band', 'Lower Band', 'RSI', 'RSI signal', 'MA signal']]
    macd_selected = macd_df[['Ticker', 'Date', 'MACD', 'Signal','MACD Signal']]

    combined_df = pd.merge(rsi_bollinger_selected, macd_selected, on=['Ticker', 'Date'], how='outer', suffixes=('x', 'y'))

    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]
else:
    print("One of the DataFrames does not contain the 'Ticker' column. Skipping merge.")
    combined_df = pd.concat([rsi_bollinger_df[['Ticker', 'Date']], macd_df[['Ticker', 'Date']]], axis=0, ignore_index=True)

combined_df.to_csv(output_file.replace('.xlsx', '.csv'), index=False)

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    combined_df.to_excel(writer, index=False, sheet_name='Portfolio')

    workbook = writer.book
    worksheet = writer.sheets['Portfolio']

    buy_fill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')  # Green
    sell_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')  # Red
    hold_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # Yellow

    for row in range(2, len(combined_df) + 2):  # row 2 in excel, ie cell 1
        for col in ['RSI signal', 'MA signal', 'MACD Signal']:
            if col in combined_df.columns:
                cell_value = combined_df[col].iloc[row - 2] 
                cell = worksheet.cell(row=row, column=combined_df.columns.get_loc(col) + 1) 
                cell.value = cell_value  
                if cell_value == 'Buy':
                    cell.fill = buy_fill
                elif cell_value == 'Sell':
                    cell.fill = sell_fill
                elif cell_value == 'Hold':
                    cell.fill = hold_fill

print(f"\nData successfully written to {output_file}.")
