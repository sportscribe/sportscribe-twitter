import logging
import twitter, os
from datetime import datetime, date, timedelta
import time
from tinydb import TinyDB, Query
sportscribe = __import__("sportscribe-python")
from sportscribe import SportScribe
from dotenv import load_dotenv

def postSportScribe(d : {}):

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

  # If we have twitter handles for both teams
  if vt_twitter and ht_twitter:
    intro = ht_name + ' ' + ht_twitter  +  ' hosts ' + vt_name + ' ' + vt_twitter
  # If we dont have twitter handles,  and we have pro account
  elif 'parts' in d:
    intro = d['parts']['intro']
  # Else just use the names
  else:
    intro = ht_name +  ' hosts ' + vt_twitter

  #######################################################################################################
  #
  # Build the message string
  # Be sure not to let the msg get larger than the 280 twtter limit
  # Make sure click_url is short. When hashtags are used, you dont have a lot of space to work with
  #
  #######################################################################################################


  click_url = 'SportScribe.co'
  msg = intro + '\n\n' + 'Automatically post match previews and data to your twitter feed. Learn how at ' + click_url


  ########################################################################################################
  ## END 
  ########################################################################################################


  # If we have hashtag data on this match or teams, post them after the message
  other_twitter = set(other_twitter)
  if len(other_twitter) > 0 or 'match' in social:
    msg = msg + '\n\n\n'
    if 'match' in social:
      match_social = social['match']
      for ms in match_social:
        if 'platform' in ms and ms['platform'] == 'TWTR':
          msg = msg + ms['tag'] + ' '

    for t in other_twitter:
      msg = msg + t + ' '


  # Post the final message
  fixture = d['fixture_id']
  try:
    api.PostUpdate(msg,media=media)
    logger.info('Fixture {}:\tSuccessfuly Posted'.format(fixture))
    return True
  except Exception as e:
    print("ERROR POSTING TO TWITTER")
    logger.error('Fixture {}:\t{}'.format(fixture,e))
    return False


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


if os.getenv('LEAGUES'):
  LEAGUES = list(os.getenv('LEAGUES').replace(' ','').split(','))
else:
  LEAGUES = []


if os.getenv('LOGFILE'):
  logfile = os.getenv('LOGFILE')
else:
  logfile = os.path.dirname(os.path.realpath(__file__)) + '/sportscribe-twitter.log'


# Set Up Logging
logger = logging.getLogger('sportscribe-twitter')
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

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
    if (start - datetime.now()) < timedelta(hours=post_delta):
      print(d['data']['league_id'])
      if len(LEAGUES) == 0 or str(d['data']['league_id']) in LEAGUES:
        print("POSTING")
        if postSportScribe(d['data']):
          db.remove(Query().id == id)

  if start <= datetime.now():
    print('Removing ' , id , ' from db')
    db.remove(Query().id == id)


