from app.services.client.client_api import ApiClient

class WeatherService:

    def __init__(self):
        self.client = ApiClient(
            base_url="https://api.open-meteo.com/v1"
        )

    def get_weather(
        self,
        latitude: float,
        longitude: float,
        forecast_days: int = 3
    ):
        params = {
            "latitude": latitude,
            "longitude": longitude,

            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_gusts_10m",
                "pressure_msl",
            ]),

            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "precipitation_probability",
                "wind_speed_10m",
                "wind_gusts_10m",
            ]),

            "daily": ",".join([
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
            ]),

            "forecast_days": forecast_days,
            "timezone": "auto",
        }

        return self.client.get(
            "/forecast",
            params=params
        )