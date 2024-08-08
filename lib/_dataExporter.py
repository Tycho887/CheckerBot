from datetime import datetime
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot_score_vs_date(db, user_id, score_type, start_date=None, end_date=None):
    # Fetch the records
    records = db.get_records(user_id, start_date, end_date)
        
    # Define the score column names in the order they appear in the database
    score_columns = ["well_being", "energy", "productivity", "stress", "depression", "score"]
        
    # Convert the records to a DataFrame
    columns = ["id", "user_id", "date"] + score_columns
    df = pd.DataFrame(records, columns=columns)
        
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    user_name = db.get_user_name(user_id)

        
    # Plot the specified score against the date
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='date', y=score_type)
    plt.title(f'{score_type.replace("_", " ").title()} over Time for {user_name}')
    plt.xlabel('Date')
    plt.ylabel(score_type.replace("_", " ").title())
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f'plots/{user_name}_{score_type}_vs_date.png')

    plt.show()