
import os
from pymongo import MongoClient
import talib
import pandas as pd
from io import StringIO
import datetime
import time
import requests


import patterns

from dotenv import load_dotenv
load_dotenv()



apiKey = os.getenv("FMG_KEY")
url = os.getenv("FMG_URL")


client = MongoClient('mongodb://localhost:27017/')
db = client['big_bang']


tickers_list_collection = db['tickers_list']
patterns_collection = db['candle_patterns']









def processCandlePatternsAnalysis(item, tickerHistory):
    try:

        df = pd.DataFrame(tickerHistory['historical'][::-1])

        patterns_analysis_collection = db['candlestick_patterns_analysis_list']

        patternsCount = patterns_collection.count_documents({})

        bullsCount=0
        bearsCount=0
        for pattern in patterns_collection.find():
            pattern_function = getattr(talib, pattern['talib_name'])
            
            try:
                results = pattern_function(df['open'], df['high'], df['low'], df['close'])
                last = results.tail(1).values[0]
                
                if last > 0:
                    bullsCount += 1
                elif last < 0:
                    bearsCount += 1

            except Exception as e:
                print('Error at : ')
        

        
        analysisDoc = {
                "name":item['name'],
                "ticker":item['ticker'],
                "bullish":(bullsCount / patternsCount) * 100,
                "bearish":(bearsCount / patternsCount) * 100,
                "bulls":bullsCount,
                "bears":bearsCount,
                "updated":datetime.datetime.utcnow()

        }        

        patterns_analysis_collection.find_one_and_update({'name': analysisDoc['name']}, {'$set':analysisDoc}, upsert=True)

        print('Candlestick patterns for stock %s have been processed!' %(item['ticker']))

        return {
            "status":"success",
            "error":""
        }


    except Exception as e:
        # print('Error processing ticker with symbol ', symbol , "  and reason is ", e)
        return {
            "status":"error",
            "error":e
        }







def generatePatterns():
    try:
            
        print('Generating Patterns...')
        
        for key, value in patterns.candle_patterns.items():
            patternDoc = {
                "name":value,
                "talib_name":key
            }

            patterns_collection.find_one_and_update({'name': value}, {'$set':patternDoc}, upsert=True)
            


    except Exception as e:
        print('reading file with error ', e)








print("Classifier started...")


# generatePatterns()

for item in tickers_list_collection.find():
    tickerHistoryResponse = requests.get(url+"historical-price-full/"+item['ticker']+"?apikey="+apiKey)    
    result = processCandlePatternsAnalysis(item, tickerHistoryResponse.json())
    if(result['status'] != "success"):
        errorDate = datetime.datetime.now()
        report = '%s  -  error processing ticker candle patterns analysis for  %s \n' %(errorDate, item['ticker'])
        file_object = open('candlestick_patterns_classifier.log', 'a')
        file_object.write(report)
        file_object.close()




