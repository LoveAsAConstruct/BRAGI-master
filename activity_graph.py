import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('data.db')

# Query data from the Interactions table
query = """
SELECT id, user_id, english_word, current_time, correct
FROM Interactions
WHERE user_id = 1
ORDER BY current_time;
"""
df = pd.read_sql_query(query, conn)
conn.close()  # Close the connection to the database

# Convert current_time to datetime
df['current_time'] = pd.to_datetime(df['current_time'])

# Calculate cumulative correct answers
df['cumulative_correct'] = df['correct'].cumsum()

# Plotting user progress over time
plt.figure(figsize=(10, 6))
plt.plot(df['current_time'], df['cumulative_correct'], marker='o', linestyle='-')
plt.title('User Progress Over Time')
plt.xlabel('Time')
plt.ylabel('Cumulative Correct Answers')
plt.grid(True)
plt.show()

# Calculate total attempts and successful attempts per word
df['attempts'] = df.groupby('english_word')['english_word'].transform('count')
df['correct_attempts'] = df.groupby('english_word')['correct'].transform('sum')

# Perseverance plot (attempts per word)
plt.figure(figsize=(10, 6))
df_unique = df.drop_duplicates(subset='english_word')
plt.bar(df_unique['english_word'], df_unique['attempts'], color='skyblue')
plt.title('Perseverance: Attempts per Word')
plt.xlabel('Words')
plt.ylabel('Number of Attempts')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Knowledge plot (success rate per word)
df_unique['success_rate'] = df_unique['correct_attempts'] / df_unique['attempts']
plt.figure(figsize=(10, 6))
plt.bar(df_unique['english_word'], df_unique['success_rate'], color='green')
plt.title('Knowledge: Success Rate per Word')
plt.xlabel('Words')
plt.ylabel('Success Rate')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
