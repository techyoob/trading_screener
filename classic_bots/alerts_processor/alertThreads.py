



import talib
import pandas as pd
import numpy as np
from pymongo import MongoClient
from io import StringIO
from datetime import date, datetime
import time
import requests
import json
from bson.json_util import dumps
import logging

import os
from dotenv import load_dotenv
load_dotenv()




class AlertThreads:


    response_404 = {
        "status":"error",
        "details":""
    }

    response_200 = {
        "status":'success',
        "details":""
    }





    def __init__(self):
        logging.info(' Initializing Alert threads')
        dbName = os.getenv("DB_NAME")
        url = os.getenv("DB_URL")
        alertsCollectionName = os.getenv("ALERTS_COLL")

        self.dbClient=MongoClient(url)
        db=MongoClient(url)[dbName]
        self.alertsCollection=db[alertsCollectionName]


        self.fmgKey = os.getenv("FMG_KEY")
        self.fmgURL = os.getenv("FMG_URL")





    def executeAlert(self, params):

        alert = params.get('alert', 'invalid')

        if(alert['name'] == "invalid"):
            logging.warning(' Unknow alert name')
        
        elif(alert['name'] == "new_high"):
            return self.__new_high_alert(params)

        elif(alert['name'] == "new_low"):
            return self.__new_low_alert(params)

        elif(alert['name'] == "new_high_ask"):
            return self.__new_high_ask_alert(params)

        elif(alert['name'] == "new_low_ask"):
            return self.__new_low_ask_alert(params)

        elif(alert['name'] == "new_high_bid"):
            return self.__new_high_bid_alert(params)

        elif(alert['name'] == "new_low_bid"):
            return self.__new_low_bid_alert(params)

        elif(alert['name'] == "bollinger_bands"):
            return self.__bollinger_bands_signal_alert(params)

        elif(alert['name'] == "moving_average"):
            return self.__moving_average_alert(params)





    ############################################################
    #
    #                       NEW HIGH
    #
    #############################################################

    def __new_high_alert(self, params):
        try:
            todayStr=date.today().strftime('%Y-%m-%d')
            stock = params['stock']
            alert=params.get('alert', {})
            historicalDailyArr=params.get('historicalDailyArr', [])
            tickerQuoteJson=params.get('tickerQuoteJson', {})
            historicalDailyDf=[]

            if(len(historicalDailyArr)>0):
                historicalDailyDf = pd.DataFrame(historicalDailyArr)
            else:
                logging.warning(" Cannot get daily historical price data for %s" %stock['ticker'])
                raise
            

            currentAlert={}
            tickerAlertsCursor = self.alertsCollection.find_one( {"ticker":stock['ticker'], alert['name']: {'$exists':True}} )

            if(tickerAlertsCursor == None):
                currentAlert = alert.get('model', {}).copy()
            else:
                currentAlert=tickerAlertsCursor.get(alert['name'], alert['model'])

            if(len(currentAlert)  < 1):
                return

            lastUpdatedStr = currentAlert.get('last_updated', "1970-01-01")
            lastUpdated = datetime.strptime(lastUpdatedStr, "%Y-%m-%d").date()


            if(lastUpdated  < datetime.today().date()):
                filteredHistorical = historicalDailyDf[ historicalDailyDf['date'] > lastUpdatedStr]
 
                if len(filteredHistorical) > 0:
                    targetdayRows = filteredHistorical[ filteredHistorical['high']==filteredHistorical['high'].max() ]
                    targetdayRows = targetdayRows[ targetdayRows['date']==targetdayRows['date'].min() ]

                    historyHighest = targetdayRows['high'].iloc[0]

                    if(historyHighest > currentAlert['price']):
                        currentAlert['price'] = historyHighest
                        currentAlert['price_date'] = targetdayRows['date'].iloc[0]


            if isinstance(tickerQuoteJson, list) & len(tickerQuoteJson) > 0:
                todayHigh = tickerQuoteJson[0].get('dayHigh', 0)
                if(todayHigh > currentAlert['price']):
                    currentAlert['price'] = todayHigh
                    currentAlert['price_date'] = todayStr

                currentAlert['last_updated']=todayStr


                updatedtickerDoc = {
                    "ticker":stock['ticker'],
                    "name":stock['name'],
                    "new_high":currentAlert
                }

                # print('new high for %s is - %s ' %(updatedtickerDoc['ticker'], updatedtickerDoc['new_high']))

                self.alertsCollection.find_one_and_update({'ticker':stock['ticker'] }, {'$set': updatedtickerDoc}, upsert=True)
            else:
                logging.warning(' Cannot read ticker  %s data while processing new high alert' %stock['ticker'])
                return self.response_404

            return self.response_200

        except Exception as e:
            stock = params['stock']
            logging.error(' Error proccessing new high alert for ticker %s ' %stock['ticker'])
            #print('Error processing ticker with ticker ', e)
            return self.response_404




    ############################################################
    #
    #                       NEW LOW
    #
    #############################################################

    def __new_low_alert(self, params):
        try:

            todayStr=date.today().strftime('%Y-%m-%d')
            stock = params['stock']
            alert=params.get('alert', {})
            historicalDailyArr=params.get('historicalDailyArr', [])
            tickerQuoteJson=params.get('tickerQuoteJson', {})
            historicalDailyDf=[]
            
            if(len(historicalDailyArr)>0):
                historicalDailyDf = pd.DataFrame(historicalDailyArr)
            else:
                logging.warning(" Cannot get daily historical price data for %s" %stock['ticker'])
                raise
            
            currentAlert={}
            tickerAlertsCursor = self.alertsCollection.find_one( {"ticker":stock['ticker'], alert['name']: {'$exists':True}} )

            if(tickerAlertsCursor == None):
                currentAlert = alert.get('model', {}).copy()
            else:
                currentAlert=tickerAlertsCursor.get(alert['name'], alert['model'])

            if(len(currentAlert)  < 1):
                return


            lastUpdatedStr = currentAlert.get('last_updated', "1970-01-01")
            lastUpdated = datetime.strptime(lastUpdatedStr, "%Y-%m-%d").date()


            if(lastUpdated  < datetime.today().date()):
                filteredHistorical = historicalDailyDf[ historicalDailyDf['date'] >= lastUpdatedStr]

                if len(filteredHistorical) > 0:
                    targetdayRows = filteredHistorical[ filteredHistorical['low']==filteredHistorical['low'].min() ]
                    targetdayRows = targetdayRows[ targetdayRows['date']==targetdayRows['date'].min() ]
                    historyLowest = targetdayRows['low'].iloc[0]

                    if(historyLowest < currentAlert['price']):
                        currentAlert['price'] = historyLowest
                        currentAlert['price_date'] = targetdayRows['date'].iloc[0]


            if isinstance(tickerQuoteJson, list) & len(tickerQuoteJson) > 0:
                todayLow = tickerQuoteJson[0].get('dayLow', 0)
                if(todayLow < currentAlert['price']):
                    currentAlert['price'] = todayLow
                    currentAlert['price_date'] = todayStr

                currentAlert['last_updated']=todayStr

                updatedtickerDoc = {
                    "ticker":stock['ticker'],
                    "name":stock['name'],
                    "new_low":currentAlert
                }

                # print('new low for %s is - %s ' %(updatedtickerDoc['ticker'], updatedtickerDoc['new_low']))

                self.alertsCollection.find_one_and_update({'ticker':stock['ticker'] }, {'$set': updatedtickerDoc}, upsert=True)
            else:
                # print('error reading current ticker data')
                logging.warning(' Cannot read ticker %s data while processing new low alert!' %stock['ticker'])
                return self.response_404


            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)
            stock = params['stock']
            logging.error(' Error proccessing new low alert for ticker %s ' %stock['ticker'])
            return self.response_404




    ############################################################
    #
    #                       NEW HIGH ASK
    #
    #############################################################

    def __new_high_ask_alert(self, params):
        try:
            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)
            stock = params['stock']
            logging.error(' Error proccessing new high ask alert for ticker %s ' %stock['ticker'])
            return self.response_404




    ############################################################
    #
    #                       NEW LOW ASK
    #
    #############################################################

    def __new_low_ask_alert(self, params):
        try:
            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)

            stock = params['stock']
            logging.error(' Error proccessing new low ask alert for ticker %s ' %stock['ticker'])
            return self.response_404



    ############################################################
    #
    #                       NEW HIGH BID
    #
    #############################################################

    def __new_high_bid_alert(self, params):
        try:
            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)

            stock = params['stock']
            logging.error(' Error proccessing new high bid alert for ticker %s ' %stock['ticker'])
            return self.response_404



    ############################################################
    #
    #                       NEW LOW BID
    #
    #############################################################

    def __new_low_bid_alert(self, params):
        try:
            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)

            stock = params['stock']
            logging.error(' Error proccessing new low bid alert for ticker %s ' %stock['ticker'])
            return self.response_404





    ############################################################
    #
    #                   Bollinger Bands signals
    #
    #############################################################

    def __bollinger_bands_signal_alert(self, params):
        try:
            #TODO:
            # + get 1 minute data history 
            # + process bb wit talib
            # + detect a squeeze
            # + if squeeze detected, analyze whether buy or sell
            # + signal can be "NONE" "SELL" "BUY"

            stock = params['stock']
            alert=params.get('alert', {})
            currentAlert={}
            currentAlert = alert.get('model', {}).copy()
            if(len(currentAlert)  < 1):
                raise


            historical1MinArr=params.get('historical1MinArr', [])
            df=[]
            if(len(historical1MinArr)>0):
                df = pd.DataFrame(historical1MinArr[::-1])
            else:
                logging.warning(" Cannot get daily historical price data for %s" %stock['ticker'])
                raise


            df = df.set_index(pd.DatetimeIndex( df['date'].values).strftime('%Y-%m-%d %H:%M:%S'))

            period = 20
            upper, middle, lower = talib.BBANDS(df['close'], 
                                            timeperiod=period,
                                            nbdevup=1,
                                            nbdevdn=1,
                                            matype=0)

            df['middle']=middle
            df['upper']=upper
            df['lower']=lower

            signal = [] 
            signal_price = [] 
            for i in range(len(df['close'])):
                if df['close'][i] > df['upper'][i]:                   
                    signal.append("sell")
                    signal_price.append(df['close'][i])

                elif df['close'][i] < df['lower'][i]:
                    signal.append("buy")
                    signal_price.append(df['close'][i])
                    
                else:
                    signal.append("none")
                    signal_price.append(np.nan)
                    

            df['signal'] =  signal
            df['signal_price'] =  signal_price


            for index, row in df.iloc[::-1].iterrows():
                if(row['signal']=='none'):
                    continue                
                
                if(row['signal']=='buy'):
                    if(currentAlert['signal']=='sell'):
                        break
                    elif(currentAlert['signal']=='none'):
                        currentAlert['signal']='buy'
                        currentAlert['signal_price']=row['close']
                        currentAlert['signal_date']=row['date']
                        currentAlert['renewed']=1
                        continue
                    elif(currentAlert['signal']=='buy'):
                        currentAlert['renewed']+=1
                        continue

                if(row['signal']=='sell'):
                    if(currentAlert['signal']=='buy'):
                        break
                    elif(currentAlert['signal']=='none'):
                        currentAlert['signal']='sell'
                        currentAlert['signal_price']=row['close']
                        currentAlert['signal_date']=row['date']
                        currentAlert['renewed']=1
                        continue
                    elif(currentAlert['signal']=='sell'):
                        currentAlert['renewed']+=1
                        continue

            currentAlert['last_updated']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            updatedtickerDoc = {
                "ticker":stock['ticker'],
                "name":stock['name'],
                "bollinger_bands":currentAlert
            }

            # print('bollinger alert for %s is - %s ' %(updatedtickerDoc['ticker'], updatedtickerDoc['bollinger_bands']))
            self.alertsCollection.find_one_and_update({'ticker':stock['ticker'] }, {'$set': updatedtickerDoc}, upsert=True)

            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)

            stock = params['stock']
            logging.error(' Error proccessing bollinger band alert for ticker %s ' %stock['ticker'])
            return self.response_404






    ############################################################
    #
    #                   Moving Average Signals 
    #
    #############################################################

    def __moving_average_alert(self, params):
        try:

            stock = params['stock']
            alert=params.get('alert', {})
            currentAlert={}
            currentAlert = alert.get('model', {}).copy()
            if(len(currentAlert)  < 1):
                return

            historical1MinArr=params.get('historical1MinArr', [])
            historical1MinDf=[]


            if(len(historical1MinArr)>0):
                historical1MinDf = pd.DataFrame(historical1MinArr[::-1])
            else:
                logging.warning(" Cannot get daily historical price data for %s" %stock['ticker'])
                raise


            historical1MinDf = historical1MinDf.set_index(pd.DatetimeIndex( historical1MinDf['date'].values).strftime('%Y-%m-%d %H:%M:%S'))



            historical1MinDf['sma20'] = talib.SMA(historical1MinDf['close'], timeperiod=20)
            historical1MinDf['sma100'] = talib.SMA(historical1MinDf['close'], timeperiod=100)
            historical1MinDf['sma_signal'] = 0.0
            historical1MinDf['sma_signal'] = np.where(historical1MinDf['sma20'] > historical1MinDf['sma100'], 1.0, 0.0)


            historical1MinDf['ema20'] = talib.EMA(historical1MinDf['close'], timeperiod=20)
            historical1MinDf['ema100'] = talib.EMA(historical1MinDf['close'], timeperiod=100)
            historical1MinDf['ema_signal'] = 0.0
            historical1MinDf['ema_signal'] = np.where(historical1MinDf['ema20'] > historical1MinDf['ema100'], 1.0, 0.0)


            historical1MinDf['sma_position'] = historical1MinDf['sma_signal'].diff()
            historical1MinDf['ema_position'] = historical1MinDf['ema_signal'].diff()

            
            lastHourDf = historical1MinDf.tail(60)
            for index, row in lastHourDf.iloc[::-1].iterrows():

                if (currentAlert['ema']!='none') and (currentAlert['sma']!='none'):
                    break

                if(row['sma_position']!=0 and currentAlert['sma']=='none'):
                    currentAlert['sma']= 'buy' if row['sma_position'] == 1 else 'sell' if row['sma_position'] == -1 else 'none'
                    currentAlert['sma_date'] = row['date']
                    currentAlert['sma_price'] = row['close']

                if(row['ema_position']!=0 and currentAlert['ema']=='none'):
                    currentAlert['ema']= 'buy' if row['ema_position'] == 1 else 'sell' if row['ema_position'] == -1 else 'none'
                    currentAlert['ema_date'] = row['date']
                    currentAlert['ema_price'] = row['close']


            currentAlert['last_updated']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            updatedtickerDoc = {
                "ticker":stock['ticker'],
                "name":stock['name'],
                "moving_average":currentAlert
            }

            # print('moving_average alert for %s is - %s ' %(updatedtickerDoc['ticker'], updatedtickerDoc['bollinger_bands']))
            self.alertsCollection.find_one_and_update({'ticker':stock['ticker'] }, {'$set': updatedtickerDoc}, upsert=True)



            return self.response_200
            
        except Exception as e:
            # print('Error processing ticker with ticker ', e)

            stock = params['stock']
            logging.error(' Error proccessing new low bid alert for ticker %s ' %stock['ticker'])
            return self.response_404









    ############################################################
    #
    #                       Helper Functions 
    #
    #############################################################


def isBusinessHours():
    today=date.today().strftime('%Y-%m-%d')

    # TODO:
    # Check if market is open
    # skip alert processing
    # Report Warning: market is closed


    # isMarketopenDataResponse = requests.get(self.fmgURL+"is-the-market-open"+"?apikey="+self.fmgKey)
    # ismarketOpen = isMarketopenDataResponse.json().get('isTheStockMarketOpen', False) 
    # if(ismarketOpen==False):
    #     return self.response_404