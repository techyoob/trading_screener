



from lstm_handler import Handler





import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()




# TODO:
#  
#       + Re-train lstm model for a given TICKER name 
#       + Process prediction for different set of ranges ( e.g. 1 day, 2 days, ..., and 7 days )


# TODO: 
# - read tickers_list to be processed




apiKey = os.getenv("FMG_KEY")
url = os.getenv("FMG_URL")

# tickers=["AAPL", "UPST", "UBER", "SHOP"]
tickers=["AAPL"]
lstm = Handler()

for ticker in tickers:
    tickerHistoryResponse = requests.get(url+"historical-price-full/"+ticker+"?apikey="+apiKey)    
    lstm.train(tickerHistoryResponse.json())
