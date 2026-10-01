import sqlite3

DATABASE = "../soc.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("SELECT * FROM alerts")

alerts = cursor.fetchall()

for alert in alerts:
    print(alert)

connection.close()