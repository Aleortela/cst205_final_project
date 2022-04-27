import sqlite3
conn = sqlite3.connect("205final.sqlite")
cursor = conn.cursor()

sql_query = """ CREATE TABLE users (
    userid int PRIMARY KEY,
    username text NOT NULL, 
    password text NOT NULL
)"""

cursor.execute(sql_query)