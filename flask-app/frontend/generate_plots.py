# This function should be in a separate file, such as your_plot_script.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def generate_plots(user = 1):
    print("Generating plots")
    conn = sqlite3.connect('flask-app\data\data.db')
    if user is not None:
        query = f"""
        SELECT id, user_id, english_word, time, correct
        FROM Interactions
        WHERE user_id = {user}
        ORDER BY time;
        """
    else:
        query = f"""
        SELECT id, user_id, english_word, time, correct
        FROM Interactions
        ORDER BY time;
        """
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df['time'])
    df['time'] = pd.to_datetime(df['time'])
    df['cumulative_correct'] = df['correct'].cumsum()

    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Print first few rows to verify correct timestamps
    print(df.head())
    print(df['time'])
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df['cumulative_correct'],linestyle='-', color='blue')
    plt.title('User Progress Over Time')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Correct Answers')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(r'flask-app\frontend\static\images\user_progress.png'   )
    plt.close()
    
    df['attempts'] = df.groupby('english_word')['english_word'].transform('count')
    df['correct_attempts'] = df.groupby('english_word')['correct'].transform('sum')
    
    plt.figure(figsize=(10, 6))
    df_unique = df.drop_duplicates(subset='english_word')
    plt.bar(df_unique['english_word'], df_unique['attempts'], color='skyblue')
    plt.title('Perseverance: Attempts per Word')
    plt.xlabel('Words')
    plt.ylabel('Number of Attempts')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(r'flask-app\frontend\static\images\perseverance.png')
    plt.close()

    df_unique['success_rate'] = df_unique['correct_attempts'] / df_unique['attempts']
    plt.figure(figsize=(10, 6))
    plt.bar(df_unique['english_word'], df_unique['success_rate'], color='green')
    plt.title('Knowledge: Success Rate per Word')
    plt.xlabel('Words')
    plt.ylabel('Success Rate')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(r'flask-app\frontend\static\images\knowledge.png')
    plt.close()
    print("Plots updated")
generate_plots()