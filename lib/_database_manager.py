import sqlite3
import numpy as np
import lib._functions as f
import datetime
from prompt import analyse_message_with_LLM
class DatabaseManager:

    """A class to manage the database
    The database consists of two tables: users and records.

    The users table stores:
    - id: the primary key, an integer that uniquely identifies the user
    - name: the name of the user

    The records table stores:
    - id: the primary key
    - user_id: the id of the user that the record belongs to
    - date: the day at which the record was created
    - well_being: integer score between 1 and 5
    - energy: integer score between 1 and 5
    - productivity: integer score between 1 and 5
    - sentiment: a real number between -1.0 (negative) and 1.0 (positive)
    - mood: a real number between 0.0 (bad) and 1.0 (good)
    - key_topics: text containing a comma-separated list of key topics
    - score: overall calculated score
    """

    def __init__(self, db_name="lib/database/CheckIn.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS records (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            user_id INTEGER, 
                            date TEXT, 
                            well_being REAL,          -- 0.0 to 10
                            energy REAL,              -- 0.0 to 10
                            productivity INT,         -- 0.0 to 10
                            sentiment INT,            -- -1.0 to 1.0
                            mood INT,                 -- 0.0 to 1.0
                            key_topics TEXT,          -- e.g., "work, family, health"
                            message TEXT,             -- the original message
                            score REAL,               -- overall score, also normalized 0.0 to 1.0
                            FOREIGN KEY(user_id) REFERENCES users(id)
                        );
                        """)

    def add_user(self, user_id, user_name):
        # Check if the user already exists
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        if self.cursor.fetchone() is not None:
            return False
        else:
            user_name = user_name[0].upper() + user_name[1:]
            self.cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, user_name))
            self.conn.commit()
            return True

    def remove_user(self, user_id):
        # Check if the user exists
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        if self.cursor.fetchone() is None:
            return False
        else:
            self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
            return True

    def add_record(self, user_id, LLM_response_dict, message):

        # Find the current date
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Extract the metrics from the LLM response

        well_being = LLM_response_dict['well_being']
        energy = LLM_response_dict['energy']
        productivity = LLM_response_dict['productivity']
        sentiment = LLM_response_dict['sentiment']
        mood = LLM_response_dict['mood']
        key_topics = ", ".join(LLM_response_dict['key_topics'])

        # Calculate the overall score

        score = f.calculate_composite_score()

        # Insert the record into the table
        self.cursor.execute("""INSERT INTO records (
                                user_id, 
                                date, 
                                well_being, 
                                energy, 
                                productivity, 
                                sentiment, 
                                mood, 
                                key_topics,
                                message, 
                                score
                              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (user_id, date, well_being, energy, productivity, sentiment, mood, key_topics, message, score))

        self.conn.commit()
        return True

    def get_records(self, user_id, start_date=None, end_date=None):
        assert start_date is None or isinstance(start_date, str), "start_date must be a string"
        assert end_date is None or isinstance(end_date, str), "end_date must be a string"

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

    def get_user_name(self, user_id):
        self.cursor.execute("SELECT name FROM users WHERE id=?", (user_id,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()
