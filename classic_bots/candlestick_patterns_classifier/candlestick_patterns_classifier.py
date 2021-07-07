

import sys
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



import logging

scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/candlestick_patterns_classifier.log' if len(scriptAbsPath) > 0 else 'candlestick_patterns_classifier.log'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' Candlestick patterns classifier has been started!')

mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")
client = MongoClient(mongoURL)
db = client[dbName]

tickersStr = os.getenv("TICKERS_COLLECTION")
historicalPriceStr = os.getenv("HISTORICAL_PRICE_COLLECTION")
fmgURL = os.getenv("FMG_URL")
fmgKEY = os.getenv("FMG_KEY")

tickers_collection = db[tickersStr]
historical_price_collection = db[historicalPriceStr]

tickers_list_collection = db['tickers_list']
patterns_collection = db['candle_patterns']






def processCandlePatternsAnalysis(item, tickerHistoryArr):
    try:
        df = pd.DataFrame(tickerHistoryArr[::-1])

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
                logging.warning(' Exception thrown processing pattern %s ' %pattern)
                # print('Error at : ')
        

        
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
            
        
        for key, value in patterns.candle_patterns.items():
            patternDoc = {
                "name":value,
                "talib_name":key
            }

            patterns_collection.find_one_and_update({'name': value}, {'$set':patternDoc}, upsert=True)
            print('Pattern %s code was added!' %value)


    except Exception as e:
        # print('Exception thrown reading patterns csv file  ', e)
        logging.error(' Exception thrown reading patterns csv file')






def run(loadPatterns):

    if loadPatterns:
        generatePatterns()

    for item in tickers_list_collection.find():
        historicalCursor = historical_price_collection.find_one({'ticker':item['ticker']},{"_id":0, "historical":1,})
        historicalArr=[]

        if historicalCursor == None:
            tickerHistoryResponse = requests.get(fmgURL+"historical-price-full/"+item['ticker']+"?apikey="+fmgKey)
            historicalArr = tickerHistoryResponse.json().get('historical', [])

        else:
            historicalArr = historicalCursor.get("historical", [])
            

        if(len(historicalArr)==0):
            logging.warning(" Cannot get historical pricese for %s " %item['ticker'])
            continue

        result = processCandlePatternsAnalysis(item, historicalArr)
        if(result['status'] != "success"):
            logging.warning('Failed to process candlestick patterns for %s' %item['ticker'])
            





if __name__ == "__main__":
    
    loadPatterns = False
    if sys.argv[1:]:
        loadPatterns = True if sys.argv[1] == 'patterns' else False
       


    processorTic = time.perf_counter()
    run(loadPatterns)
    processorToc = time.perf_counter()
    logging.info(f' Candlestick patterns classifier finished in {processorToc - processorTic:0.4f} seconds!!')
    