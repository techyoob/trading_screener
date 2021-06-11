

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout



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
# add config variables (1 day, 2 days, ...etc)











apiKey = os.getenv("FMG_KEY")
url = os.getenv("FMG_URL")

tickers=["AAPL", "UPST", "UBER", "SHOP"]
# tickers=["AAPL"]
# lstm = Handler()

for ticker in tickers:
    tickerHistoryResponse = requests.get(url+"historical-price-full/"+ticker+"?apikey="+apiKey)    
    processPredictions(tickerHistoryResponse.json())







def processPredictions(ticker):
    print('predicting for %s' %ticker)



