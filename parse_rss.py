from lxml import etree
import sqlite3
from datetime import datetime


def parse_rss2(file_desc):
    tree = etree.parse(file_desc)
    root = tree.getroot()
    items = root.find("channel").findall("item")
    entries = []
    for i in items:
        url = i.find("link").text
        title = i.find("title").text
        guid = i.find("guid").text
        pub_date = i.find("pubDate").text
        try:
            dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            dt = None
        entries.append({"title": title, "url": url, "guid": guid, "pub_date": dt})
    return entries


def create_db(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    schema = """
    CREATE TABLE entries (
        id     integer primary key autoincrement not null,
        title  text,
        url    text,
        guid   text not null,
        tweeted boolean,
        pub_date timestamp
    );
    """
    c.execute(schema)


def push_db(entries, db):
    conn = sqlite3.connect(db)
    for e in entries:
        c = conn.cursor()
        c.execute("SELECT COUNT(guid) FROM entries WHERE guid = ?", (e["guid"],))
        if c.fetchone() == (0,):
            values = (e["title"], e["url"], e["guid"], False, e["pub_date"])
            c.execute("INSERT INTO entries (title,url,guid,tweeted,pub_date) values (?,?,?,?,?)", values)
    conn.commit()


def choose_tweet(db, mark=False):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT title, url, id FROM entries WHERE tweeted = 0 ORDER BY id DESC")
    tweet = c.fetchone()
    if mark and tweet is not None:
        c.execute("UPDATE entries SET tweeted = 1 WHERE id = ?", (tweet[2],))
        conn.commit()
    return tweet
