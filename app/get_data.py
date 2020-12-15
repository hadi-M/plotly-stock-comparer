from ipdb.__main__ import main
import yfinance as yf
from os.path import join as path_join
import pandas as pd
from datetime import datetime
from glob import glob


DATA_DIR = "data"


# 1. Check if the data file exists, if so, exit
if glob(path_join(DATA_DIR, "*.pckl")):
    # Data file/files exist
    exit()


TICKER_CSV_FILE = "./s_and_p_500_tickers/constituents_csv.csv"
TICKER_LIST = pd.read_csv(TICKER_CSV_FILE)["Symbol"].to_list()

# 2. Downloading all of the market data
final_df = yf.download(TICKER_LIST, auto_adjust=False)

# 3. Saving market data with this format yyy-mm-dd_market_data.pckl
now_yyyymmdd = datetime.now().strftime(r"%Y-%m-%d")

# 4. Forward fill the data
df = df.fillna(method="ffill")

final_df.to_pickle(
    path_join(
        DATA_DIR,
        f"{now_yyyymmdd}_market_data_forward_filled.pckl"
    )
)

# TODO: Make it so it updates the data everyday