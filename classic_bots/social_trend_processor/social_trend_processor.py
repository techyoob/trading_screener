



from pymongo import MongoClient
from datetime import datetime
import time
import requests
import json

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



def populate_social_trends():
    try:
# TODO:
# + Read social trend API and save data into a big bang model collection
# 	document model {
#		"ticker":"",
#		"name":"",
#		"score":"",
#		"direction":"",
#		"average day/week":"",
#		"last_updated":""
# 	}
#
#
# + Read sentiment from multiple sources

        response = requests.request("GET", ssURL+"stocks/trending/twitter/", headers=headers)
        # response = requests.request("GET", ssURL+"stocks/trending/reddit/", headers=headers)

        if response.status_code == 200:
            socialTrendData = json.loads(response.content)

            if( len(socialTrendData) == 0 ):
                print(" Empty Array from API!!! ")

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
                    print(" Social trend for stock %s has been processed " %(item['stock']))
                else:
                    print('!!!Cant fetch daily sentiment for ticker %s !!!' %(item['stock']))
                    saveReport('!!!Cant fetch daily sentiment for ticker %s !!!' %(item['stock']))
                    # raise Exception('!!!Cant fetch daily sentiment for ticker %s !!!' %(item['stock']))
                    # report erro and continue to nenxt ticker item

        else:
            raise Exception('!!!Cant fetch 3rd party api!!!')


        
    except Exception as e:
        # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
        print('Error processing social trends ', e)
        saveReport('Error processing social trends ')
        






def saveReport(report):
    reportDate = datetime.datetime.now()
    logReport = '%s  - %s \n' %(reportDate, report)
    file_object = open('social_trend_processor.log', 'a')
    file_object.write(logReport)
    file_object.close()


populate_social_trends()