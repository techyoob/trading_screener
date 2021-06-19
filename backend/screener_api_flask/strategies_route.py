


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
today = date.today()


class StrategyRequest:


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

        self.params=params
        self.dbClient=MongoClient(url)
        self.db=MongoClient(url)[name]


    def getRequest(self):
        strategy=self.params.get('strat')

        
        if(strategy is None or len(strategy) < 1):
            return self.response_404

        if(strategy == "big_bang"):
            return self. __get_big_bang()
        
        if(strategy == "patterns_analysis"):
            return self.__get_candlestick_patterns_analysis()

        if(strategy == "most_actives"):
            return self.__get_most_actives()

        if(strategy == "most_gainers"):
            return self.__get_most_gainers()

        if(strategy == "most_losers"):
            return self.__get_most_losers()

        if(strategy == "social_trends"):
            return self.__get_social_trends()

        return self.response_404






    def __get_big_bang(self):
        def mapLstmArray(item, itemInfo):

            
            return  {
                    "ticker":item['ticker'],
                    "forecasting":[{"1 day":item['forecasting'][0]},
                        {"2 days":item['forecasting'][1]},
                        {"5 days":item['forecasting'][4]} 
                    ],
                    "movement":item['movement'],
                    "current":{
                        "price":itemInfo['price'],
                        "percentage":itemInfo['changesPercentage'],
                        "change":itemInfo['change'],
                        "volume":itemInfo['volume'],
                        "day high":itemInfo['dayHigh'],
                        "day low":itemInfo['dayLow']
                    },
                    "date":item['date'],
                    "time":item['time']
                }
                



        try:
            filter=self.params.get('filter')

            if(filter == "top50"):

                collection = os.getenv("LSTM_FORECASTING_COLLECTION")

                lstm_list_cursor = self.db[collection].find().limit(50)
                lstm_list_str = dumps(list(lstm_list_cursor))
                lstm_list = json.loads(lstm_list_str)
                lstm_list_sorted = sorted(lstm_list, key = lambda i: i['ticker'])

                quoteStr=""
                for item in lstm_list_sorted:
                    quoteStr+=item['ticker']+','


                apiKey = os.getenv("FMG_KEY")
                url = os.getenv("FMG_URL")
                tickersQuoteResponse = requests.get(url+"quote/"+quoteStr+"?apikey="+apiKey)
                tickersQuote = json.loads(tickersQuoteResponse.text)


                mergedArray = map(mapLstmArray, lstm_list_sorted, tickersQuote)


                results = list(mergedArray)
                                
                last_updated = today.strftime("%d/%m/%Y %H:%M")
     

                return {
                    "status":200,
                    "results":results,
                    "last_update":last_updated
                }
         
            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404



    def __get_social_trends(self):
        try:
            filter=self.params.get('filter')

            if(filter == "top30"):
                                
                collection = os.getenv("SOCIAL_TREND_COLLECTION")
                recentTrend = today.strftime("%Y-%m-%d")

                # recentTrend=datetime(2021, 4, 16).strftime("%Y-%m-%d")

                social_trend_cursor = self.db[collection].find({'date':recentTrend}).limit(50)            

                social_trend_str = dumps(list(social_trend_cursor))
                social_trend_list = json.loads(social_trend_str)

                last_updated = today.strftime("%d/%m/%Y %H:%M")

                return {
                    "status":200,
                    "results":social_trend_list,
                    "last_update":last_updated,
                    "trends_date":""
                }

            else:
                raise Exception('Wrong filter name')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404



    def __get_most_gainers(self):

        def aggregateLoserTicker(ticker):
            
            # strategiesStr=self.params.get('strats')
            # strategies = strategiesStr.split(',')
            
            return {
                "name":ticker['companyName'],
                "ticker":ticker['ticker'],
                "price":ticker['price'],
                "changes":round(ticker['changes'], 2),
                "changes percentage":ticker['changesPercentage']
            }


        try:
            filter=self.params.get('filter')

            if(filter == "top30"):
                
                apiKey = os.getenv("FMG_KEY")
                url = os.getenv("FMG_URL")

                gainersTickersReply = requests.get(url+"gainers?apikey="+apiKey)
                gainersTickers = json.loads(gainersTickersReply.text)

                aggregateGainerTickersResult = map(aggregateLoserTicker, gainersTickers)

                results = list(aggregateGainerTickersResult)

                last_updated = today.strftime("%d/%m/%Y %H:%M")

                return {
                    "status":200,
                    "results":results,
                    "last_update":last_updated
                }



            elif(filter == "top30aggr"):
                print(" hello aggregate losers")
                return self.response_200


            else:
                raise Exception('filter is None or len(filter) < 1')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404



    def __get_most_losers(self):

        def aggregateLoserTicker(ticker):
            
            # strategiesStr=self.params.get('strats')
            # strategies = strategiesStr.split(',')

            
            return {
                "name":ticker['companyName'],
                "ticker":ticker['ticker'],
                "price":ticker['price'],
                "changes":ticker['changes'],
                "changes percentage":ticker['changesPercentage'],
                "strategies":{}
            }


        try:
            filter=self.params.get('filter')

            if(filter == "top30"):
                
                apiKey = os.getenv("FMG_KEY")
                url = os.getenv("FMG_URL")

                loserTickersReply = requests.get(url+"losers?apikey="+apiKey)
                loserTickers = json.loads(loserTickersReply.text)

                aggregateLoserTickersResult = map(aggregateLoserTicker, loserTickers)

                results = list(aggregateLoserTickersResult)

                last_updated = today.strftime("%d/%m/%Y %H:%M")

                return {
                    "status":200,
                    "results":results,
                    "last_update":last_updated
                }



            elif(filter == "top30aggr"):
                print(" hello aggregate losers")
                return self.response_200


            else:
                raise Exception('filter is None or len(filter) < 1')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404



    def __get_most_actives(self):

        def aggregateActiveTicker(ticker):
            
            # strategiesStr=self.params.get('strats')
            # strategies = strategiesStr.split(',')



            return {
                "name":ticker['companyName'],
                "ticker":ticker['ticker'],
                "price":ticker['price'],
                "changes":ticker['changes'],
                "changes percentage":ticker['changesPercentage'],
                "strategies":{
                    "strat I":"value"
                    }
                
            }


        try:
            filter=self.params.get('filter')

            if(filter == "top30"):
                apiKey = os.getenv("FMG_KEY")
                url = os.getenv("FMG_URL")

                activeTickersReply = requests.get(url+"actives?apikey="+apiKey)
                activeTickers = json.loads(activeTickersReply.text)

                aggrActiveTickersResult = map(aggregateActiveTicker, activeTickers)

                results = list(aggrActiveTickersResult)

                
                last_updated = today.strftime("%d/%m/%Y %H:%M")

                return {
                    "status":200,
                    "data":results,
                    "last_update":last_updated
                }

            elif(filter == "top30aggr"):
                print('aggregating data')
                return self.response_200


            else:
                raise Exception('filter is None or len(filter) < 1')
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404



    def __get_candlestick_patterns_analysis(self):
        def mapBullBearArrays(bull, bear):
            
            return [
                {
                    "ticker":bull['ticker'],
                    "bulls":bull['bulls'],
                    "bears":bull['bears'],
                    "name":bull['name']
                },
                {
                    "ticker":bear['ticker'],
                    "bulls":bear['bulls'],
                    "bears":bear['bears'],
                    "name":bear['name']
                    }
                ]



        try:
            filter=self.params.get('filter')

            if(filter == "top50"):
                
                collection = os.getenv("PATTERNS_ANALYSIS_COLLECTION")
                
                top_bulls_cursor = self.db[collection].find().sort("bulls", -1).limit(50)
                top_bears_cursor = self.db[collection].find().sort("bears", -1).limit(50)
            
                mergedArray = map(mapBullBearArrays, top_bulls_cursor, top_bears_cursor)
                results = list(mergedArray)
                
                last_updated = today.strftime("%d/%m/%Y %H:%M")
     

                return {
                    "status":200,
                    "results":results,
                    "last_update":last_updated
                }
                
            elif(filter == "one"):

                ticker=self.params.get('ticker')
                if(ticker is None or len(ticker) < 1):
                    raise Exception('ticker is None or len(ticker) < 1')

                collection = os.getenv("PATTERNS_ANALYSIS_COLLECTION")
                ticker_patterns_rating = self.db[collection].find_one({"ticker":ticker})
                
                if(ticker_patterns_rating is None):
                    raise Exception('ticker is None ')

                results = {
                    "bears":ticker_patterns_rating['bears'],
                    "bulls":ticker_patterns_rating['bulls']
                }

                return {
                    "status":200,
                    "results":results
                }

            else:
                raise Exception('filter is None or len(filter) < 1')

        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


