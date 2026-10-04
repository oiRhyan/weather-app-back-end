from langchain_core.tools import tool
from app.services.weather_service import WeatherService

weather_service = WeatherService()

@tool
def get_weather(
    latitude: float,
    longitude: float,
    forecast_days: int = 3
) -> dict:
    """
    Obtém as condições meteorológicas atuais e a previsão
    para uma localização usando latitude e longitude.

    Args:
        latitude: Latitude da localização.
        longitude: Longitude da localização.
        forecast_days: Quantidade de dias de previsão. 
                       Deve estar entre 1 e 16.

    Returns:
        Dados meteorológicos atuais e previsão.
    """
    print("Calling getWeather summary")
    return weather_service.get_weather(
        latitude=latitude,
        longitude=longitude,
        forecast_days=forecast_days
    )