import json
import sqlite3

with open("data.json", "r") as file:
    data = json.loads(file.read())

with sqlite3.connect("./database.db") as con:
    cur = con.cursor()
    try:
        cur.execute("""
            CREATE TABLE entry (
               	id INTEGER NOT NULL,
               	title VARCHAR NOT NULL,
               	body VARCHAR NOT NULL,
               	iso_time VARCHAR NOT NULL,
               	lat FLOAT,
               	lon FLOAT,
               	PRIMARY KEY (id)
            )
            """)
    except:
        pass

    cur.executemany("INSERT INTO entry VALUES(:id, :title, :body, :isoTime, :lat, :lon)", data)
