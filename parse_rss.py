from lxml import etree
import sqlite3
import os.path

def parse_rss2(file_desc):
    tree = etree.parse(file_desc)
    root = tree.getroot()
    items = root.find("channel").findall("item")
    entries = [{"title": i.find("title").text,
                "url": i.find("link").text,
                "guid": i.find("guid").text} for i in items]
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
    c.execute("SELECT title, url FROM entries WHERE tweeted = 0")
    return c.fetchone()
