


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


class StockRequest:


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
        query=self.params.get('query')


        if(query is None or len(query) < 1):
            return self.response_404

        if(query == "chart"):
            return self.__get_stock_history()
        
        if(query == "alerts"):
            return self.__get_stock_alerts()

        if(query == "profile"):
            return self.__get_stock_profile()

        if(query == "overview"):
            return self.__get_stock_overview()



        return self.response_404






    def __get_stock_history(self):
        try:
            filter=self.params.get('filter')
            ticker = self.params.get('ticker')   

            if(ticker is None or len(ticker) < 1):
                raise Exception('symbol is None or len(symbol) < 1')

            if(filter is None):
                raise Exception('period is None or len(symbol) < 1')


            if(filter == "def" or filter == 'DAILY'):
                results = []
                apiKey = os.getenv("FMG_KEY")
                url = os.getenv("FMG_URL")

                historicalDailly = requests.get(url+"historical-price-full/"+ticker+"?apikey="+apiKey)

                if historicalDailly.status_code == 200:
                    results = json.loads(historicalDailly.content)
                    results = results.get('historical', [])

                    filteredResults = results[:150]
                    filteredResults = filteredResults[::-1]        

                    return {
                        "status":200,
                        "results":filteredResults
                    }
                else:
                    raise Exception('cant request DAILY historical')

                # if(period=="5D"):
                #     historical5minReply = requests.get(url+"historical-chart/1hour/"+symbol+"?apikey="+apiKey)

                #     if historical5minReply.status_code == 200:
                #         results = json.loads(historical5minReply.content)[:33]
                #         results.reverse()




           
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_stock_alerts(self):
        try:

            filter=self.params.get('filter')
            ticker = self.params.get('ticker')


            if(filter == "5days"):

                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                stockAlertsCursor = self.db[alertsAnalysisColl].find_one( {'ticker':ticker}, {"_id":0, "name":0, "ticker":0} )
             
                alertsListStr = dumps(list(stockAlertsCursor))
                alerts_list = json.loads(alertsListStr)
                alerts_result = []
                for alertStr in alerts_list:
                    #TODO:
                    # return only 5days recent objects

                    alertObj = {
                        "name": alertStr.replace("_", " "),
                        "item":stockAlertsCursor[alertStr]
                    }
                    alerts_result.append(alertObj)
                    
                last_updated = last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":alerts_result,
                    "last_updated":last_updated
                }

            elif(filter == "all" or filter =="def"):
                
                alertsAnalysisColl = os.getenv("ALERTS_ANALYSIS_COLLECTION")

                startDate = date.today() - timedelta(5)
                startDate = startDate.strftime('%Y-%m-%d')

                stockAlertsCursor = self.db[alertsAnalysisColl].find_one( {'ticker':ticker}, {"_id":0, "name":0, "ticker":0} )
                
                if stockAlertsCursor is None:
                    return {
                        "status":200,
                        "results":[],
                    }

                alertsListStr = dumps(list(stockAlertsCursor))
                alerts_list = json.loads(alertsListStr)
                alerts_result = []
                for alertStr in alerts_list:
                    alertObj = {
                        "name": alertStr.replace("_", " "),
                        "item":stockAlertsCursor[alertStr]
                    }
                    alerts_result.append(alertObj)
                    
                last_updated = last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
     

                return {
                    "status":200,
                    "results":alerts_result,
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_stock_profile(self):
        try:
            print(" am at ")
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


    def __get_stock_overview(self):
        try:
            filter = self.params.get('filter')
            ticker = self.params.get('ticker')

            if(ticker is None or len(ticker) < 1):
                raise Exception('ticker is None or len(ticker) < 1')

            if(filter == "def"):


                apiKey = os.getenv("FMG_KEY")
                url = os.getenv("FMG_URL")

                stockInfoReply = requests.get(url+"quote/"+ticker+"?apikey="+apiKey)
                stockInfo = json.loads(stockInfoReply.text)[0]

                results = [
                    {"ticker":ticker},
                    {"name":'{name}'.format_map(stockInfo)},
                    {"price": '${price}'.format_map(stockInfo)},
                    {"open": '${open}'.format_map(stockInfo)},
                    {"change":  '${change:.2f} ({changesPercentage:.2f}%)'.format_map(stockInfo)},
                    {"volume": '$%s' %shortBigNumbers(stockInfo['volume'])},
                    {"market cap":'$%s' %shortBigNumbers(stockInfo['marketCap'])},
                    {"day range":'${dayLow:.2f} - ${dayHigh:.2f}'.format_map(stockInfo)},
                ]

                return {
                    "status":200,
                    "results":results,
                }


            else:
                raise Exception('cant serve ticker')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404




        # historicalHourReply = requests.get(self.fmgURL+"historical-chart/1hour/"+ticker['ticker']+"?apikey="+self.fmgKey)

        # if historicalHourReply.status_code == 200:
        #     historicalHourData = json.loads(historicalHourReply.content)
        #     tickerChartData=[]
        #     for item in historicalHourData[:5]:
        #         tickerChartData.append({
        #             "date": item['date'],
        #             "price": item['open']
        #         })
                
        #     return {
        #         "ticker": ticker['ticker'],
        #         "name": ticker['name'],
        #         "new_high": ticker['new_high'],
        #         "chartData": tickerChartData
        #     }

        # return {}







def shortBigNumbers(bigNumber):
    bigNumber = float('{:.3g}'.format(bigNumber))
    magnitude = 0
    while abs(bigNumber) >= 1000:
        magnitude += 1
        bigNumber /= 1000.0
    return '{}{}'.format('{:f}'.format(bigNumber).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])