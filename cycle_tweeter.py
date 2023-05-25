#!/usr/bin/env python

# nohup python3 cycle_tweeter.py &
# ps ax | grep cycle_tweeter.py

from collections import defaultdict
from typing import Generator, Iterable
from multiprocessing import current_process
from dotenv import load_dotenv
from api import API
from twitter_media import TwitterMedia

import logging
import time
import os
import schedule
import tweepy

from requests_oauthlib import OAuth1

def job():
    try:
        LOGGER.info("Calling API")
        day_in, day_out = API.get_yesterday(os.environ["VIVACITY_KEY"])
        LOGGER.info("Called API. Yesterday totals are {} and {}".format(day_in, day_out))

        os.system("chromium --headless --disable-gpu --screenshot ./index.html --force-device-scale-factor=2 --window-size=1060,590")

        time.sleep(10)

        post_on_twitter(day_in, day_out)

    except Exception as e:

        LOGGER.error(str(e))


def post_on_twitter(day_in, day_out):

    FILENAME = 'screenshot.png'
    MEDIA_CATEGORY = 'tweet_image'

    twitterMedia = TwitterMedia(FILENAME, MEDIA_CATEGORY,oauth)
    twitterMedia.upload_init()
    twitterMedia.upload_append()
    twitterMedia.upload_finalize()

    tweet = "Yesterday, more than {} people were cycling on the ~A38Cycleway. {} headed into the city, {} headed towards Selly Oak.".format(day_in + day_out,day_in,day_out)

    response = client.create_tweet(text=tweet, media_ids=[twitterMedia.media_id])


if __name__ == '__main__':

    ### Set up logging
    # Create logger with 'spam_application'
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    
    # create file handler which logs even debug messages
    fh = logging.FileHandler('cycle_tweet.log')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    LOGGER.addHandler(fh)
    LOGGER.info('Starting Bot. PID: {}'.format(current_process().pid))

    # Load .env file with api keys
    load_dotenv(override=True)

    # Set up OAuth and Tweepy Client for tweeting
    client = tweepy.Client(
        consumer_key=os.environ["CONSUMER_KEY"], consumer_secret=os.environ["CONSUMER_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"], access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
    )

    oauth = OAuth1(os.environ["CONSUMER_KEY"],
                   client_secret=os.environ["CONSUMER_SECRET"],
                   resource_owner_key=os.environ["ACCESS_TOKEN"],
                   resource_owner_secret=os.environ["ACCESS_TOKEN_SECRET"])
    

    job()

    # # Schedule the job to run once an hour
    # schedule.every().hour.at(":01").do(job)

    # # Loop to run job
    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)
