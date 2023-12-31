import sqlite3

connection = sqlite3.connect(r"C:\sqlite\bat_criminals.db")
cursor = connection.cursor()

with open(r"C:\sqlite\criminals.csv", "r") as file1:
    no_records = 0
    for row in file1:
        values = row.strip().split(",")  # Split values and remove leading/trailing spaces
        if len(values) == 7:
            cursor.execute("INSERT INTO criminals VALUES(?,?,?,?,?,?,?)", values)
            connection.commit()
            no_records += 1

connection.close()
print(f"\n{no_records} records transferred into database!")
