

from os_schedule_dispatch import TaskScheduler


import subprocess
import json
import os
from dotenv import load_dotenv
load_dotenv()





def initializeScreener():

    
    scheduler = TaskScheduler()
    f = open ('managerCfg.json', "r")
    config = json.loads(f.read())
    tasks = config.get('tasks', [])
    for task in tasks:
        scheduler.set(task)

    
    print("Screener has been initialized!")




def execBatFile(config):
    print("running bat file ")














# initializeBigBang()