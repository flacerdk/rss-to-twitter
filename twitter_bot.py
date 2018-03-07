import os.path
import sys
from urllib.request import urlopen

import tweepy

try:
    import config
except ModuleNotFoundError:
    print(
        '''
You need a config.py file.

Copy config_template.py to config.py and add your credentials.
        ''',
    )
    sys.exit(1)
import parse_rss


def setup_api():
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
    return tweepy.API(auth)


def update_db(feed, db):
    rss = urlopen(feed)
    entries = parse_rss.parse_rss2(rss)
    parse_rss.push_db(entries, db)


def tweet(api, feed, db):
    tco_length = api.configuration()[u'short_url_length']
    tweet = parse_rss.choose_tweet(db, mark=True)
    if tweet is not None:
        text = tweet[0][0:280-tco_length-1]
        api.update_status(text+" "+tweet[1])
    return tweet


if __name__ == "__main__":
    feed_db = '{}/{}'.format(os.path.dirname(os.path.realpath(sys.argv[0])), config.FEED_DB)
    if not os.path.isfile(feed_db):
        parse_rss.create_db(feed_db)
    update_db(config.FEED_URL, feed_db)
    api = setup_api()
    if config.TWEET:
        print(tweet(api, config.FEED_URL, feed_db))
    else:
        print(parse_rss.choose_tweet(feed_db))
