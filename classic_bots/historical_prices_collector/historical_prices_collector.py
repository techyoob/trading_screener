# TODO:
#   + load tickers list 
#   + every loop through the list, load historical price for every ticker in threads
#   + 3 threads at a time
#


import csv
import json
from pymongo import MongoClient
import datetime
import time
import os
import requests
from queue import Queue
from threading import Thread

from dotenv import load_dotenv
load_dotenv()

import logging

scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/historical_prices_collector.log' if len(scriptAbsPath) > 0 else 'historical_prices_collector.log'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' history price collector has been started!')

mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")
tickersStr = os.getenv("TICKERS_COLLECTION")
historicalPriceStr = os.getenv("HISTORICAL_PRICE_COLLECTION")
fmgURL = os.getenv("FMG_URL")
fmgKEY = os.getenv("FMG_KEY")


client = MongoClient(mongoURL)
db = client[dbName]
tickers_collection = db[tickersStr]
historical_price_collection = db[historicalPriceStr]


class AlertProcessingWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        # while True:
            # Get the work from the queue and expand the tuple

        try:
            params= self.queue.get()
            stock = params.get('stock', "")
            ticker = stock.get('ticker', "")
            name = stock.get('name', "")

            tickerHistoryResponse = requests.get(fmgURL+"historical-price-full/"+ticker+"?apikey="+fmgKEY)            
            historicalArr = tickerHistoryResponse.json().get('historical', [])

            if(len(historicalArr)==0):
                logging.warning(' Emty history prices list has been fetched')
                return
            
            historicalDoc = {"ticker": ticker,
                        "name": name,
                        "historical":historicalArr,
                        "updated": datetime.datetime.utcnow()}

            historical_price_collection.find_one_and_update({'name': name, 'ticker':ticker}, {'$set':historicalDoc}, upsert=True)

        finally:
            self.queue.task_done()








def collect():
        try:
                            

            
            THREADS_POOL_SIDE = 4
            currentCursorPage=0
            stocksCount = tickers_collection.count_documents({})
            print('stocksCount is %s '  %stocksCount)

            skipSize = currentCursorPage * THREADS_POOL_SIDE
            stocksCurrentCursorPage = tickers_collection.find({}, {"_id":0, "name":1, "ticker":1}).limit(THREADS_POOL_SIDE).skip(skipSize)

            while( skipSize < stocksCount):
                print(' ################################ looping batch at page %s ' %currentCursorPage)

                stockTic = time.perf_counter()
                
                queue = Queue()
                for stock in stocksCurrentCursorPage:

                    params={
                        "stock":stock
                    }

                    worker = AlertProcessingWorker(queue)
                    worker.daemon = True
                    worker.start()
                    queue.put(params)

                queue.join()
                
                currentCursorPage=currentCursorPage+1
                skipSize = currentCursorPage * THREADS_POOL_SIDE

                stocksCurrentCursorPage = tickers_collection.find({}, {"_id":0, "name":1, "ticker":1}).limit(THREADS_POOL_SIDE).skip(skipSize)
                stockToc = time.perf_counter()
                print(f'Batch processed in {stockToc - stockTic:0.4f} seconds')



        
        except Exception as e:
            print('reading file with error ', e)
            logging.error(' Error populating ticker list. Script is ending... ')





processorTic = time.perf_counter()
collect()
processorToc = time.perf_counter()
logging.info(f' History prices collector finished in {processorToc - processorTic:0.4f} seconds!!')