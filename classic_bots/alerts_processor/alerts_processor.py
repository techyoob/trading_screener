


import logging
from pymongo import MongoClient
from datetime import datetime
import time
import requests
import json
import pandas as pd

import os
from queue import Queue
from threading import Thread
from dotenv import load_dotenv
load_dotenv()


import logging
scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/alerts_processor.log' if len(scriptAbsPath)>0 else 'alerts_processor.log'
alertsModelsFile=scriptAbsPath+'/alerts.json' if len(scriptAbsPath)>0 else 'alerts.json'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' Alerts processor has been started!')



from alertThreads import AlertThreads
at = AlertThreads()


ssKey = os.getenv("SS_KEY")
ssURL = os.getenv("SS_URL")


fmgKey = os.getenv("FMG_KEY")
fmgURL = os.getenv("FMG_URL")

mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")
alertsCollectionName = os.getenv("ALERTS_COLL")
stocksCollectionName =  os.getenv("TICKERS_COLL")

db=MongoClient(mongoURL)[dbName]
alertsCollection=db[alertsCollectionName]
stocksCollection=db[stocksCollectionName]

alerts = json.load(open(alertsModelsFile,  "r"))



class AlertProcessingWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        # while True:
            # Get the work from the queue and expand the tuple
        params= self.queue.get()

        try:
            analyzeAlerts(params)
            # at.executeAlert(params)

        finally:
            self.queue.task_done()







def run_processor():
    try:

        
        BATCH_SIZE = 4
        currentCursorPage=0
        stocksCount = stocksCollection.count_documents({})
        print('stocksCount is %s '  %stocksCount)

        skipSize = currentCursorPage * BATCH_SIZE
        stocksCurrentCursorPage = stocksCollection.find({}, {"_id":0, "name":1, "ticker":1}).limit(BATCH_SIZE).skip(skipSize)

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
            skipSize = currentCursorPage * BATCH_SIZE

            stocksCurrentCursorPage = stocksCollection.find({}, {"_id":0, "name":1, "ticker":1}).limit(BATCH_SIZE).skip(skipSize)
            stockToc = time.perf_counter()
            print(f'Batch processed in {stockToc - stockTic:0.4f} seconds')

    except Exception as e:
        print('Error processing  alerts', e)
        logging.error(' Error processing Alerts')







def analyzeAlerts(params):
    try:

        stock = params['stock']
        tickerAlertsCursor = alertsCollection.find_one( {"ticker":stock['ticker']} )

        tickerHistoryResponse = requests.get(fmgURL+"historical-price-full/"+stock['ticker']+"?apikey="+fmgKey)
        historicalArr = tickerHistoryResponse.json().get('historical', [])

        if(len(historicalArr)>0):
            historicalDf = pd.DataFrame(historicalArr)
            params['historicalDf']=historicalDf


        tickerCurrentResponse = requests.get(fmgURL+"quote/"+stock['ticker']+"?apikey="+fmgKey)
        tickerCurrentJson = tickerCurrentResponse.json()
        params['tickerCurrentJson']=tickerCurrentJson





        for alert in alerts:            
            currentAlert={}
            if(tickerAlertsCursor == None):
                currentAlert = alert.get('current_alert', {}).copy()
            else:
                currentAlert=tickerAlertsCursor.get(alert['name'], alert['current_alert'])

            if(len(currentAlert)  < 1):
                break

            params['alert']=alert
            params['currentAlert']=currentAlert

            result = at.executeAlert(params)




        return {
            "status":"success",
            "error":""
        }


    except Exception as e:
        return {
            "status":"error",
            "error":e
        }





processorTic = time.perf_counter()
run_processor()
processorToc = time.perf_counter()
logging.info(f' Processor finished in {processorToc - processorTic:0.4f} seconds!')




