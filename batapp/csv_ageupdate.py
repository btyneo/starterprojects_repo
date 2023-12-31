import sqlite3
from random import randint

connection = sqlite3.connect(r"C:\sqlite\bat_criminals.db")
cursor = connection.cursor()

# Update each row with a random age
cursor.execute("SELECT rowid FROM criminals")
row_ids = cursor.fetchall()

for row_id in row_ids:
    age = randint(22, 61)
    cursor.execute("UPDATE criminals SET age = ? WHERE rowid = ?", (age, row_id[0]))
    connection.commit()

connection.close()
print("Ages updated successfully!")
