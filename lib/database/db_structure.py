db_name = "database/CheckIn.db"

db_structure = {
    "users": {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT"
    },
    "records": {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER",
        "date": "TEXT",
        "well_being": "INT",
        "energy": "INT",
        "productivity": "INT",
        "sentiment": "TEXT",
        "mood": "TEXT",
        "score": "REAL",
        "key_topics": "TEXT",
        "message": "TEXT",
        "FOREIGN KEY(user_id)": "REFERENCES users(id)"
    },
    "incidents": {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER",
        "date": "TEXT",
        "incident": "TEXT",
        "FOREIGN KEY(user_id)": "REFERENCES users(id)"
    }
}

def get_fields(table):
    """
    Returns a list of fields that can be interacted with in a table.
    
    :param table: str
    :return: list
    """
    return [field for field in db_structure[table].keys() if (field != "id" and "FOREIGN" not in field)]