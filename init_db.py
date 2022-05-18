import sqlite3
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

sql_query = """ CREATE TABLE users (
    userid int PRIMARY KEY,
    username text NOT NULL, 
    password text NOT NULL
)"""

drink_query = """ CREATE TABLE drinksnew (
    drinkid int PRIMARY KEY,
    drink_name text NOT NULL,
    user text NOT NULL
)"""

#cursor.execute(sql_query)
cursor.execute(drink_query)
