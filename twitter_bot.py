from config import *
from urllib.request import urlopen
from parse_rss import *
import sys
import os.path
import tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def update_db(feed, db):
    rss = urlopen(feed)
    entries = parse_rss2(rss)
    push_db(entries, db)


def tweet(feed, db):
    tco_length = api.configuration()[u'short_url_length']
    tweet = choose_tweet(db, mark=True)
    if tweet is not None:
        text = tweet[0][0:140-tco_length-1]
        api.update_status(text+" "+tweet[1])
    return tweet

if __name__ == "__main__":
    feed_db = os.path.dirname(os.path.realpath(sys.argv[0]))+'/'+FEED_DB
    if os.path.isfile(feed_db) == False:
        create_db(feed_db)
    update_db(FEED_URL, feed_db)
    if TWEET:
        print(tweet(FEED_URL, feed_db))
    else:
        print(choose_tweet(feed_db))
