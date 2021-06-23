# fetch the friends of a user
# store data in two tables: People - usernames and retrieved, Follows - which user id follows which user id
# ask user to enter a username that will be fetched next
# if user does not enter a username, then try to fetch a user from table "People" who has not already been fetched

import urllib.request, urllib.parse, urllib.error
from twitter_url import augment
import ssl
import json
import sqlite3

DB_CONN = sqlite3.connect("friends.sqlite")
DB_CURSOR = DB_CONN.cursor()

# FIXME remove these
DB_CURSOR.execute("DROP TABLE IF EXISTS People")
DB_CURSOR.execute("DROP TABLE IF EXISTS Follows")

DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS People (id INTEGER PRIMARY KEY, name TEXT UNIQUE, retrieved INTEGER)")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Follows (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))")

# Ignore SSL certificate errors
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def getNextUser(uname):
    uid = -1
    if uname:
        # insert the user if needed, retrieve if not already retrieved
        DB_CURSOR.execute("INSERT OR IGNORE INTO People (name, retrieved) Values (?, ?)", (uname, 0))
        DB_CONN.commit()  # important so that subsequent SELECTs can find the entry
        DB_CURSOR.execute("SELECT * FROM People WHERE name = (?)", (uname,))
        (uid, uname, retrieved) = DB_CURSOR.fetchone()
        if (retrieved):
            (uid, uname) = (-1, "")
        else:
            DB_CURSOR.execute("UPDATE People SET retrieved = 1 WHERE id = (?)", (uid, ))
    else:
        # find a user that has not been retrieved yet
        DB_CURSOR.execute("SELECT id, name FROM People WHERE retrieved = 0 LIMIT 1")
        try:
            (uid, uname) = DB_CURSOR.fetchone()
        except:
            (uid, uname) = (-1,"")
    return (uid, uname)

while True:
    uname = input("Enter user name or type 'quit':")
    uname = uname.strip()
    if (uname == "quit"):
        break
    (uid, uname) = getNextUser(uname)
    
    if (not uname):
        print(f"No user to retrieve.")
        continue
    print(f"Will retrieve uid: {uid} uname: {uname}")

    


