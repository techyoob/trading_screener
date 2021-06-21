

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

    
    # startups = config.get('startups', [])
    # for startup in startups:
    #     #TODO
    #     # - run every startup in the array


    #     p = subprocess.run(["D:\\screener_project\\frontend\\big_bang_screener_ui_react\\run.bat"],  creationflags=subprocess.CREATE_NEW_CONSOLE)
    #     # subprocess.call(r'start D:\screener_project\frontend\big_bang_screener_ui_react\run.bat',creationflags=subprocess.CREATE_NEW_CONSOLE,  shell=True)
    #     print(startup)



    print("end of initializeBigBang")




def execBatFile(config):
    print("running bat file ")














# initializeBigBang()