import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
conn.set_trace_callback(print)
cur = conn.cursor()

tableName = "Emails"
cur.execute(f"DROP TABLE IF EXISTS {tableName}")
cur.execute(f"CREATE TABLE {tableName} (email TEXT, count INTEGER)")

fname = input("Enter file name: ")
fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    
    cur.execute(f"SELECT count FROM {tableName} WHERE email = ? ", (email, ))
    # print(f"QUERY: [{cur.query.decode()}]")

    row = cur.fetchone()
    # https://www.tutorialspoint.com/sqlite/sqlite_python.htm
    if row is None:
        cur.execute(f"INSERT INTO {tableName} (email, count) VALUES (?, 1)", (email,))
    else:
        cur.execute(f"UPDATE {tableName} SET count = count + 1 WHERE email = ? ", (email,))
    # print(f"QUERY: [{cur.query.decode()}]")

    conn.commit()

# Not sure if fetchall is needed in statement below. works even wtihout it
allRows = cur.execute(f"SELECT * FROM {tableName} ORDER BY count DESC LIMIT 5").fetchall()
for row in allRows:
    print(f"{row[0]} -> {row[1]}")

cur.close()


