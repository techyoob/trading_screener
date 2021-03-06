
import logging
import platform
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta



class TaskScheduler:


    def __init__(self):
        print(" Initilizing Schedule dispatcher ")

 
    def getCurrentSchedule(self):
        print(" to read already scheduled tasks when needed  ")


    def set(self, task):
        script = task.get('script', "")
        time = task.get('time', "")
        folder = os.getenv("OS_TASK_SCHEDULER")
        name = task.get('name', "")
        date = task.get('date', "")
        run = task.get('run', "")
        frequency = task.get('frequency', "")
        frequencySize = task.get('frequency_size', "")

        if(frequency == "ONCE"):
            logging.warning(" Script %s has no schedule!" %script)
            return

        if platform.system() == 'Windows':

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


        if platform.system() == 'Linux':


            path=self.__getScriptPath(script)
            if(path==None):
                logging.warning(" Script %s was not found" %script)
                return


            from crontab import CronTab
            cron = CronTab(user='root')

            existingJobs = cron.find_comment(name)
            for job in existingJobs:
                cron.remove(job)

            commandStr='python3 %s' %path
            job = cron.new(command=commandStr, comment=name)

            if(frequency == "DAILY"):
                hour, minute = time.split(':')
                job.day.every(1)
                job.hour.on(hour)
                job.minute.on(minute)

            elif(frequency == "MINUTE"):
                job.minute.every(frequencySize)

            cron.write()
            print('Cron for %s was scheduled' %name)
         

         

    def __getOSTaskSchedule(self):
        print(" am here at __getOSTaskSchedule ")


    def __getScriptPath(self,filename):
        result = []
        searchPath='../'        
        absRootPath = os.path.abspath(searchPath)

        # Wlaking top-down from the root
        for root, dir, files in os.walk(searchPath):
            if filename in files:
                rPath=os.path.join(root, filename)
                result.append(absRootPath+rPath[2:])

        return result[0] if len(result) > 0 else None