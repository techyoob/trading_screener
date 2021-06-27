




import os
import requests
import json


import numpy as np

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
import datetime
import time


import logging
reportPath=os.path.dirname(__file__)
reportFile=reportPath+'/lstm_forecasting.log' if len(reportPath)>0 else 'lstm_forecasting.log'
logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' LSTM forecasting has been started!')




apiKey = os.getenv("FMG_KEY")
url = os.getenv("FMG_URL")
mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")
lstmColl = os.getenv("LSTM_FORECASTING_COLLECTION")



tickers=["AAPL", "UPST", "UBER", "SHOP"]

client = MongoClient(mongoURL)
db = client[dbName]



def split_sequences(seq, n_steps_in, n_steps_out):
    X,y =[], []
    
    for i in range(len(seq)):
        end = i+n_steps_in
        out_end = end+ n_steps_out
        
        if out_end >len(seq):
            break
            
        seq_x, seq_y = seq[i:end], seq[end:out_end]
        
        X.append(seq_x)
        y.append(seq_y)
    
    return np.array(X), np.array(y)
    





def processForecasting(item,tickerHistory):
    try:
        
        df = pd.DataFrame(tickerHistory['historical'][::-1])
        df.tail()
        
        
        df = df.set_index("date")[['open']].tail(1000)
        df = df.set_index(pd.to_datetime(df.index))
        df.head()

        scaler = MinMaxScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns =df.columns, index=df.index)
        df.head()

        n_per_in = 15
        n_per_out = 5

        n_features = 1

        X,y = split_sequences(list(df.open), n_per_in,n_per_out)


        X = X.reshape(X.shape[0],X.shape[1],n_features)

        model = Sequential()
        model.add(LSTM(50, activation='softsign', return_sequences=True, input_shape=(n_per_in,n_features)))
        model.add(LSTM(15, activation='softsign', return_sequences=True))
        model.add(LSTM(15, activation='softsign', return_sequences=True))
        model.add(LSTM(15, activation='softsign', return_sequences=True))
        model.add(LSTM(15, activation='softsign', return_sequences=True))
        model.add(LSTM(15, activation='softsign'))
        model.add(Dense(n_per_out))

        model.summary()

        model.compile(optimizer='adam',loss='mse', metrics=['accuracy'])
        res = model.fit(X,y, epochs=60, batch_size=32, validation_split=0.1)
        


        yhat = model.predict(np.array(df.tail(n_per_in)).reshape(1,n_per_in,n_features)).tolist()[0]
        yhat = scaler.inverse_transform(np.array(yhat).reshape(-1,1)).tolist()

        def flatten(item):
            return item[0]

        preds_10_days = list( map(flatten, yhat))

        predsColl = db[lstmColl]

        date = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime("%H:%M:%S")

        preds = { "date": date,
                "time": time,
                "name": item['companyName'],
                "ticker":item['ticker'],
                "movement": "open",
                "forecasting": preds_10_days}


        predsColl.find_one_and_update({'ticker':tickerHistory['symbol']}, {'$set':preds}, upsert=True)

        return {
            "status":"success",
            "error":""
        }



    except Exception as e:
        # print('Error processing ticker with symbol  and reason is ', e)
        logging.warning(' Exception thrown while training LSTM model for %s ' %item['ticker'])

        return {
            "status":"error",
            "error":e
        }





mostGainersResponse = requests.get(url+"gainers?apikey="+apiKey)    

mostGainersTickers = mostGainersResponse.json()


for item in mostGainersTickers:
    tickerHistoryResponse = requests.get(url+"historical-price-full/"+item['ticker']+"?apikey="+apiKey)    
    result = processForecasting(item, tickerHistoryResponse.json())


logging.info(' LSTM forecasting finished!')


