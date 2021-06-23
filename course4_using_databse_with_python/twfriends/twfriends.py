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

def addNewUser(uname):
    DB_CURSOR.execute("INSERT OR IGNORE INTO People (name, retrieved) Values (?, ?)", (uname, 0))
    DB_CONN.commit()  # important so that subsequent SELECTs can find the entry
    
def setUserAsRetrieved(uname):
    DB_CURSOR.execute("UPDATE People SET retrieved = 1 WHERE name = (?)", (uname, ))
    DB_CONN.commit()

def getUserInfo(user):
    DB_CURSOR.execute("SELECT * FROM People WHERE name = (?)", (user,))
    return DB_CURSOR.fetchone()

def getUserId(user):
    (uid, uname, retrieved) = getUserInfo(user)
    return uid

def addNewConnection(uname, fname):
    uid = getUserId(uname)
    fid = getUserId(fname)
    print(f"Adding connection from {uid}:{uname} to {fid}:{fname}")
    DB_CURSOR.execute("INSERT OR IGNORE INTO Follows (from_id, to_id) Values (?, ?)", (uid, fid))
    DB_CONN.commit()

def getNextUser(uname):
    if uname:
        try:
            (uid, uname, retrieved) = getUserInfo(uname)
        except Exception as e:
            # user does not exist already
            return uname
        if (retrieved):
            print(f"uname: {uname} has already been retrieved")
            uname = ""
    else:
        # find a user that has not been retrieved yet
        DB_CURSOR.execute("SELECT name FROM People WHERE retrieved = 0 LIMIT 1")
        try:
            uname = DB_CURSOR.fetchone()[0]
        except:
            uname = ""
    return uname

def getTwitterFriends(uname):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    url = augment(TWITTER_URL, {'screen_name': uname, 'count': '5'})
    try:
        connection = urllib.request.urlopen(url, context=CTX)
    except Exception as e:
        print(f"Could not retrieve user: {uname} error: [{e}]")
        return []
    
    # fetch was successful
    addNewUser(uname)
    setUserAsRetrieved(uname)

    data = connection.read().decode()
    headers = dict(connection.getheaders())

    print(f"Remaining: [{headers['x-rate-limit-remaining']}]")
    try:
        js = json.loads(data)
    except:
        print(f'ERROR: Unable to parse json: [{data}]')
        return []
    if 'users' not in js:
        print(f"ERROR: could not find 'users' in: [{js}]")
        return []
    return js['users']

def main():
    while True:
        uname = input("Enter user name or type 'quit':")
        uname = uname.strip()
        if (uname == "quit"):
            break
        uname = getNextUser(uname)
        
        if (not uname):
            print(f"No user to retrieve.")
            continue
        print(f"Will retrieve uname: {uname}")
    
        friends = getTwitterFriends(uname)
        for f in friends:
            fname = f['screen_name']
            print(fname)
            addNewUser(fname)
            addNewConnection(uname, fname)

if __name__ == "__main__":
    main()
