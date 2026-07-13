import sqlite3


class Database:

    def __init__(self, db_name="uber_predictions.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute()

        conn.commit()
        conn.close()