



import logging
import subprocess
import json
import os
import subprocess


from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
from os_schedule_dispatch import TaskScheduler
from os_service_dispatch import ServiceCreator



def run(isNew):

    #TODO:
    # + Check pre-requisit
    # + load configuration file 
    # + if system is new, populate first time data by running all tasks immediatly
    # + schdeule Tasks
    #       - Remove old schedule 
    #       - Create new schedule
    #
    # + Run Tasks
    #       - Stop if running
    #       - Re-create service
    #       - Start new service
    



    # Check pre-requisit
    results = checkPrerequisites()
    if not results['status']:
        print(' System requirements is missing - %s ' %results)
        return

    tasks, services = loadConfigs()

    if isNew:
        # commandStr = f'python3  {tasks[5]["rpath"]}{tasks[5]["script"]}'            
        # ret = os.system(commandStr)

        for task in tasks:            
            # run and wait for task at every loop
            commandStr = f'python3  {task["rpath"]}{task["script"]}'
            print(" Executing %s ..." %task['script'])
            ret = os.system(commandStr)
            if(ret != 0 ):
                print(" command wasnt executed ")
                logging.warning('Task cannot execute')



    scheduler = TaskScheduler()
    for task in tasks:
        scheduler.set(task)


    serviceHandler = ServiceCreator()
    for service in services:
        serviceHandler.set(service)





def loadConfigs():
    tasks=[]
    services=[]

    try:
        with open('managerCfg.json', "r") as configFile:
            config = json.loads(configFile.read())
            tasks = config.get('tasks', [])
            services = config.get('services', [])

        return (tasks, services)

    except:
        return (tasks, services)






def checkPrerequisites():
    #TODO:
    # + Check database server is running and connectableeeeeeeeeeeeee
    # + return 

    results={
        "status":True,
        "details":""
    }
    print(" Checking pre-requisites...")
    
    #
    # Check if mongodb server available 
    #

    try:
        mongoURL = os.getenv("DB_URL")
        client = MongoClient(mongoURL)
        info = client.server_info()
        results['status'] = True if info['ok'] == 1.0 else False

    except:
        results["status"]=False
        results["details"]="Database connection error"
        return results





    return results





def execBatFile(config):
    print("running bat file ")














# initializeBigBang()