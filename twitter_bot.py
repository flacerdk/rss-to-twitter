from config import *
import urllib2
from parse_rss import *
import os.path
import tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def update_db(feed, db):
    rss = urllib2.urlopen(feed)
    entries = parse_rss2(rss)
    push_db(entries, db)


def tweet(feed, db):
    tco_length = api.configuration()[u'short_url_length']
    tweet = choose_tweet(db)
    if tweet is not None:
        text = tweet[0][0:140-tco_length-1]
        api.update_status(text+" "+tweet[1])
    return tweet

if __name__ == "__main__":
    if os.path.isfile(FEED_DB) == False:
        create_db(FEED_DB)
    update_db(FEED_URL, FEED_DB)
    if TWEET:
        print tweet(FEED_URL, FEED_DB)
