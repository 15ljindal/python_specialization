import urllib.request, urllib.parse, urllib.error
from twitter_url import augment
import ssl
import json
import sqlite3

print('Calling Twitter...')
TWITTER_URL = "https://api.twitter.com/1.1/friends/list.json"

conn = sqlite3.connect('twitter_friends.sqlite')
cur = conn.cursor()

tableName = "TwitterFriends"
cur.execute(f"CREATE TABLE IF NOT EXISTS {tableName} (name TEXT, retrieved INTEGER, friends INTEGER)")

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    acct = input("Enter a twitter account or enter 'quit' to stop:")
    acct = acct.strip()
    print(f"User entered: [{acct}]")
    if (acct == "quit"):
        break
    if (len(acct) < 1):
        # user did not enter a new name. we will get friends of an account that has not been "retrieved" already
        cur.execute(f"SELECT name FROM {tableName} WHERE retrieved = 0 LIMIT 1")
        try:
            acct = cur.fetchone()[0]
        except:
            print("No unretrieved accounts found!")
            continue

    url = augment(TWITTER_URL, {'screen_name': acct, 'count': '5'})
    print(f"Retrieve url: {url}")
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    print(f"Remaining: {headers['x-rate-limit-remaining']}")
    js = json.loads(data)

    cur.execute(f"UPDATE {tableName} SET retrieved = 1 WHERE name = ?", (acct, ))

    # look at friends of the account retrieved. for each friend:
    # if the friend already exists in the table:
    #   update it friend count by 1
    # else:
    #   add that friend account into the table
    countNew = 0
    countOld = 0
    for f in js['users']:
        fName = f['screen_name']
        print(f"Processing friend: {fName}")
        cur.execute(f"SELECT friends FROM {tableName} WHERE name = ? LIMIT 1", (fName,))
        try:
            count = cu.fetchOne()[0]
            cur.execute(f"UPDATE {tableName} SET friends = ? WHERE name = ?", (count + 1, fName))
            countOld += 1
        except:
            cur.execute(f"INSERT INTO {tableName} (name, retrieved, friends) VALUES (?, 0, 1)", (fName, ))
            countNew += 1
        
    print(f"New accounts added: {countNew} Accounts updated: {countOld}")
    conn.commit()
