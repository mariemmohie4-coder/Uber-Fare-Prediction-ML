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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pickup_lat REAL,
                pickup_lon REAL,
                dropoff_lat REAL,
                dropoff_lon REAL,
                pickup_datetime TEXT,
                passenger_count INTEGER,
                trip_distance_km REAL,
                bearing REAL,
                avg_distance_to_center REAL,
                is_airport INTEGER,
                hour_sin REAL,
                hour_cos REAL,
                manhattan_distance REAL,
                displacement_ratio REAL,
                predicted_fare REAL,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()