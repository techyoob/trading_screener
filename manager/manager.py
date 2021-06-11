

from os_schedule_dispatch import TaskScheduler


import subprocess
import json
import os
from dotenv import load_dotenv
load_dotenv()





# TODO:
#   + the manager keeps data up to date
#   + it manages bots and tasks to successfully update database and report big bang system behavior
#   + it dispatches some BOTs to windows/linux scheduler
#   + it runs BOTs to be executed once
#   + it reports big bang system behavior in object file (e.g json file wioth variables to track system behavior)
#   + it reads a json file that has the parameters to use for managing big bang system
#   + it saves the managing status in json file 
#   





# TODO:
# STEP I:
#   -   set os scheduling
#   -   report the STEP I status


def initializeBigBang():


    # TODO:
    # read managerCfg.json
    # 
    # loop through tasks list and dispatch every task to os task scheduler


    
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

# TODO:
# STEP II:
#   -   Run other non OS task scheduler dependent scripts, 
#   -   each script has an execution frequency configured from json file (e.g every min, every 5 min, ...etc, no longer than one hour)
#   -   Every bot/script has its own log file
#   -   
#


def execBatFile(config):
    print("running bat file ")














initializeBigBang()