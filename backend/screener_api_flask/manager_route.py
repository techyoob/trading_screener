


import talib
import pandas as pd
from pymongo import MongoClient
from io import StringIO
from datetime import date, datetime, timedelta
import time
import requests
import json
from bson.json_util import dumps

import os
from dotenv import load_dotenv
load_dotenv()



from os_schedule_dispatch import TaskScheduler

class ManagerRequest:


    response_404 = {
        "status":404,
        "results":[]
    }

    response_200 = {
        "status":200,
        "results":[]
    }









    def __init__(self, params):
        
        name = os.getenv("DB_NAME")
        url = os.getenv("DB_URL")


        self.fmgKey = os.getenv("FMG_KEY")
        self.fmgURL = os.getenv("FMG_URL")

        self.params=params
        self.dbClient=MongoClient(url)
        self.db=MongoClient(url)[name]


    def getRequest(self):
        query=self.params.get('query')


        if(query is None or len(query) < 1):
            return self.response_404

        if(query == "system overview"):
            return self.__get_system_overview()
        
        if(query == "something else"):
            return self.__get_something_else()

        return self.response_404






    def __get_system_overview(self):
        try:
            print("requesting system overview")

            scheduler = TaskScheduler()
            f = open ('../../manager/managerCfg.json', "r")
            config = json.loads(f.read())
            tasks = config.get('tasks', [])
            tasksOverview=[]
            for task in tasks:
                isTaskActive = scheduler.isTaskScheduled(task['name'])
                taskObj = {
                    "name":task['name'],
                    "isActive":isTaskActive,
                }
                tasksOverview.append(taskObj)

            f.close()
                   
            last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")
    

            return {
                "status":200,
                "results":tasksOverview,
                "last_updated":last_updated
            }
            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


    def __get_something_else(self):
        try:
            print(" requesting something else ")
       
            last_updated = datetime.now().strftime("%d-%m-%Y %H:%M")

            return {
                "status":200,
                "results":[],
                "last_updated":last_updated
            }

            
        except Exception as e:
            # print('Error processing ticker with ticker ', ticker , "  and reason is ", e)
            print('Error processing ticker with ticker ', e)
            return self.response_404


        