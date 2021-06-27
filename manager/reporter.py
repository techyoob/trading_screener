


import time
import logging
import os

reportPath=os.path.dirname(__file__)


logging.basicConfig(filename=reportPath+'/screener_report.log', format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' Reporter has been started!')



def run():
    #print(" Reporter is processing....")
    logging.info(" Am logging for every minute")
    logging.warning(" ops am running forever every 1 minute")
    print(' reporter os rruning ')
    



#TODO:
# write pseudocode to:
# + Read every bot's log file 
# + Notify admin about abnormalities
# + Read every file and sub-file within screener project folder
# + 






run()