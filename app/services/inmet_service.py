from datetime import date, timedelta

from app.tools.inmet_tool import (
    get_nearest_inmet_station,
    get_inmet_weather_summary
)

class InmetService:

    def __init__(self):
        self.period_days = 7

    def get_data(
        self,
        latitude: float,
        longitude: float
    ) -> dict:

        station = get_nearest_inmet_station.invoke({
            "latitude": latitude,
            "longitude": longitude
        })

        if not station:
            return self._empty_response()

        station_id = station.get("station_id")

        if not station_id:
            return self._empty_response()

        end_date = date.today()

        start_date = (
            end_date -
            timedelta(days=self.period_days)
        )

        summary = get_inmet_weather_summary.invoke({
            "station_id": station_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })

        has_data = self._has_data(summary)

        return {
            "available": True,
            "has_data": has_data,

            "station": {
                "id": station.get("station_id"),
                "name": station.get("station_name"),
                "distance_km": station.get("distance_km")
            },

            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },

            "summary": (
                summary
                if has_data
                else None
            )
        }

    @staticmethod
    def _has_data(
        summary: dict | None
    ) -> bool:

        if not summary:
            return False

        return any(
            value is not None
            for value in summary.values()
        )

    @staticmethod
    def _empty_response() -> dict:

        return {
            "available": False,
            "has_data": False,
            "station": None,
            "period": None,
            "summary": None
        }