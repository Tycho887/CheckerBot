import unittest
import sqlite3
import os
import datetime
from lib.database import (
    create_database, add_user, remove_user, add_data_to_records, 
    add_incident, get_users, get_last_n_records_for_user, 
    get_all_records, get_incidents_for_user
)
from lib.utility import calculate_composite_score

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a temporary database
        cls.db_name = 'tests/test_db_file.db'
        global db_name
        db_name = cls.db_name
        create_database()

    @classmethod
    def tearDownClass(cls):
        # Remove the database file after tests
        os.remove(cls.db_name)

    def test_add_user(self):
        # Test adding a new user
        result = add_user(1, 'john')
        self.assertTrue(result)
        
        # Test preventing duplicate user addition
        result = add_user(1, 'john')
        self.assertFalse(result)

        # Test user retrieval
        users = get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], 'John')  # Name should be capitalized

    def test_remove_user(self):
        add_user(2, 'jane')
        
        # Test removing existing user
        result = remove_user(2)
        self.assertTrue(result)
        
        # Test removing non-existent user
        result = remove_user(2)
        self.assertFalse(result)

    def test_add_data_to_records(self):
        data = {
            'well_being': 0.9,
            'energy': 0.8,
            'productivity': 10,
            'sentiment': 6,
            'mood': 5,
            'key_topics': ['work', 'health']
        }
        add_user(3, 'alice')
        add_data_to_records(3, data, 'Feeling good today')

        # Check if record was added correctly
        records = get_last_n_records_for_user(3)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][-2], calculate_composite_score(data))  # Checking composite score

    def test_add_incident(self):
        add_user(4, 'bob')
        add_incident(4, 'Had a minor accident')

        # Check if incident was added correctly
        incidents = get_incidents_for_user(4)
        self.assertEqual(len(incidents), 1)
        self.assertEqual(incidents[0][-1], 'Had a minor accident')

    def test_get_last_n_records_for_user(self):
        add_user(5, 'charlie')
        data1 = {'well_being': 0.7, 'energy': 0.6, 'productivity': 0.5, 'sentiment': 0.4, 'mood': 0.3, 'key_topics': ['topic1']}
        data2 = {'well_being': 0.9, 'energy': 0.8, 'productivity': 0.7, 'sentiment': 0.6, 'mood': 0.5, 'key_topics': ['topic2']}
        add_data_to_records(5, data1, 'First entry')
        add_data_to_records(5, data2, 'Second entry')

        # Retrieve last record
        records = get_last_n_records_for_user(5, limit=1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][-2], calculate_composite_score(data2))

        # Retrieve all records
        records = get_last_n_records_for_user(5)
        self.assertEqual(len(records), 2)

    def test_get_all_records(self):
        # Assumes data has already been added in previous tests
        all_records = get_all_records()
        self.assertGreater(len(all_records), 0)

if __name__ == '__main__':
    unittest.main()
