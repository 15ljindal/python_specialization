import sqlite3

conn = sqlite3.connect('orgemaildb.sqlite')
conn.set_trace_callback(print)
cur = conn.cursor()

tableName = "Counts"
col1 = "org"
col2 = "count"
cur.execute(f"DROP TABLE IF EXISTS {tableName}")
cur.execute(f"CREATE TABLE {tableName} ({col1} TEXT, {col2} INTEGER)")

fname = input("Enter file name: ")
fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split('@')
    org = pieces[1]
    org = org.rstrip()
    
    cur.execute(f"SELECT {col1} FROM {tableName} WHERE {col1} = ? ", (org, ))
    # print(f"QUERY: [{cur.query.decode()}]")

    row = cur.fetchone()
    # https://www.tutorialspoint.com/sqlite/sqlite_python.htm
    if row is None:
        cur.execute(f"INSERT INTO {tableName} ({col1}, {col2}) VALUES (?, 1)", (org,))
    else:
        cur.execute(f"UPDATE {tableName} SET {col2} = {col2} + 1 WHERE {col1} = ? ", (org,))
    # print(f"QUERY: [{cur.query.decode()}]")

    conn.commit()

# Not sure if fetchall is needed in statement below. works even wtihout it
allRows = cur.execute(f"SELECT * FROM {tableName} ORDER BY count DESC LIMIT 5").fetchall()
for row in allRows:
    print(f"{row[0]} -> {row[1]}")

cur.close()


