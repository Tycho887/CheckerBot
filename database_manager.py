import sqlite3
import numpy as np
import functions as f
from abc import ABC, abstractmethod
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DatabaseManager:
    """A class to manage the database
    The database consists of two tables: users and records

    The users table stores 2 columns:

    id: the primary key, an integer that uniquely identifies the user
    name: the name of the user

    The users table stores the users that have opted into the service

    The records table stores 8 columns:

    Meta information

    id: the primary key
    user_id: the id of the user that the record belongs to
    date: the day at which the record was created

    these scores are all integers between 1 and 5

    Well-being: the well-being score
    Energy: the energy score
    Productivity: the productivity score
    Stress: the stress score
    Depression: the depression score

    the overall score is a real number calculated from the scores above

    Score: the overall score (real number)

    """

    def __init__(self, db_name="database/CheckIn.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, 
                            user_id INTEGER, 
                            date TEXT, 
                            well_being INTEGER, 
                            energy INTEGER, 
                            productivity INTEGER, 
                            stress INTEGER, 
                            depression INTEGER, 
                            score REAL)""")
        
    def add_user(self, name):

        # check if the user already exists

        self.cursor.execute("SELECT * FROM users WHERE name=?", (name,))

        if self.cursor.fetchone() is not None:
            return

        # find the highest id in the users table

        self.cursor.execute("SELECT MAX(id) FROM users")

        # fetchone returns a tuple, so we need to extract the integer

        user_id = self.cursor.fetchone()[0]

        if user_id is None:
            user_id = 0
        else:
            user_id += 1

        # insert the user into the table

        self.cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, name))

        self.conn.commit()

    def get_user_id(self, name):

        self.cursor.execute("SELECT id FROM users WHERE name=?", (name,))

        return self.cursor.fetchone()[0]

    def add_record(self, user, well_being, energy, productivity, stress, depression):

        # find the user id

        user_id = self.get_user_id(user)

        # find the date

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # calculate the score

        input_vector = np.array([well_being, energy, productivity, stress, depression], dtype=int)

        score = f.score(input_vector)

        # insert the record into the table

        self.cursor.execute("""INSERT INTO records (user_id, 
                            date, 
                            well_being, 
                            energy, 
                            productivity, 
                            stress, 
                            depression, 
                            score) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (user_id, date, well_being, energy, productivity, stress, depression, score))

        self.conn.commit()

    def get_records(self, user, start_date = None, end_date = None):

        assert start_date is None or isinstance(start_date, str), "start_date must be a string"
        assert end_date is None or isinstance(end_date, str), "end_date must be a string"

        # find the user id

        user_id = self.get_user_id(user)

        # find the records for the different cases
        
        if start_date is None and end_date is None:
            self.cursor.execute("SELECT * FROM records WHERE user_id=?", (user_id,))

        elif start_date is not None and end_date is None:
            self.cursor.execute("SELECT * FROM records WHERE user_id=? AND date>=?", (user_id, start_date))

        elif start_date is None and end_date is not None:
            self.cursor.execute("SELECT * FROM records WHERE user_id=? AND date<=?", (user_id, end_date))

        else:
            self.cursor.execute("SELECT * FROM records WHERE user_id=? AND date BETWEEN ? AND ?", (user_id, start_date, end_date))

        return self.cursor.fetchall()
    
    def get_users(self):

        self.cursor.execute("SELECT * FROM users")

        return self.cursor.fetchall()

    def close(self):
            
            self.conn.close()

    def plot_score_vs_date(self, user, score_type, start_date=None, end_date=None):
        # Fetch the records
        records = self.get_records(user, start_date, end_date)
        
        # Define the score column names in the order they appear in the database
        score_columns = ["well_being", "energy", "productivity", "stress", "depression", "score"]
        
        # Convert the records to a DataFrame
        columns = ["id", "user_id", "date"] + score_columns
        df = pd.DataFrame(records, columns=columns)
        
        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'])
        
        # Plot the specified score against the date
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x='date', y=score_type)
        plt.title(f'{score_type.replace("_", " ").title()} over Time for {user}')
        plt.xlabel('Date')
        plt.ylabel(score_type.replace("_", " ").title())
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(f'plots/{user}_{score_type}_vs_date.png')

        plt.show()

# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.close()


if __name__ == "__main__":

    db = DatabaseManager()

    db.add_user("Alice")
    db.add_user("Bob")

    db.add_record("Alice", 5, 5, 5, 1, 1)
    db.add_record("Alice", 1, 1, 1, 5, 5)
    db.add_record("Bob", 3, 3, 3, 3, 3)

    # print(db.get_records("Alice"))
    print(db.get_records("Alice", start_date="2024-08-1"))
    print(db.get_records("Alice", end_date="2021-07-1"))
    print(db.get_records("Alice", start_date="2024-07-1", end_date="2024-08-7"))

    print(db.get_users())

    db.plot_score_vs_date("Alice", "score")

    db.close()