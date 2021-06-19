



import talib
import pandas as pd
from pymongo import MongoClient
from io import StringIO
from datetime import date, datetime
import time
import requests
import json
from bson.json_util import dumps

import os
from dotenv import load_dotenv
load_dotenv()
# today = date.today()




class AlertThreads:


    response_404 = {
        "status":"error",
        "details":""
    }

    response_200 = {
        "status":'success',
        "details":""
    }

    print('Threads')




    def __init__(self):
        print('Initializing Alert threads')
        dbName = os.getenv("DB_NAME")
        url = os.getenv("DB_URL")
        alertsCollectionName = os.getenv("ALERTS_COLL")

        self.dbClient=MongoClient(url)
        db=MongoClient(url)[dbName]
        self.alertsCollection=db[alertsCollectionName]


        self.fmgKey = os.getenv("FMG_KEY")
        self.fmgURL = os.getenv("FMG_URL")


        f = open ('alertsCollectionModel.json', "r")
        self.alertsModels = json.loads(f.read())




    def executeAlert(self, params):

        alert = params.get('alert', 'invalid')

        if(alert['name'] == "invalid"):
            print('Alert type error')
        
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

        elif(alert['name'] == "bollinger_band_squeeze"):
            return self.__bollinger_band_squeeze_alert(params)





    ############################################################
    #
    #                       NEW HIGH
    #
    #############################################################

    def __new_high_alert(self, params):
        try:
            todayStr=date.today().strftime('%Y-%m-%d')
            stock = params['stock']
            currentAlert=params.get('currentAlert', {})
            historicalDf=params.get('historicalDf', [])
            tickerCurrentJson=params.get('tickerCurrentJson', {})

            lastUpdatedStr = currentAlert.get('last_updated', "1970-01-01")
            lastUpdated = datetime.strptime(lastUpdatedStr, "%Y-%m-%d").date()


            if(lastUpdated  < datetime.today().date()):
                filteredHistorical = historicalDf[ historicalDf['date'] > lastUpdatedStr]
 
                if len(filteredHistorical) > 0:
                    targetdayRows = filteredHistorical[ filteredHistorical['high']==filteredHistorical['high'].max() ]
                    targetdayRows = targetdayRows[ targetdayRows['date']==targetdayRows['date'].min() ]

                    historyHighest = targetdayRows['high'].iloc[0]

                    if(historyHighest > currentAlert['price']):
                        currentAlert['price'] = historyHighest
                        currentAlert['price_date'] = targetdayRows['date'].iloc[0]


            if isinstance(tickerCurrentJson, list) & len(tickerCurrentJson) > 0:
                todayHigh = tickerCurrentJson[0].get('dayHigh', 0)
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
                print('error reading current ticker data')
                return self.response_404

            return self.response_200

        except Exception as e:
            print('Error processing ticker with ticker ', e)
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
            currentAlert=params.get('currentAlert', {})
            historicalDf=params.get('historicalDf', [])
            tickerCurrentJson=params.get('tickerCurrentJson', {})

            lastUpdatedStr = currentAlert.get('last_updated', "1970-01-01")
            lastUpdated = datetime.strptime(lastUpdatedStr, "%Y-%m-%d").date()


            if(lastUpdated  < datetime.today().date()):
                filteredHistorical = historicalDf[ historicalDf['date'] >= lastUpdatedStr]

                if len(filteredHistorical) > 0:
                    targetdayRows = filteredHistorical[ filteredHistorical['low']==filteredHistorical['low'].min() ]
                    targetdayRows = targetdayRows[ targetdayRows['date']==targetdayRows['date'].min() ]
                    historyLowest = targetdayRows['low'].iloc[0]

                    if(historyLowest < currentAlert['price']):
                        currentAlert['price'] = historyLowest
                        currentAlert['price_date'] = targetdayRows['date'].iloc[0]


            if isinstance(tickerCurrentJson, list) & len(tickerCurrentJson) > 0:
                todayLow = tickerCurrentJson[0].get('dayLow', 0)
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
                print('error reading current ticker data')
                return self.response_404


            return self.response_200
            
        except Exception as e:
            print('Error processing ticker with ticker ', e)
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
            print('Error processing ticker with ticker ', e)
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
            print('Error processing ticker with ticker ', e)
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
            print('Error processing ticker with ticker ', e)
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
            print('Error processing ticker with ticker ', e)
            return self.response_404





    ############################################################
    #
    #                   Bollinger Band Squeeze
    #
    #############################################################

    def __bollinger_band_squeeze_alert(self, params):
        try:
            #TODO:
            # + get 1 minute data history 
            # + process bb wit talib
            # + detect a squeeze
            # + if squeeze detected, analyze whether buy or sell
            # + 

            return self.response_200
            
        except Exception as e:
            print('Error processing ticker with ticker ', e)
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