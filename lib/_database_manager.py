import sqlite3
import numpy as np
import lib._functions as f
import datetime
import lib._dataExporter as de

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

    def __init__(self, db_name="lib/database/CheckIn.db"):

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
        
    def add_user(self, user_id, user_name):

        # check if the user already exists

        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))

        # if the user has already opted in, return False

        if self.cursor.fetchone() is not None:
            return False
        else:
            user_name = user_name[0].upper() + user_name[1:]
            self.cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, user_name))
            self.conn.commit()
            return True

    def remove_user(self, user_id):

        # check if the user exists

        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))

        # if the user does not exist, return False

        if self.cursor.fetchone() is None:
            return False
        else:
            self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
            return True

    def add_record(self, user_id, well_being, energy, productivity, stress, depression):

        assert isinstance(user_id, int), "user_id must be an integer"
        assert isinstance(well_being, int), "well_being must be an integer"
        assert isinstance(energy, int), "energy must be an integer"
        assert isinstance(productivity, int), "productivity must be an integer"
        assert isinstance(stress, int), "stress must be an integer"
        assert isinstance(depression, int), "depression must be an integer"

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

        return True

    def get_records(self, user_id, start_date = None, end_date = None):

        assert start_date is None or isinstance(start_date, str), "start_date must be a string"
        assert end_date is None or isinstance(end_date, str), "end_date must be a string"

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
    
    def get_user_name(self, user_id):
            
        self.cursor.execute("SELECT name FROM users WHERE id=?", (user_id,))
    
        return self.cursor.fetchone()[0]

    def close(self):
            
        self.conn.close()