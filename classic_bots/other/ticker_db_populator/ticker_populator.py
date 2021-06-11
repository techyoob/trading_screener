







from pymongo import MongoClient
import yfinance as yf

import csv
import json
import datetime
import time
import patterns





def candlePatternsListUpdater():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['shares_db']
        patterns_collection = db['candle_patterns_list']
        
        print(patterns.candle_patterns)
        for key, value in patterns.candle_patterns.items():
            patternDoc = {
                "name":value,
                "talib_name":key
            }

            tickerid = patterns_collection.find_one_and_update({'name': value}, {'$set':patternDoc}, upsert=True)
            print(" ticker added with id ", tickerid)


    except Exception as e:
        print('reading file with error ', e)



def initialTickersList():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['shares_db']
        tickers_collection = db['tickers_list']

        with open('otherlisted.csv') as f:
            for row in csv.reader(f, delimiter='|'):
                if row[0]=="Symbol":
                    continue

                tickerName = row[1].split('-')
                ticker = {"symbol": row[0],
                        "name": tickerName[0].strip(),
                        "exchange": "other",
                        "note": tickerName[1].strip() if len(tickerName) > 1 else "",
                        "updated": datetime.datetime.utcnow()}

                tickers_collection.find_one_and_update({'name': row[1], 'symbol':row[0]}, {'$set':ticker}, upsert=True)
                print(" ticker added with symbol ", row[0])

    except Exception as e:
        print('reading file with error ', e)











def saveConfigFile(counter):
    with open('config.json', "w") as json_file:
        dataDict = { "counter": counter }
        json.dump(dataDict, json_file)


def loadConfigFile():
    with open('config.json') as json_file:
        data = json.load(json_file)
        return data['counter']




def run_populator():
    try:
        counter = loadConfigFile()

        client = MongoClient('mongodb://localhost:27017/')
        db = client['shares_db']
        tickers_collection = db['tickers_list']

        tickersCount = tickers_collection.count_documents({})
        # limitPerIterationsSet = (counter + 13602) % tickersCount

        # for i in range(counter, tickersCount):
        for i in range(counter, tickersCount):
            try:                
                ticker = tickers_collection.find()[i]
                symbol = ticker['symbol']

                tickerInfo = yf.Ticker(symbol)
                info = tickerInfo.info

            
                if 'symbol' not in info.keys():
                    info['symbol'] = symbol
                
                info['updated'] = datetime.datetime.utcnow()
                
                ticker_profile_collection = db['ticker_profile_collection']
                ticker_profile_collection.find_one_and_update({'shortName': info['shortName']}, {'$set':info}, upsert=True)
                
                time.sleep(2)
                history = tickerInfo.history(period="max")
                dailyHistoryCSV = history.to_csv()

                ticker_history_doc = {
                    "shortName":info['shortName'],
                    "symbol":symbol,
                    "daily":dailyHistoryCSV,
                    "hourly":"",
                    "updated":datetime.datetime.utcnow()
                }
                
                ticker_history_collection = db['ticker_history_collection']
                ticker_history_collection.find_one_and_update({'shortName': ticker_history_doc['shortName']}, {'$set':ticker_history_doc}, upsert=True)
                print(" Ticker was added with symbol   ", symbol )

            except Exception as e:
                # print('Error processing ticker with symbol ', symbol , "  and reason is ", e)
                print('Error processing ticker with symbol ', symbol, " error ", e )


            saveConfigFile(i+1)
            time.sleep(2)



    except Exception as e:
        print('Reading tickers list file with error ', e)













print('Start of Script')

#  Uncoment to populate list of tickers and save in database (NoSQL)
# initialTickersList()


# uncomment to populate data for each ticker in the list 
run_populator()


#  uncomment to pupulate/update candle stick patterns
# candlePatternsListUpdater()


print('End of Script')



