import os
from datetime import datetime, date, timedelta
from tinydb import TinyDB, Query
sportscribe = __import__("sportscribe-python")
from sportscribe import SportScribe
from dotenv import load_dotenv


if not load_dotenv():
  print('cannot find .env file')
  exit()


# Setup TinyDB object
db = TinyDB(os.path.dirname(os.path.realpath(__file__)) + '/sportscribe.db.json')

# Get number of days to pull data from .env
try:
  pull_days = int(os.getenv('SPORTSCRIBE_PULL_DAYS'))
  pull_days = min(pull_days,10)
except e:
  pull_days = 3

# Setup SportScribe object
ss = SportScribe(os.getenv('SPORTSCRIBE_API_KEY'))
ss.setEndpoint(os.getenv('SPORTSCRIBE_ENDPOINT'))

# For each day in range, pull that day's match previews, and store in the fixtures table
for i in range(0,pull_days):

  pull_time = date.today() + timedelta(days=i)
  pull_date = pull_time.strftime('%Y-%m-%d')
  print('Pulling ', pull_date)
  result = ss.getMatchPreviewByDate(pull_date)

  if result:
    for r in result.data:
      try:
        id = r['fixture_id']
        Data = Query()
        if not db.search(Data.id == id):
          print("Inserting " , id)
          start = datetime.strptime(r['start_utc_timestamp'],'%Y-%m-%d %H:%M:%S')
          db.insert({'id':id,'posted':False,'start_time_utc':r['start_utc_timestamp'],'start_timestamp_utc':start.timestamp(),'data':r})
      except:
        print('Error, skipping')
  else:
    print('Error pulling ' , pull_date)

