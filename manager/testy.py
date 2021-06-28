import os

from crontab import CronTab
cron = CronTab(user='root')



job = cron.new(command="python3 /home/techyoob/Documents/stock_workspace/big_bang_trading_screener/manager/reporter.py", comment='testy cron')
job.day.every(1)
job.hour.on(23)
job.minute.on(47)


cron.write()

print(' am done cron')


## python3 /home/techyoob/Documents/stock_workspace/big_bang_trading_screener/manager/reporter.py



def find_files(filename, search_path):
   result = []

# Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

# print(find_files("alerts_processor.py","../"))