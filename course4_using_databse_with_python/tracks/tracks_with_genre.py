import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb_with_genre.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);

''')

fname = input('Enter file name:')
if (len(fname) < 1):
    fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

data = ET.parse(fname)
allTracks = data.findall('dict/dict/dict')  # tracks are part of the third level of dictionary
print(f"Number of tracks: [{len(allTracks)}]")

tracksAdded = 0
for track in allTracks:
    if (lookup(track, "Track ID") is None):
        continue

    name = lookup(track, "Name")
    artist = lookup(track, "Artist")
    album = lookup(track, "Album")
    genre = lookup(track, "Genre")
    length = lookup(track, "Total Time")

    if name is None or artist is None or album is None or genre is None:
        continue

    print(f"{name}, {artist}, {album}, {genre}, {length}")

    cur.execute("INSERT OR IGNORE INTO Artist (name) VALUES (?)", (artist,))
    cur.execute("SELECT id from Artist WHERE name = ?", (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?, ?)", (artist_id, album))
    cur.execute("SELECT id from Album WHERE title = ?", (album,))
    album_id = cur.fetchone()[0]
    
    cur.execute("INSERT OR IGNORE INTO Genre (name) VALUES (?)", (genre,))
    cur.execute("SELECT id from Genre WHERE name = ?", (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute("INSERT OR REPLACE INTO Track (title, album_id, genre_id, len) VALUES (?, ?, ?, ?)",
                (name, album_id, genre_id, length))
    
    conn.commit()
    tracksAdded += 1

print(f"Number of tracks added: [{tracksAdded}]")


    

