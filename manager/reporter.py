


import time
import logging
import os


scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/screener_report.log' if len(scriptAbsPath) > 0 else 'screener_report.log'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' Reporter has been started!')



def run():
    #print(" Reporter is processing....")
    logging.info(" Am logging for every minute")
    print(' reporter os rruning ')
    



#TODO:
# write pseudocode to:
# + Read every bot's log file 
# + Notify admin about abnormalities
# + Read every file and sub-file within screener project folder
# + 






run()