import twitter, os
from datetime import datetime, date, timedelta
import time
from tinydb import TinyDB, Query
sportscribe = __import__("sportscribe-python")
from sportscribe import SportScribe
from dotenv import load_dotenv


# Only post leagues which appear in the leagues list
# or set LEAGUES = [] to do them all
LEAGUES = [ 21, 23, 30, 39, 42, 47 , 37, 24, 22 , 21, 17]


def postSportScribe(d : {}):

  click_url = 'SportScribe.co'

  if d['match_img']:
    media = d['match_img'];
  else:
    media = None

  other_twitter = []

  social = d['social']
  ht_id = d['hometeam_id']
  ht_name = d['hometeam_name']
  ht_social = social[str(ht_id)]
  ht_twitter = None
  for s in ht_social:
    if s['platform'] == 'TWTR':
      ht_twitter = s['tag']
    elif s['platform'] == 'TWTR_OTHER':
      other_twitter.append(s['tag'])

  vt_id = d['visitorteam_id']
  vt_name = d['visitorteam_name']
  vt_social = social[str(vt_id)]
  vt_twitter = None
  for s in vt_social:
    if s['platform'] == 'TWTR':
      vt_twitter = s['tag']
    elif s['platform'] == 'TWTR_OTHER':
      other_twitter.append(s['tag'])

  if vt_twitter and ht_twitter:
    intro = ht_name + ' ' + ht_twitter  +  ' hosts ' + vt_name + ' ' + vt_twitter
  else:
    intro = d['parts']['intro']


  msg = intro + '\n\n' + 'Automatically post match previews and data to your twitter feed. Learn how at ' + click_url

  other_twitter = set(other_twitter)
  if len(other_twitter) > 0 or 'match' in social:
    msg = msg + '\n\n\n'
    if 'match' in social:
      match_social = social['match']
      for ms in match_social:
        if 'platform' in ms and ms['platform'] == 'TWTR':
          msg = msg + ms['tag']

    for t in other_twitter:
      msg = msg + t + ' '



  api.PostUpdate(msg,media=media)

###################################################################
##
##
## START MAIN PROGRAM
##
##
###################################################################

if not load_dotenv():
  print('cannot find .env file')
  exit()


# Setup TinyDB object
db = TinyDB(os.path.dirname(os.path.realpath(__file__)) + '/sportscribe.db.json')

# Setup twitter API object
api = twitter.Api(consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
                  consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
                  access_token_key=os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
                  access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
		  )



# Get number of hours before match to post to twitter
# Maximum of 48 hours
# Default 1
try:
  post_delta = int(os.getenv('SPORTSCRIBE_POSTHOUR_DELTA'))
  post_delta = min(post_delta,48)
except e:
  post_delta = 1



# For each day in range, pull that day's match previews from the tinyDB
# Post to twitter if the difference between start time and now is less than 'post_delta' hours
# Remove from the tinyDB when the game start time has passed
for d in db:

  start = datetime.fromtimestamp(d['start_timestamp_utc'])
  id = d['id']
  if not d['posted']:
    if start - datetime.now() < timedelta(hours=post_delta):
      print(d['data']['league_id'])
      if len(LEAGUES) == 0 or int(d['data']['league_id']) in LEAGUES:
        print("POSTING")
        postSportScribe(d['data'])
        db.update({'posted':True},Query().id == id)

  if start <= datetime.now():
    print('Removing ' , id , ' from db')
    db.remove(Query().id == id)


