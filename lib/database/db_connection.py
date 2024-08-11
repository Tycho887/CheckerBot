import sqlite3
from .db_structure import db_name, db_structure

# We create a decorator function that handles the connection to the database and closes it after the function is executed.
def connect(function):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        result = function(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper

@connect
def create_database(cursor):
    for table_name, table_structure in db_structure.items():
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{column} {datatype}' 
                                                                              for column, datatype 
                                                                              in table_structure.items()])})")
        
if __name__ == "__main__":
    db_name = "../../" + db_name
    create_database()