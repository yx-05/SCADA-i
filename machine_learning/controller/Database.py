# Database.py
# Database utility class
# Define the connection to db and collect the function to retreive or store data in the db

import sqlite3

class Database():
    def __init__(self, db_name):
        """Initialize the connection with sqlite"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to SQLite database and create a cursor."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            