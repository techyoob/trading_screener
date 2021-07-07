

import manager
import sys
import time
import os
import logging


scriptAbsPath=os.path.dirname(__file__)
reportFile=scriptAbsPath+'/screener_report.log' if len(scriptAbsPath) > 0 else 'screener_report.log'

logging.basicConfig(filename=reportFile, format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info(' Reporter has been started!')





def run(isNew):
    manager.run(isNew)






if __name__ == "__main__":
    
    isNew = False
    if sys.argv[1:]:
        isNew = True if sys.argv[1] == 'new' else False



    logging.info(f' Manager has started!')
    processorTic = time.perf_counter()
    run(isNew)
    processorToc = time.perf_counter()
    logging.info(f' Manager finished in {processorToc - processorTic:0.4f} seconds!!')
    