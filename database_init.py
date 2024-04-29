import sqlite3

# Connect to a database (or create it if it doesn't exist)
conn = sqlite3.connect('data.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table as per requirement
sql ='''CREATE TABLE Interactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    english_word TEXT,
    current_time TEXT DEFAULT CURRENT_TIMESTAMP,
    correct BOOLEAN
);'''
cursor.execute(sql)

# Commit your changes in the database
conn.commit()

# Close the connection
conn.close()
