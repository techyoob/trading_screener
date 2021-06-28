import os

from crontab import CronTab
cron = CronTab(user='root')



job = cron.new(command="python3 ", comment='testy cron')
job.day.on(int(time))




python3 /home/techyoob/Documents/stock_workspace/big_bang_trading_screener/manager/reporter.py



def find_files(filename, search_path):
   result = []

# Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

print(find_files("alerts_processor.py","../"))