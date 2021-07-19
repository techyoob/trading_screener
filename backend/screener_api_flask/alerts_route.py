


import talib
import pandas as pd
from pymongo import MongoClient
from io import StringIO
from datetime import date, datetime, timedelta
import time
import requests
import json
from bson.json_util import dumps

import os
from dotenv import load_dotenv
load_dotenv()
today = date.today()


class AlertRequest:


    response_404 = {
        "status":404,
        "results":[]
    }

    response_200 = {
        "status":200,
        "results":[]
    }









    def __init__(self, params):
        
        name = os.getenv("DB_NAME")
        url = os.getenv("DB_URL")


        self.fmgKey = os.getenv("FMG_KEY")
        self.fmgURL = os.getenv("FMG_URL")

        self.params=params
        self.dbClient=MongoClient(url)
        self.db=MongoClient(url)[name]


    def getRequest(self):
        alert=self.params.get('query')


        if(alert is None or len(alert) < 1):
            return self.response_404

        if(alert == "new high"):
            return self.__get_new_high()
        
        if(alert == "new low"):
            return self.__get_new_low()

        if(alert == "new high ask"):
            return self.__get_new_high_ask()

        if(alert == "new low ask"):
            return self.__get_new_low_ask()

        if(alert == "new high bid"):
            return self.__get_new_high_bid()

        if(alert == "new low bid"):
            return self.__get_new_low_bid()

        if(alert == "bollinger bands"):
            return self.__get_bollinger_bands()

        if(alert == "moving average"):
            return self.__get_moving_average()

        return self.response_404






    def __get_new_high(self):
        try:
            filter=self.params.get('filter')

            if(filter == "5days"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                # newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.last_updated':{"$gte": startDate}} )

                # TODO:
                # Uncomment below for real results

                newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.price_date':{ "$gte": startDate }}, {"_id":0, "new_high":1, "name":1, "ticker":1}).limit(50)

                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")

                return {
                    "status":200,
                    "results":new_high_list,
                    "last_updated":last_updated
                }

            elif(filter == "all"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")
                newHighListCursor = self.db[alertsAnalysisColl].find({}, {"_id":0, "new_high":1, "name":1, "ticker":1}).limit(50)
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")


                return {
                    "status":200,
                    "results":new_high_list,
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_new_low(self):
        try:
            filter=self.params.get('filter')
            if(filter == "5days"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                # newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.last_updated':{"$gte": startDate}} )
                newLowListCursor = self.db[alertsAnalysisColl].find( {'new_low.price_date':{ "$gte": startDate }}, {"_id":0, "new_low":1, "name":1, "ticker":1} ).limit(50)
             
                newLowListStr = dumps(list(newLowListCursor))
                new_low_list = json.loads(newLowListStr)
                last_updated = last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":new_low_list,
                    "last_updated":last_updated
                }

            elif(filter == "all"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION") 
                newLowListCursor = self.db[alertsAnalysisColl].find({}, {"_id":0, "new_low":1, "name":1, "ticker":1}).limit(50)

                newLowListStr = dumps(list(newLowListCursor))
                new_low_list = json.loads(newLowListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":new_low_list,
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_new_high_ask(self):
        try:
            print(" am at __get_new_high_ask")
            filter=self.params.get('filter')

            if(filter == "something"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                # newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.last_updated':{"$gte": startDate}} )

                # TODO:
                # Uncomment below for real results

                newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.price_date':{ "$gte": startDate }}, {"_id":0, "new_high":1, "name":1, "ticker":1} )
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":new_high_list,
                    "last_updated":last_updated
                }

            elif(filter == "all"):


                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                newHighListCursor = self.db[alertsAnalysisColl].find({}, {"_id":0, "new_high":1, "name":1, "ticker":1})
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":"__get_new_low",
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_new_low_ask(self):
        try:
            print(" am at __get_new_low_ask")
            filter=self.params.get('filter')

            if(filter == "something"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                # newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.last_updated':{"$gte": startDate}} )

                # TODO:
                # Uncomment below for real results

                newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.price_date':{ "$gte": startDate }}, {"_id":0, "new_high":1, "name":1, "ticker":1} )
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":new_high_list,
                    "last_updated":last_updated
                }

            elif(filter == "all"):


                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                newHighListCursor = self.db[alertsAnalysisColl].find({}, {"_id":0, "new_high":1, "name":1, "ticker":1})
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":"__get_new_low",
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_new_high_bid(self):
        try:
            print(" am at __get_new_high_bid")
            filter=self.params.get('filter')

            if(filter == "something"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                # newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.last_updated':{"$gte": startDate}} )

                # TODO:
                # Uncomment below for real results

                newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.price_date':{ "$gte": startDate }}, {"_id":0, "new_high":1, "name":1, "ticker":1} )
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":new_high_list,
                    "last_updated":last_updated
                }

            elif(filter == "all"):


                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                newHighListCursor = self.db[alertsAnalysisColl].find({}, {"_id":0, "new_high":1, "name":1, "ticker":1})
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":"__get_new_low",
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_new_low_bid(self):
        try:
            print(" am at __get_new_low_bid")
            filter=self.params.get('filter')

            if(filter == "something"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                # newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.last_updated':{"$gte": startDate}} )

                # TODO:
                # Uncomment below for real results

                newHighListCursor = self.db[alertsAnalysisColl].find( {'new_high.price_date':{ "$gte": startDate }}, {"_id":0, "new_high":1, "name":1, "ticker":1} )
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":new_high_list,
                    "last_updated":last_updated
                }

            elif(filter == "all"):


                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                newHighListCursor = self.db[alertsAnalysisColl].find({}, {"_id":0, "new_high":1, "name":1, "ticker":1})
             
                newHighListStr = dumps(list(newHighListCursor))
                new_high_list = json.loads(newHighListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":"__get_new_low",
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_bollinger_bands(self):
        try:
            print(" am at __get_bollinger_bands")
            filter=self.params.get('filter')

            if(filter == "something"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")
                currentDate = date.today().strftime('%Y-%m-%d')
                bollingerBandsListCursor = self.db[alertsAnalysisColl].find( {'bollinger_bands.signal_date':{ "$eq": currentDate }}, {"_id":0, "bollinger_bands":1, "name":1, "ticker":1} )
             
                # bollingerBandsListStr = dumps(list(bollingerBandsListCursor))
                # bollinger_bands_list = json.loads(bollingerBandsListStr)

                bollingerBandsList=list(bollingerBandsListCursor)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":bollingerBandsList,
                    "last_updated":last_updated
                }

            elif(filter == "all"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")
                currentDate = date.today().strftime('%Y-%m-%d')
                bollingerBandsListCursor = self.db[alertsAnalysisColl].find( {'bollinger_bands':{ "$exists": True }}, {"_id":0, "bollinger_bands":1, "name":1, "ticker":1} ).limit(50)
             
             
                # bollingerBandsListStr = dumps(list(bollingerBandsListCursor))
                # bollinger_bands_list = json.loads(bollingerBandsListStr)
                bollingerBandsList=list(bollingerBandsListCursor)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":bollingerBandsList,
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_moving_average(self):
        try:
            print(" am at __get_bollinger_bands")
            filter=self.params.get('filter')

            if(filter == "something"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")
                currentDate = date.today().strftime('%Y-%m-%d')

                movingAverageListCursor = self.db[alertsAnalysisColl].find(
                                {'moving_average':{ '$elemMatch': { "sma":{"$in":['buy', 'sell']}, "ema":{"$in":['buy', 'sell']}} }}
                                ,{"_id":0, "moving_average":1, "name":1, "ticker":1}).limit(50)

                movingAverageListStr = dumps(list(movingAverageListCursor))
                movingAverageList = json.loads(movingAverageListStr)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")


                return {
                    "status":200,
                    "results":movingAverageList,
                    "last_updated":last_updated
                }

            elif(filter == "all"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")
                # fromDate = date.today().strftime('%Y-%m-%d')
                fromDate = datetime.now() - timedelta(3)



                movingAverageListCursor = self.db[alertsAnalysisColl].find( { "$or":[
                                                        { "moving_average.sma":{"$in":['sell', 'buy']}, "moving_average.sma_date":{ "$gt": fromDate.strftime('%Y-%m-%d %H:%M:%S')} },
                                                        { "moving_average.ema":{"$in":['sell', 'buy']}, "moving_average.ema_date":{ "$gte": fromDate.strftime('%Y-%m-%d %H:%M:%S')}  }
                                                 ] }
                                                ,{"_id":0, "moving_average":1, "name":1, "ticker":1}).limit(50)

      
        
                movingAverageList = list(movingAverageListCursor)
                last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":movingAverageList,
                    "last_updated":last_updated
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


# ##############################################################
#
#               Helper Functions
#
# ##############################################################


    def __aggregateTickerMiniChart(self, ticker):

        historicalHourReply = requests.get(self.fmgURL+"historical-chart/1hour/"+ticker['ticker']+"?apikey="+self.fmgKey)

        if historicalHourReply.status_code == 200:
            historicalHourData = json.loads(historicalHourReply.content)
            tickerChartData=[]
            for item in historicalHourData[:5]:
                tickerChartData.append({
                    "date": item['date'],
                    "price": item['open']
                })
                
            return {
                "ticker": ticker['ticker'],
                "name": ticker['name'],
                "new_high": ticker['new_high'],
                "chartData": tickerChartData
            }

        return {}