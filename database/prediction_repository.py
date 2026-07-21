from datetime import datetime
from database.database import Database

class PredictionRepository:
    def __init__(self):
        self.database = Database()

    def save_prediction(
        self,
        pickup_lat,
        pickup_lon,
        dropoff_lat,
        dropoff_lon,
        pickup_datetime,
        passenger_count,
        trip_distance_km,
        bearing,
        avg_distance_to_center,
        is_airport,
        hour_sin,
        hour_cos,
        manhattan_distance,
        displacement_ratio,
        predicted_fare
    ):
        conn = self.database.connect()
        cursor = conn.cursor()

        query = """
            INSERT INTO predictions (
                pickup_lat, pickup_lon, dropoff_lat, dropoff_lon,
                pickup_datetime, passenger_count, trip_distance_km, bearing,
                avg_distance_to_center, is_airport, hour_sin, hour_cos,
                manhattan_distance, displacement_ratio, predicted_fare, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            pickup_lat,
            pickup_lon,
            dropoff_lat,
            dropoff_lon,
            str(pickup_datetime),
            passenger_count,
            trip_distance_km,
            bearing,
            avg_distance_to_center,
            is_airport,
            hour_sin,
            hour_cos,
            manhattan_distance,
            displacement_ratio,
            predicted_fare,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()