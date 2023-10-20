import pandas as pd
from stockx import main as get_stockx_data
from nike import main as get_nike_data
from eobuwie import get_shoe_data as get_eobuwie_data

# Get data from StockX
stockx_data = get_stockx_data()

# Get data from Nike and eObuwie
nike_data = get_nike_data()
eobuwie_data = get_eobuwie_data()

# Concatenate the data from Nike and eObuwie
merged_data = pd.concat([nike_data, eobuwie_data], ignore_index=True)

# Create a DataFrame with the lowest price and 'shoeLink' for each shoe based on 'shoeId'
lowest_price_data = merged_data.groupby('shoeId').agg({'price': 'min', 'shoeLink': 'first'}).reset_index()

# Ensure lowest_price_data is a DataFrame, not a dictionary
lowest_price_data = pd.DataFrame(lowest_price_data)
print(lowest_price_data)

# Merge the lowest price data with StockX data based on 'shoeId'
final_data = pd.merge(stockx_data, lowest_price_data, on='shoeId', how='inner')

# Rename the 'price' column to indicate it's the lowest price
final_data.rename(columns={'price': 'lowestPrice'}, inplace=True)

# Specify the file path where you want to save the Excel file
excel_file_path = "final_shoe_data.xlsx"

# Write the final_data DataFrame to an Excel file
final_data.to_excel(excel_file_path, index=False)

# Print or process the final_data DataFrame
print(final_data)
