

#commebts


import csv
import json
from pymongo import MongoClient
import datetime
import time
import os
from dotenv import load_dotenv
load_dotenv()


mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")

filenames = ["nasdaqlisted.csv", "otherlisted.csv"]


def populate():
        try:
            print('Populating Big Bang Ticker List...')
            client = MongoClient(mongoURL)
            db = client[dbName]
            tickers_collection = db['tickers_list']

            for filename in filenames:
                with open(filename) as f:
                    for row in csv.reader(f, delimiter='|'):
                        if row[0]=="Symbol":
                            continue

                        tickerName = row[1].split('-')
                        ticker = {"ticker": row[0],
                                "name": tickerName[0].strip(),
                                "exchange": "other",
                                "note": tickerName[1].strip() if len(tickerName) > 1 else "",
                                "list_category":[],
                                "updated": datetime.datetime.utcnow()}

                        tickers_collection.find_one_and_update({'name': row[1], 'ticker':row[0]}, {'$set':ticker}, upsert=True)
                        print(" ticker added with symbol ", row[0])

        except Exception as e:
            print('reading file with error ', e)





populate()