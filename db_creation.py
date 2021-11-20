import sqlite3
conn = sqlite3.connect("thehackernews.db")

c = conn.cursor()

c.execute(""" CREATE TABLE posts (
    id INTEGER,
    header TEXT,
    link TEXT,
    date BLOB)""")

conn.commit()
conn.close()
