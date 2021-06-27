

#commebts


import csv
import json
from pymongo import MongoClient
import datetime
import time
import os
from dotenv import load_dotenv
load_dotenv()

import logging

scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/ticker_list_populator.log' if len(scriptAbsPath) > 0 else 'ticker_list_populator.log'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' USA market ticker list populator has been started!')

mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")

filenames = ["nasdaqlisted.csv", "otherlisted.csv"]




def populate():
        try:

            client = MongoClient(mongoURL)
            db = client[dbName]
            tickers_collection = db['tickers_list']

            for filename in filenames:
                dataAbsPathFile=scriptAbsPath+'/'+filename if len(scriptAbsPath) > 0 else filename
                with open(dataAbsPathFile) as f:
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
                        #print(" ticker added with symbol ", row[0])
                        # logging.info( " Ticker with symbol %s was added ", row[0] )

        except Exception as e:
            print('reading file with error ', e)
            logging.error(' Error populating ticker list. Script is ending... ')





populate()

logging.info(' Ticker list populator finished!')