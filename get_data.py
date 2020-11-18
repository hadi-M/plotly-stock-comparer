import yfinance as yf
from os.path import join as path_join
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
TICKER_CSV_FILE = "./s_and_p_500_tickers/constituents_csv.csv"
TICKER_LIST = pd.read_csv(TICKER_CSV_FILE)["Symbol"].to_list()                                                                

# 1. Downloading all of the market data
final_df = yf.download(TICKER_LIST, auto_adjust=False)

# 2. Saving market data with this format yyy-mm-dd_market_data.pckl
now_yyyymmdd = datetime.now().strftime(r"%Y-%m-%d")
final_df.to_pickle(
    path_join(
        DATA_DIR,
        f"{now_yyyymmdd}_market_data.pckl"
    )
)
