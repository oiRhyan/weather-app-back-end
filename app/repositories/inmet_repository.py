import sqlite3
import math
from pathlib import Path
from typing import Any

DATABASE_PATH = Path("data/database/inmet.db")

class InmetRepository:

    def __init__(
        self,
        database_path: str | Path = DATABASE_PATH
    ):
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path
        )
        connection.row_factory = sqlite3.Row
        return connection

    def get_station(
        self,
        station_id: str
    ) -> dict[str, Any] | None:
        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT
                    station_id,
                    station_name,
                    state,
                    region,
                    latitude,
                    longitude,
                    altitude
                FROM stations
                WHERE station_id = ?
                """,
                (station_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            connection.close()

    def get_all_stations(
        self
    ) -> list[dict[str, Any]]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT
                    station_id,
                    station_name,
                    state,
                    region,
                    latitude,
                    longitude,
                    altitude
                FROM stations
                ORDER BY state, station_name
                """
            )
            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_stations_by_state(
        self,
        state: str
    ) -> list[dict[str, Any]]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT
                    station_id,
                    station_name,
                    state,
                    region,
                    latitude,
                    longitude,
                    altitude
                FROM stations
                WHERE state = ?
                ORDER BY station_name
                """,
                (state,)
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_nearest_station(
        self,
        latitude: float,
        longitude: float
    ) -> dict[str, Any] | None:

        stations = self.get_all_stations()

        if not stations:
            return None

        def calculate_distance(
            station: dict[str, Any]
        ) -> float:

            lat1 = math.radians(latitude)
            lon1 = math.radians(longitude)

            lat2 = math.radians(
                station["latitude"]
            )

            lon2 = math.radians(
                station["longitude"]
            )

            delta_lat = lat2 - lat1
            delta_lon = lon2 - lon1

            a = (
                math.sin(delta_lat / 2) ** 2
                +
                math.cos(lat1)
                *
                math.cos(lat2)
                *
                math.sin(delta_lon / 2) ** 2
            )

            c = 2 * math.atan2(
                math.sqrt(a),
                math.sqrt(1 - a)
            )

            earth_radius_km = 6371

            return earth_radius_km * c

        nearest_station = min(
            stations,
            key=calculate_distance
        )

        nearest_station["distance_km"] = round(
            calculate_distance(nearest_station),
            2
        )

        return nearest_station

    def get_observations(
        self,
        station_id: str,
        start_date: str,
        end_date: str
    ) -> list[dict[str, Any]]:
        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM observations
                WHERE station_id = ?
                  AND date BETWEEN ? AND ?
                ORDER BY date, hour_utc
                """,
                (
                    station_id,
                    start_date,
                    end_date
                )
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_observations_by_date(
        self,
        station_id: str,
        date: str
    ) -> list[dict[str, Any]]:
        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT *
                FROM observations
                WHERE station_id = ?
                  AND date = ?
                ORDER BY hour_utc
                """,
                (
                    station_id,
                    date
                )
            )
            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:
            connection.close()

    def get_precipitation(
        self,
        station_id: str,
        start_date: str,
        end_date: str
    ) -> list[dict[str, Any]]:

        connection = self._connect()

        try:
            cursor = connection.execute(
                """
                SELECT
                    date,
                    hour_utc,
                    precipitation
                FROM observations
                WHERE station_id = ?
                  AND date BETWEEN ? AND ?
                ORDER BY date, hour_utc
                """,
                (
                    station_id,
                    start_date,
                    end_date
                )
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]
        finally:
            connection.close()

    def get_weather_summary(
    self,
    station_id: str,
    start_date: str,
    end_date: str
    ) -> dict[str, Any]:

        connection = self._connect()

        try:
            database_start_date = start_date.replace("-", "/")
            database_end_date = end_date.replace("-", "/")

            cursor = connection.execute(
                """
                SELECT
                    AVG(temperature)
                        AS average_temperature,

                    MAX(temperature)
                        AS max_temperature,

                    MIN(temperature)
                        AS min_temperature,

                    AVG(humidity)
                        AS average_humidity,

                    SUM(precipitation)
                        AS total_precipitation,

                    MAX(precipitation)
                        AS max_hourly_precipitation,

                    AVG(wind_speed)
                        AS average_wind_speed,

                    MAX(wind_gust)
                        AS max_wind_gust

                FROM observations

                WHERE station_id = ?
                AND date BETWEEN ? AND ?
                """,
                (
                    station_id,
                    database_start_date,
                    database_end_date
                )
            )

            row = cursor.fetchone()

            if not row:
                return {}

            return dict(row)

        finally:
            connection.close()