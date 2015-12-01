from lxml import etree
import sqlite3

def parse_rss2(handle):
    with open(handle,"rb") as f:
        tree = etree.parse(f)
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
        guid   text not null
    );
    """
    c.execute(schema)

def push_db(entries, db):
    conn = sqlite3.connect(db)
    for e in entries:
        c = conn.cursor()
        c.execute("SELECT COUNT(guid) FROM entries WHERE guid = ?", (e["guid"],))
        if c.fetchone() == (0,):
            c.execute("INSERT INTO entries (title,url,guid) values (?,?,?)",
                      (e["title"], e["url"], e["guid"]))
    conn.commit()
