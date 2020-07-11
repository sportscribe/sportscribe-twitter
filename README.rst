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

.. code::

  TWITTER_CONSUMER_KEY=
  TWITTER_CONSUMER_SECRET=
  TWITTER_ACCESS_TOKEN_KEY=
  TWITTER_ACCESS_TOKEN_SECRET=
  SPORTSCRIBE_API_KEY=
  SPORTSCRIBE_ENDPOINT=https://api.sportscribe.co/v1_0/


Usage
=======

sportscribe-twitter-poll.py should be run on a cron once a day. It pulls the API data from SportScribe and puts it in a database to be posted to twitter
sportscribe-twitter.py should be run on a cron every hour. It polls the database and posts to twitter.





ChangeLog
=========

