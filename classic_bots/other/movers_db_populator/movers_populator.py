from pymongo import MongoClient
import yfinance as yf

import csv
import json
import datetime
import time









def run_populator():
    try:
        counter =0

        client = MongoClient('mongodb://localhost:27017/')
        db = client['shares_db']
        classified_movers_collection = db['classified_movers_list']
        tickersCount = classified_movers_collection.count_documents({})


        # TODO
        #  Find a library to serve movers list
        #  fetch list and save it in mongodb with collection name classified_movers_collection






    except Exception as e:
        print('Reading tickers list file with error ', e)













print('Start of Script')

#  Uncoment to populate list of tickers and save in database (NoSQL)
# initialTickersList()


# uncomment to populate data for each ticker in the list 
# run_populator()


#  uncomment to pupulate/update candle stick patterns
# candlePatternsListUpdater()


print('End of Script')



