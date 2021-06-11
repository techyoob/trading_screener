



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


apiKey = os.getenv("FMG_KEY")
url = os.getenv("FMG_URL")

# historical-price-full

# TODO: 
# - read tickers_list to be processed

tickers=["AAPL", "UPST", "UBER", "SHOP"]
lstm = Handler()

for ticker in tickers:
    tickerHistoryResponse = requests.get(url+"historical-price-full/"+ticker+"?apikey="+apiKey)    
    print(" running ticker trainer", tickerHistoryResponse.text)
    tickerHistoryDf = json.loads(tickerHistoryResponse.text)
    print(type(tickerHistoryDf))
    # load ticker history
    lstm.train()
