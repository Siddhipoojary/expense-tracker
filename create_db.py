import sqlite3

conn= sqlite3.connect("expenses.db")
cursor = conn.cursor()



cursor.execute(""" CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,amount INTEGER,reason TEXT,Category TEXT,date TEXT ,FOREIGN KEY (user_id) REFERENCES users(id))""")






conn.commit()
conn.close()

print("Database created successfully")


