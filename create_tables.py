import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
cursor.execute( query)

query = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL)"
cursor.execute( query)

# query = "INSERT INTO users VALUES (NULL, ?, ?)"
# cursor.execute( query, ("gaga", "qwerty"))

connection.commit()

query = "SELECT * FROM users"
for row in cursor.execute( query) :
    print( row)

connection.close()
