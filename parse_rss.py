from lxml import etree
import sqlite3
import os.path

def parse_rss2(file_desc):
    tree = etree.parse(file_desc)
    root = tree.getroot()
    items = root.find("channel").findall("item")
    entries = []
    for i in items:
        title = i.find("title").text
        guid = i.find("guid").text
        link = i.find("link").text
        link_split = dict([tuple(i.split("=")) for i in link.split("&")])
        url = link_split["url"]
        entries.append({"title": title, "url": url, "guid": guid})
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
        tweeted boolean
    );
    """
    c.execute(schema)

def push_db(entries, db):
    conn = sqlite3.connect(db)
    for e in entries:
        c = conn.cursor()
        c.execute("SELECT COUNT(guid) FROM entries WHERE guid = ?", (e["guid"],))
        if c.fetchone() == (0,):
            values = (e["title"], e["url"], e["guid"], False)
            c.execute("INSERT INTO entries (title,url,guid,tweeted) values (?,?,?,?)", values)
    conn.commit()

def choose_tweet(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT title, url, id FROM entries WHERE tweeted = 0")
    tweet = c.fetchone()
    if tweet is not None:
        c.execute("UPDATE entries SET tweeted = 1 WHERE id = ?", tweet[2])
    return c.fetchone()
