



from pymongo import MongoClient
from datetime import datetime
import time
import requests
import json
import logging

import os
from dotenv import load_dotenv
load_dotenv()



mongoURL = os.getenv("DB_URL")
dbName = os.getenv("DB_NAME")
social_coll = os.getenv("SOCIAL_TREND")

apiKey = os.getenv("SS_KEY")
ssURL = os.getenv("SS_URL")


headers = {
    'Authorization': 'Token '+apiKey,
    'Accept': 'application/json'
}



client = MongoClient(mongoURL)
db = client[dbName]
socialColl = db[social_coll]

import logging

scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/social_trend_processor.log' if len(scriptAbsPath) > 0 else 'social_trend_processor.log'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' Social Trends processor has been started!')

def populate_social_trends():
    try:
# TODO:
# + Read sentiment from multiple sources


        response = requests.request("GET", ssURL+"stocks/trending/twitter/", headers=headers)
        # response = requests.request("GET", ssURL+"stocks/trending/reddit/", headers=headers)

        if response.status_code == 200:
            socialTrendData = json.loads(response.content)

            if( len(socialTrendData) == 0 ):
                logging.warning('Empty api request returned!')

            for item in socialTrendData:
                itemResponse = requests.request("GET", ssURL+"stocks/"+item['stock']+"/sentiment/daily/", headers=headers)

                if itemResponse.status_code == 200:
                    tickerDailySentiments = json.loads(itemResponse.content)
                    accum=0
                    for sentiment in tickerDailySentiments:
                        accum=sentiment['activity']+accum
                    weekAverage = accum / len(tickerDailySentiments)
                    activityDayWeekRatio = item['activity'] / weekAverage
                    activityDayWeekRatioPercentage = activityDayWeekRatio * 100

                    sentimentDirection = "up" if item['score'] > item['avg_7_days'] else "down"

                    itemDocument =  {
                        "ticker":item['stock'],
                        "score":item['score'],
                        "date":item['date'],
                        "activity":item['activity'],
                        "direction":sentimentDirection,
                        "activity day-week":str(round(activityDayWeekRatioPercentage, 2))+"%"
                    }

                    socialColl.find_one_and_update({'ticker':item['stock']}, {'$set':itemDocument}, upsert=True)
                    logging.info(" Social trend for stock %s has been processed " %(item['stock']) )
                    #print(" Social trend for stock %s has been processed " %(item['stock']))
                else:
                    #print('!!!Cant fetch daily sentiment for ticker %s !!!' %(item['stock']))
                    logging.warning('Cant fetch daily sentiment for ticker %s ' %(item['stock']))


        else:
            raise Exception('!!!Cant fetch 3rd party api!!!')


        
    except Exception as e:
        # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
        # print('Error processing social trends ', e)
        logging.error(' Exception thrown - Error processing social trends ')

        



populate_social_trends()

logging.info(' Social Trends processor finished!')