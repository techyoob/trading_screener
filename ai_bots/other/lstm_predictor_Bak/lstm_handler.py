


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
plt.style.use('ggplot')

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout




import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()







class Handler:



    def __init__(self):
        print(" init lstm handler")




    def train(self, data):
        # df = pd.DataFrame(data['historical'])


        df = pd.read_csv(r'D:\screener_project\ai_bots\lstm_predictor\AAPL.csv')

        df = df['open'].values
        df = df.reshape(-1, 1)
        df[:7]
        
        dataset_train = np.array(df[:int(df.shape[0]*0.8)])
        dataset_test = np.array(df[int(df.shape[0]*0.8)-50:])
        
        
        scaler = MinMaxScaler(feature_range=(0, 1))
        dataset_train = scaler.fit_transform(dataset_train)
        dataset_train[:7]

        dataset_test = scaler.transform(dataset_test)
        dataset_test[:7]

        dataset_test = scaler.transform(dataset_test)


        def create_my_dataset(df):
            x = []
            y = []
            for i in range(50,df.shape[0]):
                x.append(df[i-50:i,0])
                y.append(df[i,0])
            x = np.array(x)
            y = np.array(y)
            return x,y


        x_train, y_train = create_my_dataset(dataset_train)
        x_train[:1]
        y_train[:1]


        x_test, y_test = create_my_dataset(dataset_test)
        x_test[:1]

        x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))

        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        model = Sequential()
        model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1],1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=96, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=96))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))


        model.compile(loss='mean_squared_error', optimizer ='adam')

        model.fit(x_train, y_train, epochs=50, batch_size=32)

        path = os.getenv("TRAINED_MODELS_PATH")
        name = '%s_ltsm_predictor.h5' %(data['symbol'])
        model.save(path+name)



        model = load_model(path+name)


        #visualizing our predictions
        
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        fig, ax = plt.subplots(figsize=(8,4))
        plt.plot(df, color='red', label='original Stockprice')
        ax.plot(range(len(y_train)+50, len(y_train)+50+len(predictions)),predictions,color='blue', label='predicted')
        plt.legend()


