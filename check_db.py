import sqlite3

conn=sqlite3.connect("expenses.db")
cur=conn.cursor()

cur.execute("SELECT reason,Category FROM expenses")
rows = cur.fetchall()
print(rows)

conn.close()