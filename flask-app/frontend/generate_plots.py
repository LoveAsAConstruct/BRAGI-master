# This function should be in a separate file, such as your_plot_script.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def generate_plots():
    print("Generating plots")
    conn = sqlite3.connect('flask-app\data\data.db')
    query = """
    SELECT id, user_id, english_word, current_time, correct
    FROM Interactions
    WHERE user_id = 1
    ORDER BY current_time;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['current_time'] = pd.to_datetime(df['current_time'])
    df['cumulative_correct'] = df['correct'].cumsum()

    # Plotting user progress over time
    plt.figure(figsize=(10, 6))
    plt.plot(df['current_time'], df['cumulative_correct'], marker='o', linestyle='-')
    plt.title('User Progress Over Time')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Correct Answers')
    plt.grid(True)

    # Set x-axis limits to fit the data
    plt.xlim(df['current_time'].min(), df['current_time'].max())
    start_date = '2024-04-27'  # Example start date
    end_date = '2024-04-30'    # Example end date

    plt.xlim(pd.to_datetime(start_date), pd.to_datetime(end_date))
    plt.savefig(r'flask-app\frontend\static\images\user_progress.png')  # Save the plot as a .png file
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
