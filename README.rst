sportscribe-twitter
==================

sportscribe-twitter -- Python application to post SportScribe content to twitter

v1.0.0

Installation
============

Clone this repo into your working directory

Clone https://github.com/sportscribe/sportscribe-python to the same directory

And install twitter-python and tinydb

.. code::

  pip install twitter
  pip install tinydb



You must get a twitter development account at https://developer.twitter.com 


And setup your .env file with the following variables

Twitter Keys:

.. code::

  TWITTER_CONSUMER_KEY=
  TWITTER_CONSUMER_SECRET=
  TWITTER_ACCESS_TOKEN_KEY=
  TWITTER_ACCESS_TOKEN_SECRET=
  
SportScribe API Key & Endpoint
  
.. code::

  SPORTSCRIBE_API_KEY=
  SPORTSCRIBE_ENDPOINT=https://api.sportscribe.co/v1_0/

Configuration Variables:

| Number of days in advance to pull API data to the database. 
| Optional. Default is 3. Maximum is 10

.. code::

  SPORTSCRIBE_PULL_DAYS=4

| Number of hours in advance of game start to post to Twitter. If a game starts at 13:00, a 6 hour POSTHOUR_DELTA will post to twitter at 07:00
| Optional. Default is 1. Maximum is 48

.. code::

SPORTSCRIBE_POSTHOUR_DELTA=6



Usage
=======

| sportscribe-twitter-poll.py should be run on a cron once a day. It pulls the API data from SportScribe and puts it in a database to be posted to twitter
| sportscribe-twitter.py should be run on a cron every hour. It polls the database and posts to twitter.





ChangeLog
=========

