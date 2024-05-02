import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def fetch_data(user=None, start_date=None, end_date=None, word=None):
    conn = sqlite3.connect('flask-app/data/data.db')
    query = """
    SELECT id, user_id, english_word, time, correct, type
    FROM Interactions
    WHERE 1=1
    """
    if user is not None:
        query += f" AND user_id = {user}"
    if start_date is not None:
        query += f" AND time >= '{start_date}'"
    if end_date is not None:
        query += f" AND time <= '{end_date}'"
    if word:
        query += f" AND english_word = '{word}'"
    query += " ORDER BY time;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df



def process_data(df):
    df['time'] = pd.to_datetime(df['time'])
    df['hour'] = df['time'].dt.floor('H')
    df['day'] = df['time'].dt.date
    return df

def plot_correct_answers_by_type(df):
    df_correct_type = df[df['correct'] == 1].groupby(['time', 'type']).size().unstack().rename(columns={0: 'Flashcard', 1: 'Quiz'}).fillna(0)
    df_correct_type.plot(kind='area', stacked=False, alpha=0.5)
    plt.title('Your Correct Answers by Type Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Correct Answers')
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_correct_by_type.png')
    plt.close()

def plot_perseverance_over_time(df):
    df_word_attempts = df.groupby([df['hour'], 'english_word']).size().unstack().fillna(0)
    df_word_attempts.plot(kind='line', marker='o', linestyle='-')
    plt.title('Your Perseverance Over Time')
    plt.xlabel('Hour')
    plt.ylabel('Number of Attempts per Word')
    plt.legend(title='Words', loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_perseverance_over_time.png')
    plt.close()

def plot_perseverance_by_word(df):
    df_attempts_per_word = df.groupby('english_word').size()
    df_attempts_per_word.plot(kind='bar', color='skyblue')
    plt.title('Your Perseverance by Word')
    plt.xlabel('Words')
    plt.ylabel('Total Attempts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_perseverance_by_word.png')
    plt.close()

def plot_interactions_by_type(df):
    df_type_time = df.groupby([df['time'].dt.floor('D'), 'type']).size().unstack().fillna(0)
    df_type_time.plot(kind='bar', stacked=True)
    plt.title('Your Interaction Types Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Interactions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_interactions_by_type.png')
    plt.close()

def plot_correct_answers_by_type(df):
    df_correct_type = df[df['correct'] == 1].groupby(['time', 'type']).size().unstack().fillna(0)
    df_correct_type.plot(kind='area', stacked=False, alpha=0.5)
    plt.title('Your Correct Answers by Type Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Correct Answers')
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_correct_by_type.png')
    plt.close()

def plot_user_activity_by_day(df):
    df_day = df.groupby('day').size()
    df_day.plot(kind='line', marker='o', linestyle='-')
    plt.title('Your Activity by Day')
    plt.xlabel('Day')
    plt.ylabel('Number of Interactions')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))  # Adjust to the number of different days
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_activity_by_day.png')
    plt.close()

def plot_correct_ratio_per_word(df):
    df_word_correct = df.groupby('english_word')['correct'].mean()
    df_word_correct.sort_values().plot(kind='barh', color='green')
    plt.title('Your Correct Answer Ratio per Word')
    plt.xlabel('Ratio of Correct Answers')
    plt.tight_layout()
    plt.savefig(r'flask-app/frontend/static/images/your_correct_ratio_word.png')
    plt.close()

import matplotlib.pyplot as plt

def generate_placeholder_image(filename):
    plt.figure(figsize=(10, 5))
    plt.text(0.5, 0.5, 'No data available for this period', ha='center', va='center', fontsize=14, color='gray')
    plt.axis('off')
    plt.savefig(filename)
    plt.close()

def generate_plots(user=None, start_date=None, end_date=None, word=None):
    print("Generating personal plots with filters")
    df = fetch_data(user, start_date, end_date, word)
    df = process_data(df)

    if df.empty:
        print("No data available. Generating placeholder images.")
        generate_placeholder_image(r'flask-app/frontend/static/images/your_correct_by_type.png')
        generate_placeholder_image(r'flask-app/frontend/static/images/your_perseverance_over_time.png')
        generate_placeholder_image(r'flask-app/frontend/static/images/your_perseverance_by_word.png')
        generate_placeholder_image(r'flask-app/frontend/static/images/your_interactions_by_type.png')
        generate_placeholder_image(r'flask-app/frontend/static/images/your_activity_by_day.png')
        generate_placeholder_image(r'flask-app/frontend/static/images/your_correct_ratio_word.png')
    else:
        plot_interactions_by_type(df)
        plot_correct_answers_by_type(df)
        plot_user_activity_by_day(df)
        plot_correct_ratio_per_word(df)
        plot_perseverance_over_time(df)
        plot_perseverance_by_word(df)
    print("Plots updated or placeholder images set")


if __name__ == '__main__':
    generate_plots()  # Optionally add user=USER_ID
