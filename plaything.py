
from pathlib import Path
import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect('scrapey.db')
    cur = conn.cursor()

    # cur.execute("""CREATE TABLE IF NOT EXISTS users(
    #    userid INT PRIMARY KEY,
    #    fname TEXT,
    #    lname TEXT,
    #    gender TEXT);
    # """)

    user = ('00002', 'Lois', 'Lane', 'Female')
    cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
    more_users = [('00003', 'Peter', 'Parker', 'Male'), ('00004', 'Bruce', 'Wayne', 'male')]
    cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", more_users)
    conn.commit()

    # CREATE TABLE
    # "Post"(
    #     "id"
    # INTEGER
    # NOT
    # NULL
    # UNIQUE,
    # "Field2"
    # INTEGER,
    # PRIMARY
    # KEY("id"
    # AUTOINCREMENT)
    # );