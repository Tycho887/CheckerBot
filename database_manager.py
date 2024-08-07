import sqlite3
import numpy as np
import functions as f
from abc import ABC, abstractmethod
import datetime

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

    def get_records(self, user, month=None, limit=None):

        assert month is None or isinstance(month, str), "month must be a string"
        assert limit is None or isinstance(limit, int), "limit must be an integer"

        # find the user id

        user_id = self.get_user_id(user)

        # if the limit and month are not specified, return all records
        if limit is None and month is None:

            self.cursor.execute("SELECT * FROM records WHERE user_id=?", (user_id,))

        # if the limit is specified but month is not, return the last n records.

        elif limit is not None and month is None:

            self.cursor.execute("SELECT * FROM records WHERE user_id=? ORDER BY date DESC LIMIT ?", (user_id, limit))

        # if the month is specified but the limit is not, return all records from that month

        elif month is not None and limit is None:

            self.cursor.execute("SELECT * FROM records WHERE user_id=? AND date LIKE ?", (user_id, f"{month}%"))

        # if both the month and the limit are specified, return the last n records from that month

        elif month is not None and limit is not None:
                
                self.cursor.execute("SELECT * FROM records WHERE user_id=? AND date LIKE ? ORDER BY date DESC LIMIT ?", (user_id, f"{month}%", limit))

        return self.cursor.fetchall()
    
    def get_users(self):

        self.cursor.execute("SELECT * FROM users")

        return self.cursor.fetchall()
    
    def close(self):
            
            self.conn.close()

if __name__ == "__main__":

    db = DatabaseManager()

    db.add_user("Alice")
    db.add_user("Bob")

    db.add_record("Alice", 5, 5, 5, 1, 1)
    db.add_record("Alice", 1, 1, 1, 5, 5)
    db.add_record("Bob", 3, 3, 3, 3, 3)

    print(db.get_records("Alice"))
    print(db.get_records("Alice", limit=1))
    print(db.get_records("Alice", month="2021-07"))
    print(db.get_records("Alice", month="2024-08", limit=2))

    db.close()