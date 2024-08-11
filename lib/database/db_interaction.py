import sqlite3
import datetime
from .db_connection import connect
from .db_structure import db_structure, get_fields
from lib.utility import calculate_composite_score

@connect
def add_user(cursor, user_id, user_name):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    if cursor.fetchone() is not None:
        return False
    else:
        user_name = user_name[0].upper() + user_name[1:]
        cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, user_name))
        return True
    
@connect
def remove_user(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    if cursor.fetchone() is None:
        return False
    else:
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        return True

@connect
def add_data_to_records(cursor, user_id, data, message):
    """
    user_id: int
    data: dict
    message: str
    """

    cursor.execute("""INSERT INTO records 
                   (user_id, 
                   date, 
                   well_being, 
                   energy, 
                   productivity, 
                   sentiment, 
                   mood, 
                   score, 
                   key_topics, 
                   message) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (user_id, 
                    datetime.datetime.now().isoformat(), 
                    data["well_being"], 
                    data["energy"], 
                    data["productivity"], 
                    data["sentiment"], 
                    data["mood"], 
                    calculate_composite_score(data), 
                    ", ".join(data["key_topics"]), 
                    message))
                        
@connect
def add_incident(cursor, user_id, incident):
    """
    user_id: int
    incident: str
    """

    cursor.execute("""INSERT INTO incidents 
                   (user_id, 
                   date, 
                   incident) 
                   VALUES (?, ?, ?)""",
                   (user_id, 
                    datetime.datetime.now().isoformat(), 
                    incident))
    
@connect
def get_users(cursor):
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@connect
def get_user_name(cursor, user_id):
    cursor.execute("SELECT name FROM users WHERE id=?", (user_id,))
    return cursor.fetchone()[0]

@connect
def get_last_n_records_for_user(cursor, user_id, limit=10, column=None):
    """
    Get the last N records data for a user.
    If column is None, all columns are selected.

    user_id: int
    column: str (well_being, energy, productivity, sentiment, mood, score, message)
    limit: int (Number of records to retrieve)
    """

    if column is None:
        column = "*"
    else:
        assert isinstance(column, str), f"Column name must be a string, got {column}."
        assert column in get_fields("records"), "Invalid column name."

    assert isinstance(limit, int) and limit > 0, "Limit must be a positive integer."

    cursor.execute(f"SELECT {column} FROM records WHERE user_id=? ORDER BY date DESC LIMIT ?", (user_id, limit))

    return cursor.fetchall()


@connect
def get_all_records(cursor):
    cursor.execute("SELECT * FROM records")
    return cursor.fetchall()

@connect
def get_incidents_for_user(cursor, user_id):
    """
    Get all incidents for a user.
    user_id: int
    """
    cursor.execute("SELECT * FROM incidents WHERE user_id=?", (user_id,))
    return cursor.fetchall()