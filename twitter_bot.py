from bot_secrets import *
import urllib2
from parse_rss import *
import os.path
import tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

feed = "http://news.google.de/news/feeds?pz=1&cf=all&ned=pt_BR&hl=br&q=%22vira+meme%22&output=rss"
feed_db = "feed.db"

def tweet():
    rss = urllib2.urlopen(feed)
    entries = parse_rss2(rss)
    push_db(entries, feed_db)
    tco_length = api.configuration()[u'short_url_length']
    tweet = choose_tweet(feed_db)
    if tweet is not None:
        text = tweet[0][0:140-tco_length-1]
        api.update_status(text+" "+tweet[1])
        return text

if __name__ == "__main__":
    if os.path.isfile(feed_db) == False:
        create_db(feed_db)
    print tweet()
