import sqlite3
import pandas as pd
print("Generating plots")
conn = sqlite3.connect('flask-app\data\data.db')
query = """
SELECT id, user_id, english_word, time, correct
FROM Interactions
"""
df = pd.read_sql_query(query, conn)
conn.close()
print(df['time'])