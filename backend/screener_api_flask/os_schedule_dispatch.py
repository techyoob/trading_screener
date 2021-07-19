
import platform
import subprocess
import os
import pandas as pd
import csv
from io import StringIO

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta



class TaskScheduler:

    currentSchedule = pd.DataFrame()

    def __init__(self):
        print(" Initilizing Schedule dispatcher ")
        self.getCurrentSchedule()

 
    def getCurrentSchedule(self):
        if platform.system() == 'Windows':
            command = ['schtasks.exe','/query','/TN', 'BigBang\\', '/fo', 'CSV']
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout_value = proc.stdout.read()
            self.currentSchedule = pd.read_csv(StringIO(stdout_value.decode()))




    def isTaskScheduled(self, name):
        print('check task if active')
        taskName = 'BigBang\%s' %name

        if(((self.currentSchedule['TaskName'] == taskName) & (self.currentSchedule['Status'] == 'Ready')).any()):
            return True

        return False



    def set(self, task):
        if platform.system() == 'Windows':
            
            time = task.get('time', "")
            folder = os.getenv("OS_TASK_SCHEDULER")
            name = task.get('name', "")
            date = task.get('date', "")
            run = task.get('run', "")
            frequency = task.get('frequency', "")
            frequencySize = task.get('frequency_size', "")
            

            # taskParam = "/create" if time!="now" else "/run "
            taskName = '/tn "%s\%s" ' %(folder, name)
            taskRun = '/tr %s' %run
            schedulType = '/sc %s ' %frequency
            modifier = "/mo %s" %frequencySize if len(frequencySize) > 0 else ""
            
            d = datetime.today() - timedelta(hours=0, minutes=5)
            taskTime= '/st %s ' %time if time!="now" else "/st %s " %d.strftime('%H:%M')
            taskDate = "/sd %s" %date if len(date) > 0 else ""

            
            command = 'SCHTASKS /create %s %s %s %s %s %s /F'  % (taskName, taskRun, schedulType, modifier, taskTime, taskDate)
            subprocess.call(command)

            if(time=="now"):
                command = 'SCHTASKS /run %s'  % (taskName)
                subprocess.call(command)




    def __getOSTaskSchedule(self):
        print(" am here at __getOSTaskSchedule ")




