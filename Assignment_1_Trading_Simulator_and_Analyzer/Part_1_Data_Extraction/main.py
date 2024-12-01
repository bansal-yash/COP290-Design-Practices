from datetime import date
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import stock_df
import sys
import generate_files
import plotting
import compressor

sym = sys.argv[1]
year = int(sys.argv[2])

current_date = date.today()
start_date = current_date - relativedelta(years = year)

stock_symbols = ["ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", 
                 "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", 
                 "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", 
                 "LTIM", "LT", "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SBIN", "SUNPHARMA", "TCS", 
                 "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"]

df = stock_df(symbol = sym, from_date = start_date, to_date = current_date, series = "EQ" )
df = df[[ "DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]]

time_dict, size_dict = generate_files.generate(sym,df)  # time in milliseconds

time_dict = dict(sorted(time_dict.items(), key=lambda item: item[1]))
size_dict = dict(sorted(size_dict.items(), key=lambda item: item[1]))

plotting.plot_graph_2(time_dict, size_dict, sym)

compression_time_dict, decompression_time_dict, compressed_size_dict = compressor.compress(sym)
compression_time_dict = dict(sorted(compression_time_dict.items(), key=lambda item: item[1]))
decompression_time_dict = dict(sorted(decompression_time_dict.items(), key=lambda item: item[1]))
compressed_size_dict = dict(sorted(compressed_size_dict.items(), key=lambda item: item[1]))

plotting.plot_graph_3(compression_time_dict, decompression_time_dict, compressed_size_dict, sym)